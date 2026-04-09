"""init dos models"""
import os
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from model.base import Base
from model.apple_quality import AppleQuality
from model.preprocessador import Preprocessador
from model.pipeline import Pipeline


# URL de acesso ao banco de dados
DB_PATH = "database/"

# Verifica se o diretório não existe e cria um caso não exista
if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH)

# URL de acesso ao banco de dados
DB_URL = f'sqlite:///{DB_PATH}/db_predictions.sqlite3'

# Cria a conexão com o banco de dados
engine = create_engine(DB_URL, echo=False)

# Instancia um criador de seção com o banco de dados
Session = sessionmaker(bind=engine)

# Cria o banco de dados se ele não existir
if not database_exists(engine.url):
    create_database(engine.url)

# Cria as tabelas do banco de dados
Base.metadata.create_all(engine)
