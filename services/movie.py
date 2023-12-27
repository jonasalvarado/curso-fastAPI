from models.movie import Movie as Movie_model

class MovieService():
    def __init__(self,db):
        self.db = db

    def get_movies(self):
        result = self.db.query(Movie_model).all()
        return result
    
    def get_movie(self, id):
        result = self.db.query(Movie_model).filter(Movie_model.id == id).first()
        return result
    
    def get_movies_by_category(self, category):
        result = self.db.query(Movie_model).filter(Movie_model.category == category).all()
        return result
   
    def create_movie(self, movie: Movie_model):
        new_movie = Movie_model(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return
    
    def update_movie(self, id, data: Movie_model):
        movie = self.db.query(Movie_model).filter(Movie_model.id == id).first()
        movie.title = data.title
        movie.overview = data.overview
        movie.year = data.year
        movie.rating = data.rating
        movie.category = data.category
        self.db.commit()
        return

    def delete_movie(self, id):
        movie = self.db.query(Movie_model).filter(Movie_model.id == id)
        movie.delete()
        self.db.commit()
        return
        