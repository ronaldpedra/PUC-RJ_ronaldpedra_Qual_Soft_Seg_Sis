"""Classe modelo"""
import pickle


class Model:
    """Classe modelo"""

    def __init__(self):
        """Inicializa o modelo"""
        self.model = None

    def carrega_modelo(self, path):
        """Carrega o modelo conforme o tipo de arquivo"""

        if path.endswith('.pkl'):
            with open(path, 'rb') as file:
                self.model = pickle.load(file)
        else:
            raise Exception('Formato de arquivo inválido')
        return self.model

    def preditor(self, x_input):
        """Realiza a predição"""
        if self.model is None:
            raise Exception('Modelo não carregado')
        diagnosis = self.model.predict(x_input)
        return diagnosis
