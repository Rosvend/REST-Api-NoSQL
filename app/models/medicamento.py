from pydantic import BaseModel, Field
from typing import Optional

class Medicamento(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    nombre: str
    fabricante: str
    
    class Config:
        populate_by_name = True
        json_encoders = {
            str: lambda v: v
        }