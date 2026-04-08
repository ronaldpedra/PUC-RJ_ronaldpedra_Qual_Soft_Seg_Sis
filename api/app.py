"""Arquivo principal da aplicação"""
from flask_openapi3 import OpenAPI, Info, Tag
from urllib.parse import unquote
from flask_cors import CORS
from flask import redirect


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
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc"
    )
fruta_tag = Tag(
    name="Fruta",
    description="Adição, visualização, remoção e predição de qualidade das frutas"
    )

# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para página inicial"""
    return redirect('/front/index.html')

if __name__ == "__main__":
    app.run(debug=True)
