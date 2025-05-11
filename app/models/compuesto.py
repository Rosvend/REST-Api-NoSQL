from pydantic import BaseModel, Field
from typing import Optional

class Compuesto(BaseModel):
    id: Optional[str] = Field(alias="_id")
    nombre: str