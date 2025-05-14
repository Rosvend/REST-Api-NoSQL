from pydantic import BaseModel, Field
from typing import Optional

class CompuestoPorMedicamento(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    medicamento_id: str
    compuesto_id: str
    concentracion: float
    unidad_medida: str = Field(alias="unidad")
    
    class Config:
        populate_by_name = True
        json_encoders = {
            str: lambda v: v
        }
