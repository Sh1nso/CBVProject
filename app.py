# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from SchemaClasses import MovieScheme

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


movie_schema = MovieScheme()
movies_schema = MovieScheme(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        all_movies = Movie.query.all()
        return movies_schema.dump(all_movies), 200


@movie_ns.route('/<int:id>')
class MovieView(Resource):
    def get(self, id):
        one_movie = Movie.query.get(id)
        return movie_schema.dump(one_movie), 200


@movie_ns.route('/director/')
class MovieView(Resource):
    def get(self):
        data = request.args['director_id']
        all_movies_by_director = db.session.query(Movie).filter(Movie.director_id == int(data))
        if not all_movies_by_director.all():
            return "", 404
        return movies_schema.dump(all_movies_by_director.all()), 200


@movie_ns.route('/genre/')
class MovieView(Resource):
    def get(self):
        data = request.args['genre_id']
        all_movies_by_genre = db.session.query(Movie).filter(Movie.genre_id == int(data))
        if not all_movies_by_genre.all():
            return '', 404
        return movies_schema.dump(all_movies_by_genre.all()), 200


if __name__ == '__main__':
    app.run(debug=True)
