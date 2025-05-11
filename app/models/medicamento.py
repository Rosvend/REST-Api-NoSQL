from pydantic import BaseModel, Field
from typing import Optional

class Medicamento(BaseModel):
    id: Optional[str] = Field(alias="_id")
    nombre: str
    fabricante: str