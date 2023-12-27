from typing import Optional, List
from fastapi import Depends, Path, Query
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from config.database import Session
from models.movie import Movie as Movie_model
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200,dependencies=[Depends(JWTBearer())]) 
#
def get_movies() -> List[Movie] :
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# parametros en ruta
@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
# Path valida los parametros de la ruta
def get_movie(id: int = Path(ge=1)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content="No se encontro el registro")    
    return JSONResponse(content=jsonable_encoder(result))
    

# parametros query
# validar parametros query con Path
@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No hay peliculas registradas"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# metodo post
# esquema de datos
@movie_router.post('/movies',tags=['movies'], response_model=dict,status_code=201)
def create_movie(movie: Movie) -> dict:
    try:
        db = Session()
        MovieService(db).create_movie(movie)
        return JSONResponse(status_code=201, content={"message": "Pelicula Registrada"})
    except:
        return JSONResponse(status_code=422, content={"message": "Error al agregar la pelicula"})

# metodo update
@movie_router.put('/movie/{id}',tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie)-> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Pelicula No encontrada"})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message": "Pelicula Actualizada"})

# metodo delete
@movie_router.delete('/movie/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int)-> dict:
    db = Session()
    result = db.query(Movie_model).filter(Movie_model.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Pelicula No encontrada"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200,content={"message": "Pelicula Eliminada"})
# 