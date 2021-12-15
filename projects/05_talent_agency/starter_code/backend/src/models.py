import os
import re
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import json

DB_URL = os.getenv('DATABASE_URL')
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app,database_path=DB_URL):
    if database_path.startswith("postgres://"):
      database_path = database_path.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_TRADBCK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    db.app = app
    db.init_app(app)
    db.create_all()
    #migrate = Migrate(app,db)

#Many to Many relationship setup 
movies_and_actors = db.Table('movies_and_actors',
    db.Column('actor_id', db.Integer, db.ForeignKey('Actor.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('Movie.id'), primary_key=True)
)

def db_populate():
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

    #For test purposes, the below is incorrect on purpose
    actor2 = Actor(
      name='Drew Barrymore',
      age=45,
      gender='Female',
    )
    movie2 = Movie(
      title='The Wedding Singer',
      release_date='1998-02-14'
    )

    actor2.movies.append(movie2)

    actor2.insert()
    movie2.insert()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


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
  id = db.Column('id', db.Integer, primary_key=True)
  title = db.Column(db.String)
  release_date = db.Column(db.Date)
 
  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def get(self, id):
    print("testing")
    print(db.session.query().get(id))
    self.title = db.session.query().get(id).title
    self.release_template = db.session.query().get(id).release_date
    print("Self is",self)
    
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
