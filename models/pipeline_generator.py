import numpy as np
import pandas as pd
import joblib
import random
from surprise import Reader, Dataset, KNNBasic
from scipy.spatial.distance import pdist, squareform

def compute_jaccard_similarity(trainset, user_based=True):
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

def train_user_user(k, save_path="./models/pipelines/user_user_model.joblib"):
    """
    Train a User-User collaborative filtering model using Jaccard, Cosine, and Pearson similarities.
    """
    train_pipeline(True, k, save_path)

def train_item_item(k, save_path="./models/pipelines/item_item_model.joblib"):
    """
    Train an Item-Item collaborative filtering model using Jaccard, Cosine, and Pearson similarities.
    """
    train_pipeline(False, k, save_path)

def train_pipeline(user_based, k, save_path):
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
    ratings = pd.read_csv('./Dataset 100k/u.data', engine='python', sep='\t',
                          names=['user_id', 'item_id', 'rating', 'timestamp'])
    
    reader = Reader(rating_scale=(1, 5))
    surprise_dataset = Dataset.load_from_df(ratings[['user_id', 'item_id', 'rating']], reader)
    
    # Train models for each similarity metric
    trainset = surprise_dataset.build_full_trainset()
    for model_name in similarities:
        sim_options = {'name': model_name, 'user_based': user_based}
        algo = KNNBasic(k=k, min_k=2, sim_options=sim_options)
        algo.fit(trainset)
        models[model_name] = algo
    
    # Compute Jaccard manually
    jaccard_matrix = compute_jaccard_similarity(trainset, user_based)
    models['jaccard'] = jaccard_matrix

    # Save models
    joblib.dump(models, save_path)
    print(f"Model {save_path} saved successfully!")

def predict(model_path, id_usuario, k, similarity):
    """
    Load a trained model and predict top-K recommendations for a user using a selected similarity metric.
    """
    models = joblib.load(model_path)
    model = models.get(similarity)

    if model is None:
        raise ValueError(f"Invalid similarity metric: {similarity}")

    # Load dataset
    ratings = pd.read_csv('./Dataset 100k/u.data', engine='python', sep='\t',
                            names=['user_id', 'item_id', 'rating', 'timestamp'])
    items = pd.read_csv('./Dataset 100k/u.item', engine='python', sep='\|',
                        names=['movie id', 'movie title', 'release date', 'video release date', 'IMDb URL ', 'unknown',
                                'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama',
                                'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'],
                        encoding='latin-1')

    if similarity == "jaccard":
        # Find k-nearest users or items
        nearest_neighbors = np.argsort(model[id_usuario])[-k:]

        # Convert to DataFrame
        df_predictions = pd.DataFrame({'movie id': nearest_neighbors})
        df_predictions = df_predictions.merge(items[['movie id', 'movie title', 'IMDb URL ']], on='movie id', how='left')

        df_predictions.rename(columns={
            "movie id": "movie_id",
            "movie title": "movie_title",
            "IMDb URL ": "imdb_url"
        }, inplace=True)

        print(df_predictions, end="\n\n")
        return df_predictions
    
    reader = Reader(rating_scale=(1, 5))
    surprise_dataset = Dataset.load_from_df(ratings[['user_id', 'item_id', 'rating']], reader)
    trainset = surprise_dataset.build_full_trainset()
    test = trainset.build_anti_testset()

    # Generate predictions
    predictions = model.test(test)
    user_predictions = list(filter(lambda x: x[0] == id_usuario, predictions))
    user_predictions.sort(key=lambda x: x.est, reverse=True)
    top_k = user_predictions[:k]

    # Convert to DataFrame
    labels = ['movie id', 'estimation']
    df_predictions = pd.DataFrame.from_records(list(map(lambda x: (x.iid, x.est), top_k)), columns=labels)
    df_predictions = df_predictions.merge(items[['movie id', 'movie title', 'IMDb URL ']], on='movie id', how='left')

    df_predictions.rename(columns={
        "movie id": "movie_id",
        "movie title": "movie_title",
        "IMDb URL ": "imdb_url"
    }, inplace=True)

    print(df_predictions, end="\n\n")
    return df_predictions

if __name__ == "__main__":
    k = 20  # Number of neighbors
    train_user_user(k)
    train_item_item(k)
