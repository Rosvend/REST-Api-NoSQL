from pydantic import BaseModel, Field
from typing import Optional

class CompuestoPorMedicamento(BaseModel):
    id: Optional[str] = Field(alias="_id")
    medicamento_id: str
    compuesto_id: str
    concentracion: float
    unidad: str
