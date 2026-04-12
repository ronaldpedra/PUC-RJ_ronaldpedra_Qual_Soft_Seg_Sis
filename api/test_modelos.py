"""Arquivo de teste dos modelos"""
from model import Carregador, Model, Avaliador, Pipeline


carregador = Carregador()
modelo = Model()
avaliador = Avaliador()
Pipeline = Pipeline()

# Parâmetros
URL_DADOS = './MachineLearning/data/test_dataset_apple_quality.csv'
COLUNAS = ['Size', 'Weight', 'Sweetness', 'Crunchiness', 'Juiciness', 'Ripeness', 'Acidity', 'Label']

# Carga dos dados
dataset = carregador.carregar_dados(URL_DADOS, COLUNAS)
array = dataset.values
x = array[:,0:-1]
y = array[:,-1]

# Método para testar o modelo de Random Forest a partir do arquivo correspondente
def test_modelo_rf():
    """Testando o modelo de Random Forest."""
    # Importando o modelo de Random Forest
    rf_path = './MachineLearning/models/rf_apple_quality.pkl'
    modelo_rf = modelo.carrega_modelo(rf_path)

    # Obtendo as métricas da RF
    acuracia_rf = avaliador.avaliar(modelo_rf, x, y)
    # assert acuracia_rf >= 0.704
    assert acuracia_rf >= 0.77875

def test_modelo_svm():
    """Testando o modelo SVM."""
    # Importando o modelo SVM
    svm_path = './MachineLearning/models/svm_apple_quality.pkl'
    modelo_svm = modelo.carrega_modelo(svm_path)

    # Obtendo as métricas da RF
    acuracia_svm = avaliador.avaliar(modelo_svm, x, y)
    assert acuracia_svm >= 0.704
    # assert acuracia_svm >= 0.77875

