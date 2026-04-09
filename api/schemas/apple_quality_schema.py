"""Schema de representação das frutas"""
from typing import List
from pydantic import BaseModel

from model.apple_quality import AppleQuality


class AppleQualitySchema(BaseModel):
    """ Define como uma nova fruta a ser inserida deve ser representada
    """
    farmer: str = "João Silva"
    crop: str = "2023/2024"
    size: float = -0.5
    weight: float = -1.2
    sweetness: float = -2.3
    crunchiness: float = -0.8
    juiciness: float = 0.5
    ripeness: float = 1.2
    acidity: float = -0.4

class AppleQualityViewSchema(BaseModel):
    """ Define como uma fruta será retornada.
    """
    id: int = 1
    farmer: str = "João Silva"
    crop: str = "2023/2024"
    size: float = -0.5
    weight: float = -1.2
    sweetness: float = -2.3
    crunchiness: float = -0.8
    juiciness: float = 0.5
    ripeness: float = 1.2
    acidity: float = -0.4
    quality: int = 1

class AppleQualitySearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id da fruta.
    """
    id: int = 1

class ListAppleQualitySchema(BaseModel):
    """ Define como uma lista de frutas será retornada.
    """
    predictions: List[AppleQualityViewSchema]

class AppleQualityDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    id: int

class AppleQualityDelResponseSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção bem-sucedida.
    """
    message: str

def apresenta_predicao(prediction: AppleQuality):
    """ Retorna uma representação da fruta seguindo o schema definido em
        AppleQualityViewSchema.
    """
    return {
        "id": prediction.id,
        "farmer": prediction.farmer,
        "crop": prediction.crop,
        "size": prediction.size,
        "weight": prediction.weight,
        "sweetness": prediction.sweetness,
        "crunchiness": prediction.crunchiness,
        "juiciness": prediction.juiciness,
        "ripeness": prediction.ripeness,
        "acidity": prediction.acidity,
        "quality": prediction.quality
    }

def apresenta_predicoes(predictions: List[AppleQuality]):
    """ Retorna uma representação da lista de frutas seguindo o schema definido
        em AppleQualityViewSchema.
    """
    result = [apresenta_predicao(prediction) for prediction in predictions]
    return {"predictions": result}
