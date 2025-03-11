import numpy as np
import pandas as pd
from surprise import Reader
from surprise import Dataset
from surprise.model_selection import train_test_split
from surprise import KNNBasic
from surprise import accuracy
import joblib

def predict(p_model_name, p_user_based, k, id_usuario):
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
            model_path = "./models/pipelines/user_user_model.joblib"
        case _:
            model_path = "./models/pipelines/item_item_model.joblib"

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
