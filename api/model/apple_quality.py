"""Base de dados para tabela de predições"""
from datetime import datetime
from typing import Union
from sqlalchemy import Column, String, Integer, DateTime, Float

from model import Base


class AppleQuality(Base):
    """Tabela de predições de qualidade de maçãs"""
    __tablename__ = 'apple_quality'

    id = Column(Integer, primary_key=True)
    farmer = Column("Produtor", String(50))
    crop = Column("Safra", String(20))
    size = Column("Tamanho", Float)
    weight = Column("Peso", Float)
    sweetness = Column("Doçura", Float)
    crunchiness = Column("Crocância", Float)
    juiciness = Column("Suculência", Float)
    ripeness = Column("Maturação", Float)
    acidity = Column("Acidez", Float)
    quality = Column("Qualidade", Integer, nullable=True)
    date = Column(DateTime, default=datetime.now())

    def __init__(
        self,
        farmer: str,
        crop: str,
        size: float,
        weight: float,
        sweetness: float,
        crunchiness: float,
        juiciness: float,
        ripeness: float,
        acidity: float,
        quality: int,
        date: Union[DateTime, None] = None
    ):
        """
        Cria um predição de qualidade de maçã
        
        Arguments:
            farmer: nome do produtor
            crop: safra
            size: tamanho da maçã
            weight: peso da maçã
            sweetness: doçura da maçã
            crunchiness: crocância da maçã
            juiciness: suculência da maçã
            ripeness: maturação da maçã
            acidity: acidez da maçã
            quality: qualidade da maçã
            date: data da predição
        """
        self.farmer = farmer
        self.crop = crop
        self.size = size
        self.weight = weight
        self.sweetness = sweetness
        self.crunchiness = crunchiness
        self.juiciness = juiciness
        self.ripeness = ripeness
        self.acidity = acidity
        self.quality = quality
        if date:
            self.date = date
