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

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from surprise import Reader, Dataset, KNNBasic

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
        Compute Jaccard similarity for users or items.
        """
        num_entities = trainset.n_users if user_based else trainset.n_items
        interaction_matrix = np.zeros((num_entities, num_entities))

        for u in range(num_entities):
            for v in range(num_entities):
                if u != v:
                    set_u = set(trainset.ur[u]) if user_based else set(trainset.ir[u])
                    set_v = set(trainset.ur[v]) if user_based else set(trainset.ir[v])

                    intersection = len(set_u & set_v)
                    union = len(set_u | set_v)

                    similarity = intersection / union if union != 0 else 0
                    interaction_matrix[u, v] = similarity

        return interaction_matrix

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
        ratings_qs = MovieRating.objects.values("user_id", "movie_id", "rating")  # Fetch relevant fields
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
        jaccard_matrix = self.compute_jaccard_similarity(trainset, user_based)
        models['jaccard'] = jaccard_matrix

        # Save models
        joblib.dump(models, save_path)
        print(f"Model {save_path} saved successfully!")

    def train_user_user(self, k, save_path="./models/new/pipelines/user_user_model.joblib"):
        """
        Train a User-User collaborative filtering model using Jaccard, Cosine, and Pearson similarities.
        """
        self.train_pipeline(True, k, save_path)

    def train_item_item(self, k, save_path="./models/new/pipelines/item_item_model.joblib"):
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
    