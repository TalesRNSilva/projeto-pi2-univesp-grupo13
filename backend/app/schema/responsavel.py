from pydantic import BaseModel, model_validator, ConfigDict, computed_field
from schema.base_schema import BaseSchema
import datetime as dt
from utils import convert_numeric_to_display_id

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