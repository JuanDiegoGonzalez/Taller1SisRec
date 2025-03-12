from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView

from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.model.forms import CreateForm
from apps.model.process import predict
from apps.movie_rating.models import MovieRating
from apps.movie.models import Movie
from django.contrib.auth.models import User

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from surprise import Reader, Dataset, KNNBasic
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import pairwise_distances

import time, json, joblib, random

import pandas as pd
import numpy as np

#-------------------------------------
# Nuevo endpoint
#-------------------------------------
@method_decorator(csrf_exempt, name="dispatch")
class ModelView(View):
    template_name = "movies/movie_list.html"

    def get(self, request):
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    def post(self, request):
        try:
            data = json.loads(request.body)  # Get JSON data from request
            modelo = data.get('modelo')
            tipo = data.get('tipo')
            k = data.get('k')

            if not modelo or not tipo or k is None:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Start processing
            start_time = time.time()
            # TODO
            print(modelo, tipo, k, int(data.get('user').get('username')))
            predicciones = predict(modelo, tipo, k, int(data.get('user').get('username')))
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time:.4f} seconds")

            # Convert predictions to JSON format
            predicciones_json = predicciones.to_dict(orient='records')

            return JsonResponse(predicciones_json, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

@method_decorator(csrf_exempt, name="dispatch")
class ModelTrainView(View):

    def compute_jaccard_similarity(self, trainset, user_based=True):
        """
        Compute Jaccard similarity efficiently using sparse matrices.

        Args:
            trainset (surprise.Trainset): The training set from Surprise.
            user_based (bool): Whether to compute user-user or item-item similarity.

        Returns:
            np.ndarray: Jaccard similarity matrix.
        """

        num_users = trainset.n_users
        num_items = trainset.n_items

        user_id_mapping = {trainset.to_raw_uid(i): i for i in trainset.all_users()}

        rows, cols, data = [], [], []
        for uid, iid, _ in trainset.all_ratings():
            rows.append(uid if user_based else iid)  # Users as rows if user-based, otherwise items
            cols.append(iid if user_based else uid)  # Items as columns if user-based, otherwise users
            data.append(1)  # Binary presence (1 means interaction exists)

        # Create sparse binary interaction matrix
        shape = (num_users, num_items) if user_based else (num_items, num_users)
        interaction_matrix = csr_matrix((data, (rows, cols)), shape=shape)

        # Compute Jaccard similarity manually
        intersection = interaction_matrix @ interaction_matrix.T  # Count co-occurrences
        row_sums = interaction_matrix.sum(axis=1)  # Total interactions per user/item
        union = row_sums + row_sums.T - intersection  # Union size

        # Avoid division by zero (replace 0s in the denominator with 1)
        union[union == 0] = 1
        jaccard_sim = intersection / union  # Compute Jaccard index

        # Convert to dense NumPy array
        jaccard_sim = jaccard_sim.toarray()

        # Ensure diagonal is 1 (self-similarity)
        np.fill_diagonal(jaccard_sim, 1.0)
        print(f"Jaccard similarity matrix (dense) shape: {jaccard_sim.shape}")
        return jaccard_sim, user_id_mapping

    def train_pipeline(self, user_based, k, save_path):
        """
        Train a collaborative filtering model using Surprise and save it.
        """
        similarities = ["cosine", "pearson"]
        models = {}

        # Ensure reproducibility
        seed = 10
        random.seed(seed)
        np.random.seed(seed)

        # Load dataset
        ratings_qs = MovieRating.objects.values("user_id", "movie_id", "rating")
        ratings = pd.DataFrame(list(ratings_qs))

        if ratings.empty:
            print("No ratings found in the database.")
            return

        # Rename columns to match Surprise format
        ratings.rename(columns={"movie_id": "item_id"}, inplace=True)

        reader = Reader(rating_scale=(1, 5))
        surprise_dataset = Dataset.load_from_df(ratings[['user_id', 'item_id', 'rating']], reader)

        # Train models for each similarity metric
        trainset = surprise_dataset.build_full_trainset()
        for model_name in similarities:
            sim_options = {'name': model_name, 'user_based': user_based}
            print(sim_options)
            algo = KNNBasic(k=k, min_k=2, sim_options=sim_options)
            algo.fit(trainset)
            models[model_name] = algo

        # Compute Jaccard manually
        print({'name': "Jaccard", 'user_based': user_based})

        # Compute Jaccard with ID mapping
        jaccard_matrix, user_id_mapping = self.compute_jaccard_similarity(trainset, user_based)
        models['jaccard'] = {"matrix": jaccard_matrix, "id_map": user_id_mapping}

        # Save models
        joblib.dump(models, save_path)
        print(f"Model {save_path} saved successfully!")

    def train_user_user(self, k, save_path="./models/pipelines/new/user_user_model.joblib"):
        """
        Train a User-User collaborative filtering model using Jaccard, Cosine, and Pearson similarities.
        """
        self.train_pipeline(True, k, save_path)

    def train_item_item(self, k, save_path="./models/pipelines/new/item_item_model.joblib"):
        """
        Train an Item-Item collaborative filtering model using Jaccard, Cosine, and Pearson similarities.
        """
        self.train_pipeline(False, k, save_path)


    """
    Requests
    """
    def get(self, _):
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    def post(self, _):
        try:
            # Start processing
            start_time = time.time()
            self.train_user_user(20)
            self.train_item_item(20)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time:.4f} seconds")


            return JsonResponse({"Success": "Trained model succesfully"}, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

@method_decorator(csrf_exempt, name="dispatch")
class ModelPredictView(View):

    def predict(self, p_model_name, p_user_based, k, id_usuario):
        """
        Load a trained model and predict top-K recommendations for a user using a selected similarity metric.
        """
        match p_model_name:
            case "Jaccard":
                similarity = "jaccard"
            case "Coseno":
                similarity = "cosine"
            case "Pearson":
                similarity = "pearson"

        match p_user_based:
            case "Usuario-Usuario":
                model_path = "./models/pipelines/new/user_user_model.joblib"
            case _:
                model_path = "./models/pipelines/new/item_item_model.joblib"

        models = joblib.load(model_path)
        model = models.get(similarity)

        if model is None:
            raise ValueError(f"Invalid similarity metric: {similarity}")

        # Load dataset

        ratings_qs = MovieRating.objects.values("user_id", "movie_id", "rating")
        ratings = pd.DataFrame(list(ratings_qs))

        # Rename columns to match Surprise format
        ratings.rename(columns={"movie_id": "item_id"}, inplace=True)
        items_df = pd.DataFrame(list(Movie.objects.values("id", "title", "image_url", "avg_rating")))

        reader = Reader(rating_scale=(1, 5))
        surprise_dataset = Dataset.load_from_df(ratings[['user_id', 'item_id', 'rating']], reader)
        trainset = surprise_dataset.build_full_trainset()

        if similarity == "jaccard":
            jaccard_matrix = model["matrix"]
            user_id_mapping = model["id_map"]

            # Ensure user exists
            if id_usuario not in user_id_mapping:
                raise ValueError(f"User {id_usuario} not found in training data.")

            # Get inner ID
            inner_id = user_id_mapping[id_usuario]

            # Find k-nearest users/items
            nearest_neighbors = np.argsort(jaccard_matrix[inner_id])[-k:]

            df_predictions = pd.DataFrame({'id': nearest_neighbors})
            items_df = pd.DataFrame(list(Movie.objects.values("id", "title", "image_url", "avg_rating")))
            df_predictions = df_predictions.merge(items_df[["id", "title", "image_url", "avg_rating"]], on='id', how='left')

            print(df_predictions, end="\n\n")
            return df_predictions

        # Get items rated by the user
        user_rated_items = set(trainset.ur[trainset.to_inner_uid(id_usuario)])

        # Get all items in the dataset
        all_items = set(trainset.all_items())

        # Find items not rated by user
        unrated_items = list(all_items - user_rated_items)

        # Create test set for only the unrated items of the user
        user_test_set = [(id_usuario, trainset.to_raw_iid(item_id), 0) for item_id in unrated_items]

        # Generate predictions
        predictions = model.test(user_test_set)
        user_predictions = list(filter(lambda x: x[0] == id_usuario, predictions))
        user_predictions.sort(key=lambda x: x.est, reverse=True)
        top_k = user_predictions[:k]

        # Convert to DataFrame
        labels = ['id', 'estimation']
        df_predictions = pd.DataFrame.from_records(list(map(lambda x: (x.iid, x.est), top_k)), columns=labels)
        df_predictions = df_predictions.merge(items_df[["id", "title", "image_url", "avg_rating"]], on='id', how='left')

        print(df_predictions, end="\n\n")
        return df_predictions


    """
    Requests
    """
    def get(self, _):
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    def post(self, request):
        try:

            data = json.loads(request.body)  # Get JSON data from request
            modelo = data.get('modelo')
            tipo = data.get('tipo')
            k = data.get('k')
            id_usuario = data.get('userId')

            if not modelo or not tipo or k is None:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            print(data)
            # Start processing
            start_time = time.time()
            predictions = self.predict(modelo, tipo, k, id_usuario)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time:.4f} seconds")
            predictions_json = predictions.to_dict(orient='records')

            return JsonResponse(predictions_json, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

#-------------------------------------
# Anteriores endpoints
#-------------------------------------
class ModelOldCreateView(LoginRequiredMixin, CreateView):
    template_name = 'model/model_form.html'
    success_url = reverse_lazy('model:model_result')

    def get(self, request):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        
        model = form.save(commit=False)
        model.owner = request.user

        start_time = time.time()  # Start timer
        # TODO
        predicciones = predict(model.modelo, model.tipo, model.k, int(model.owner.username))
        end_time = time.time()  # End timer
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.4f} seconds")

        predicciones_json = predicciones.to_dict(orient='records')

        request.session['predicciones'] = predicciones_json
        return redirect(self.success_url)

class ModelOldResultView(View):
    template_name = "model/model_result.html"

    def get(self, request) :
        context = {'predicciones' : request.session['predicciones']}
        return render(request, self.template_name, context)
    