"""Classe do Avaliador"""
from sklearn.metrics import accuracy_score


class Avaliador:
    """Classe do Avaliador"""

    def __init__(self):
        """Inicializa o avaliador"""

    def avaliar(self, model, x_teste, y_teste):
        """Avalia o modelo"""
        predicoes = model.predict(x_teste)

        return accuracy_score(y_teste, predicoes)
