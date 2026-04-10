"""Arquivo principal da aplicação"""
from flask import redirect
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import SQLAlchemyError

from model import Session, AppleQuality, Preprocessador, Pipeline
from schemas import ErrorSchema, apresenta_predicoes, \
    ListAppleQualitySchema, AppleQualityDelSchema, \
    AppleQualityDelResponseSchema, AppleQualityViewSchema, \
    AppleQualitySchema, apresenta_predicao


# Instanciando o objeto OpenAPI
info = Info(title="API Apple Quality", version="1.0.0")
app = OpenAPI(
    __name__,
    info=info,
    static_folder='../front',
    static_url_path='/front'
    )
CORS(app)

# Definindo tags para grupo de rotas
home_tag = Tag(
    name="Página inicial",
    description="Página inicial da aplicação"
    )
documentation_tag = Tag(
    name="Documentação",
    description="Documentação das Rotas da API"
    )
predictions_tag = Tag(
    name="Predições",
    description="Adição, Visualização e Remoção de Predições"
    )

# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para página inicial"""
    return redirect('/front/index.html')

# Rota para documentação da api
@app.get('/documentacao', tags=[documentation_tag])
def documentacao():
    """Redireciona para documentação."""
    return redirect('/openapi')

# Rota de listagem das predições realizadas
@app.get('/predictions', tags=[predictions_tag], \
         responses={"200": ListAppleQualitySchema, "404": ErrorSchema})
def get_predictions():
    """
    Retorna uma lista de predições cadastradas no banco de dados.
    Args:
        none
    
    Returns:
        list: lista de predições cadastradas no banco de dados.
    """
    # Cria conexão com o banco de dados
    session = Session()
    # Faz a busca
    predictions = session.query(AppleQuality).all()

    if not predictions:
        # Se não há predições cadastradas, retorna
        return {"predictions": []}, 200

    # Converte a lista
    return apresenta_predicoes(predictions), 200

# Rota de remoção de predições
@app.delete('/predictions', tags=[predictions_tag], \
            responses={"200": AppleQualityDelResponseSchema, "404": ErrorSchema})
def delete_prediction(query: AppleQualityDelSchema):
    """
    Remove uma predição cadastrada no banco de dados.

    Args:
        id (int): id da predição a ser removida.

    Returns:
        message: Mensagem de sucesso ou erro.
        id: id da predição removida.
    """

    prediction_id = query.id

    # Cria conexão com o banco de dados
    session = Session()

    # Busca a predição
    prediction = session.query(AppleQuality).filter(AppleQuality.id == prediction_id).first()

    if not prediction:
        # Se a predição não for encontrada, retorna um erro
        error_msg = "Predição não encontrada no banco de dados :/"
        return {"message": error_msg}, 404

    session.delete(prediction)
    session.commit()
    return {"message": f"Predição {prediction_id} removida com sucesso!"}, 200

# Rota de adição de predições
@app.post('/predictions', tags=[predictions_tag], \
          responses={"200": AppleQualityViewSchema, "400": ErrorSchema})
def add_prediction(form: AppleQualitySchema):
    """
    Adiciona uma nova predição no banco de dados.

    Args:
        farmer (str): nome do produtor.
        crop (str): safra.
        size (float): tamanho da maçã.
        weight (float): peso da maçã.
        sweetness (float): doçura da maçã.
        crunchiness (float): crocância da maçã.
        juiciness (float): suculência da maçã.
        ripeness (float): maturação da maçã.
        acidity (float): acidez da maçã.

    Returns:
        Dict: Predição adicionada.
    """

    # Instanciando as classes
    preprocessador = Preprocessador()
    pipeline = Pipeline()

    # Recuperando os dados do formulário
    farmer = form.farmer
    crop = str(form.crop)
    size = form.size
    weight = form.weight
    sweetness = form.sweetness
    crunchiness = form.crunchiness
    juiciness = form.juiciness
    ripeness = form.ripeness
    acidity = form.acidity

    # Preparando os dados para o modelo
    x_input = preprocessador.preparar_formulario(form)

    # Carregando o modelo
    model_path = "./MachineLearning/pipelines/svm_apple_quality.pkl"
    modelo = pipeline.carrega_pipeline(model_path)

    # Realizando a predição
    quality = int(modelo.predict(x_input)[0])

    predicao = AppleQuality(
        farmer=farmer,
        crop=crop,
        size=size,
        weight=weight,
        sweetness=sweetness,
        crunchiness=crunchiness,
        juiciness=juiciness,
        ripeness=ripeness,
        acidity=acidity,
        quality=quality
    )

    try:
        # Criando conexão com o banco de dados
        session = Session()

        # Adicionando a predição
        session.add(predicao)
        session.commit()

        # Concluindo transação
        return apresenta_predicao(predicao), 200

    except SQLAlchemyError as e:
        error_msg = "Não foi possível salvar nova predição :/"
        print(e)
        return {"message": error_msg}, 400

if __name__ == "__main__":
    app.run(debug=True)
