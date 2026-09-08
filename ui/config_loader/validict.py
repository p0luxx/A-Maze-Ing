from pydantic import BaseModel, Field, ValidationError, model_validator

class config_val(BaseModel):
    #Primera validacion
    width: int = Field(alias="WIDTH", ge=11, le=30)
    height: int = Field(alias= "HEIGHT", ge=7, le=30)
    entry: tuple[int, int] = Field(alias="ENTRY")
    _exit: tuple[int, int] = Field(alias="EXIT")
    output_file: str = Field(alias="OUTPUT_FILE")
    perfect: bool = Field(alias="PERFECT")


    #Ahora validacion tipo filtro.
    @model_validator(mode="after")
    def validate_mission(self) -> Self:
        if (self.entry[0] > self.width and self.entry[0] < 0) and 
         (self.entry[1] > self.height and self.entry[1] < 0):
            raise ValueError("Entry coordinates must be in the grid limits")
        if (self._exit[0] > self.width and self.exit[0] < 0) and
         (self.exit[1] > self.height and self.exit[1] < 0):
            raise ValueError("Exit coordinates must be in the grid limits")
        if entry == _exit:
            raise ValueError("Entry and exit coordinates cannot be the same")
