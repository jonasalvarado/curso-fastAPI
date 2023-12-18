from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Any, Coroutine, Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI(
    title="CURSO FASTAPI",
    description="API de referencia para el curso",
    version='1.0.0'
)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales Invalidas")

class User(BaseModel):
    email:str
    password:str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3,max_length=15)
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
movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar II',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    }  
]

@app.get('/')
def message():
    return "Bienvenido al API de my-movie-api"

@app.get('/response_html')
def response_html():
    return HTMLResponse('<h1>Hola Bienvenido al API de movies</h1>')

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie] :
    return JSONResponse(status_code=200, content=movies)

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
    return JSONResponse(status_code=200, content=token)

# parametros en ruta
@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
# Path valida los parametros de la ruta
def get_movie(id: int = Path(ge=1)) -> Movie:
    for item in movies:
        if item['id'] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=404, content="No se encontro el registro")

# parametros query
# validar parametros query con Path
@app.get('/movies/',tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=3)):
    for item in movies:
        if item['category'] == category:
            return JSONResponse(content=item)
    return JSONResponse(content=[])

# metodo post
# esquema de datos
@app.post('/movies',tags=['movies'], response_model=dict,status_code=201)
def create_movie(movie: Movie) -> dict:
    try:
        movies.append(movie)
        return JSONResponse(status_code=201, content={"message": "Pelicula Registrada"})
    except:
        return JSONResponse(status_code=422, content={"message": "Error al agregar la pelicula"})

# metodo update
@app.put('/movie/{id}',tags=['movies'], status_code=200)
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['category'] = movie.category
            item['rating'] = movie.rating
    return JSONResponse(status_code=200, content={"message": "Pelicula Actualizada"})

# metodo delete
@app.delete('/movie/{id}',tags=['movies'], status_code=200)
def delete_movie(id: int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
    return JSONResponse(status_code=200,
                         content={"message": "Pelicula Eliminada"})
# 