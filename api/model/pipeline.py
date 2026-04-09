"""Pipeline do modelo de predição de qualidade de maçãs"""
import pickle


class Pipeline:
    """Classe para carregar o modelo e realizar predições"""

    def __init__(self):
        """Inicializa o pipeline"""
        self.pipeline = None

    def carrega_pipeline(self, path):
        """Carrega o pipeline"""
        with open(path, 'rb') as file:
            self.pipeline = pickle.load(file)
        return self.pipeline
