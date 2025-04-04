# ----------------------------------------------------------------
# Vamos a utilizar las siguientes librerias
# ----------------------------------------------------------------
import numpy as np
import pandas as pd
from surprise import Reader
from surprise import Dataset
from surprise.model_selection import train_test_split
from surprise import KNNBasic
from surprise import accuracy
import random
import matplotlib.pyplot as plt

#Para garantizar reproducibilidad en resultados
seed = 10
random.seed(seed)
np.random.seed(seed)

# ----------------------------------------------------------------
# Suba al servidor los archivos u.data y u.item que se encuentran
# en el dataset descargado, en la pestaña files
# ----------------------------------------------------------------

ratings=pd.read_csv('../Dataset 100k/u.data', sep = '\t', names = [ 'user_id', 'item_id', 'rating', 'timestamp' ] )

items=pd.read_csv('../Dataset 100k/u.item', sep = '\|', names = ['movie id' ,'movie title','release date','video release date','IMDb URL ','unknown',
                                                                'Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama',
                                                                'Fantasy','Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western'], encoding='latin-1' )

reader = Reader( rating_scale = ( 1, 5 ) )
surprise_dataset = Dataset.load_from_df(ratings[['user_id', 'item_id', 'rating']], reader)

train_set, test_set=  train_test_split(surprise_dataset, test_size=.2)

# ----------------------------------------------------------------
# Creación de modelo de filtrado colaborativo basado en similitud
# con usuarios o items cercanos
# ----------------------------------------------------------------

# 3.ii) Se crea un modelo knnbasic usuario-usuario con similitud coseno
sim_options = {'name': 'cosine',
               'user_based': True
               }
algo_uu_cosine = KNNBasic(k=20, min_k=2, sim_options=sim_options)
algo_uu_cosine.fit(trainset=train_set)

print(algo_uu_cosine.predict(154,302))
print(items[items['movie id']==302][["movie id", "movie title", "release date"]], end="\n\n")

test_predictions=algo_uu_cosine.test(test_set)
print(accuracy.rmse(test_predictions, verbose = True), end="\n\n")

# ----------------------------------------------------------------
# Generando listas de predicciones para los usuarios:
#
# Se crea un dataset de "test" con las entradas faltantes de la
# matriz utilidad para que el modelo cree las predicciones
# (terminar de llenar la matriz de utilidad)
# ----------------------------------------------------------------

rating_data=surprise_dataset.build_full_trainset()
test=rating_data.build_anti_testset()

# Se crea el mismo modelo
sim_options = {'name': 'cosine',
               'user_based': False # True
               }
algo_uu_cosine = KNNBasic(k=20, min_k=2, sim_options=sim_options)
algo_uu_cosine.fit(rating_data)
predictions = algo_uu_cosine.test(test)

user_predictions=list(filter(lambda x: x[0]==196,predictions))  # Predicciones para usuario 196
user_predictions.sort(key=lambda x : x.est, reverse=True)  # Ordenamos de mayor a menor estimación de relevancia
top_10 = user_predictions[0:10]

# Se convierte a dataframe
labels = ['movie id', 'estimation']
df_predictions = pd.DataFrame.from_records(list(map(lambda x: (x.iid, x.est) , top_10)), columns=labels)

# Lo unimos con el dataframe de películas
df_predictions = df_predictions.merge(items[['movie id', 'movie title', 'IMDb URL ']], how='left', on='movie id')
print(df_predictions, end="\n\n")
