from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="CURSO FASTAPI",
    description="API de referencia para el curso",
    version='1.0.0'
)

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } 
]

@app.get('/')
def message():
    return "Bienvenido al API de my-movie-api"
@app.get('/html')
def response_html():
    return HTMLResponse('<h1>Hola Bienvenido al API de movies</h1>')
@app.get('/movies', tags=['movies'])
def get_movies():
    return movies