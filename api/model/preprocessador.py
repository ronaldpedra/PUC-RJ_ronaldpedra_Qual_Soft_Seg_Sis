"""Preprocessador de dados"""
import pickle
from sklearn.model_selection import train_test_split
import numpy as np


class Preprocessador:
    """Classe de pré-processamento de dados"""

    def __init__(self):
        """Inicializa o preprocessador"""

    def separar_teste_treino(self, dataset, percentual_teste, seed=7):
        """Separa os dados em treino e teste"""
        x_treino, x_teste, y_treino, y_teste = self.__preparar_holdout(dataset, percentual_teste, seed)
        return (x_treino, x_teste, y_treino, y_teste)

    def __preparar_holdout(self, dataset, percentual_teste, seed):
        """Divide os dados em treino e teste"""
        dados = dataset.values
        x = dados[:, 0:-1]
        y = dados[:, -1]
        return train_test_split(x, y, test_size=percentual_teste, random_state=seed)

    def preparar_formulario(self, prediction_input):
        """Prepara os dados do formulário"""
        x_input = np.array([
            prediction_input.size,
            prediction_input.weight,
            prediction_input.sweetness,
            prediction_input.crunchiness,
            prediction_input.juiciness,
            prediction_input.ripeness,
            prediction_input.acidity
        ]).reshape(1, -1)
        return x_input

    def scaler(self, x_treino):
        """Faz o escalonamento dos dados"""

        # Normalização/Padronização
        scaler = pickle.load(open('./MachineLearning/scalers/minmax_scaler_apple_quality.pkl', 'rb'))
        reescaled_x_treino = scaler.fit_transform(x_treino)
        return reescaled_x_treino
