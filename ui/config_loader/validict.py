from pydantic import BaseModel, Field, ValidationError, model_validator

class config_val(BaseModel):
    #Primera validacion
    width: int = Field(ge=11, le=30)
    height: int = Field(ge=7, le=30)
    entry: tuple[int, int] #Recordar hacer el split para convertirlo.
    _exit: tuple[int, int]
    output_file: str
    perfect: bool

"""
    #Ahora validacion tipo filtro.
    @model_validator(mode="after")
    def validate_mission(self) -> Self:
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with M")

        has_leader = any(
            member.rank in (Rank.CAPTAIN, Rank.COMMANDER)
            for member in self.crew
        )
"""


class list_validation(BaseModel):
    lista: list[config_val] = Field(e=6)
    """
        Ahroa el siguiente paso es ver como meter y validar las claves, tengo que decir no solamente hay 6 cosas en el archivo sino que deben de estar los siguientes apartados""""

class process_val():
    def manage(lista: list[dict[str, str]]) -> None
        for dic in lista:
            if dic.item == ""
