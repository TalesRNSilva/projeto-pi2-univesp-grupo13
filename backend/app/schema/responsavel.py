from pydantic import BaseModel, model_validator, ConfigDict, computed_field, Field
from .base_schema import BaseSchema
import datetime as dt
from ..utils import convert_numeric_to_display_id

# Modelos de saída
class ResponsavelResponse(BaseSchema):
    "Modelo de resposta da entidade Responsavel. Deve ser retornado em todo get que envolva a entidade."
    id: int
    nome: str
    email: str | None
    cadastro_timestamp: dt.datetime
    ativo: bool

    @computed_field
    @property
    def display_id(self) -> str:
        return convert_numeric_to_display_id(self.id).replace("O", "R")

    # outro modo de fazer isso:
    # display_id:str = ""
    # @model_validator(mode = 'after')
    # def add_display_id(self):
    #     self.display_id = convert_numeric_to_display_id(self.id).replace('O', 'R')
    #     return self

class ResponsavelResponseLean(BaseSchema):
    "Modelo de resposta da entidade Responsavel. Deve ser retornado em todo get que envolva a entidade."
    nome: str
    email: str | None

# Modelos de entrada
class ResponsavelPost(BaseSchema):
    "Modelo de entrada da entidade Responsavel."
    nome: str
    email: str | None

class ResponsavelPut(BaseSchema):
    "Modelo de atualização da entidade Responsavel"
    nome: str | None = Field(default = None, min_length = 2, max_length = 100)
    email: str | None = Field(default = None)