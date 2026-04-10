"""Arquivo de teste da API"""
import json
import pytest

from app import app


@pytest.fixture
def client():
    """Configura o cliente para testes"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_redirect(client):
    """Testa o redirecionamento da rota home '/' para a página inicial."""
    response = client.get('/')
    assert response.status_code == 302
    assert '/front/index.html' in response.location

def test_docs_redirect(client):
    """Testa o redirecionamento da rota '/documentacao' para a documentação OpenAPI."""
    response = client.get('/documentacao')
    assert response.status_code == 302
    assert '/openapi' in response.location

def test_get_predictions_route(client):
    """Testa a rota GET /predictions para listar predições."""
    response = client.get('/predictions')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'predictions' in data


@pytest.fixture
def sample_prediction_data():
    """Dados de exemplo para uma predição."""
    return {
        "farmer": "Produtor de Teste",
        "crop": 2026,
        "size": -1.5,
        "weight": -1.8,
        "sweetness": -2.0,
        "crunchiness": -1.2,
        "juiciness": 0.8,
        "ripeness": 1.5,
        "acidity": -0.6
    }

def test_add_and_delete_prediction_route(client, sample_prediction_data):
    """Testa a rota POST /predictions para adicionar uma nova predição."""

    # 1. Adicionar uma nova predição (POST /predictions)
    response = client.post('/predictions', json=sample_prediction_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'id' in data
    assert data['farmer'] == sample_prediction_data['farmer']

    # 2. Deletar a predição recém-criada (DELETE /predictions)
    response_delete = client.delete(f'/predictions?id={data['id']}')
    assert response_delete.status_code == 200
    delete_data = json.loads(response_delete.data)
    assert 'removida com sucesso' in delete_data['message']

def test_delete_nonexistent_prediction(client):
    """Testa a remoção de uma predição que não existe (deve retornar 404)."""
    response = client.delete('/predictions?id=999999')
    assert response.status_code == 404
    error_data = json.loads(response.data)
    assert 'não encontrada' in error_data['message']
