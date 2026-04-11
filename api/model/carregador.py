"""Carregador de dados"""
import pandas as pd


class Carregador:
    """Classe de carregamento de dados"""

    def __init__(self):
        """Inicializa o carregador"""

    def carregar_dados(self, url: str, atributos: list):
        """Carrega os dados"""

        return pd.read_csv(url, names=atributos, header=0, \
                           skiprows=0, delimiter=',')