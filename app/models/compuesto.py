from pydantic import BaseModel, Field
from typing import Optional

class Compuesto(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    nombre: str
    
    class Config:
        populate_by_name = True
        json_encoders = {
            str: lambda v: v
        }