import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app,database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRADBCK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

#Many to Many relationship setup 
movies_and_actors = db.Table('movies_and_actors',
    db.Column('actor_id', db.Integer, db.ForeignKey('Actor.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('Movie.id'), primary_key=True)
)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    movie = Movie(
        title='V for Vendetta',
        release_date='2006-03-17'
    )
    actor = Actor(
        name='Natalie Portman',
        age=40,
        gender='Female',
    )

    actor.movies.append(movie)

    actor.insert()
    movie.insert()


class Actor(db.Model):
  __tablename__ = 'Actor'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  age = db.Column(db.Integer)
  gender = db.Column(db.String)
  movies = db.relationship('Movie', secondary=movies_and_actors, backref=db.backref('actors',lazy=True))
 
  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender
    
  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender,
      'movies': [m.format() for m in self.movies]
    }

  def __repr__(self):
    return json.dumps(self.format())
    
  
class Movie(db.Model):
  __tablename__ = 'Movie'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  release_date = db.Column(db.Date)
 
  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date
    
  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date
    } 

  def __repr__(self):
    return json.dumps(self.format())
