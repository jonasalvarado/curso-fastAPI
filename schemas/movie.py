from typing import Optional
from pydantic import BaseModel, Field

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3,max_length=35)
    overview: str
    year: int
    rating: float
    category: str
# valores por defecto....
    
model_config = {
        "json_schema_extra":{
                "example":{
                    "id": 1,
                    "title": "esto es un valor por defecto",
                    "overview": "Texto de prueba",
                    "year": 2000,
                    "rating": 5.69,
                    "category": "terror"
                }
        }
    }
