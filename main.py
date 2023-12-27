from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from utils.jwt_manager import create_token
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI(
    title="CURSO FASTAPI",
    description="API de referencia para el curso",
    version='1.0.1'
)

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

#
@app.get('/')
def message():
    return "Bienvenido al API de my-movie-api"
#
@app.get('/response_html')
def response_html():
    return HTMLResponse('<h1>Hola Bienvenido al API de movies</h1>')
#