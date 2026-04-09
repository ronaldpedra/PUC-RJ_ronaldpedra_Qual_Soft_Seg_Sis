"""Schema de erro"""
from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """ Define como uma mensagem de erro deve ser representada
    """
    message: str
