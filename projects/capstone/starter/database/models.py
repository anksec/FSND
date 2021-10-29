import os
from sqlalchemy import Column, String, Integer, Date
from flask_sqlalchemy import SQLAlchemy 
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))


#DB_HOST = os.getenv('DB_HOST')  
#DB_USER = os.getenv('DB_USER')  
#DB_PASSWORD = os.getenv('DB_PASSWORD')  
#DB_NAME = os.getenv('DB_NAME')  
#DB_PATH = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRADBCK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test
    actor = Actor(
      name = "Natalie Portman",
      age = 40,
      gender = "Female"
    ) 
    print("Inserting actor")
    actor.insert()
    
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Actor(db.Model):
  __tablename__ = 'actors'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  age = db.Column(db.Integer)
  gender = db.Column(db.String)
  #movies = db.relationship("Movie", back_populates="actors")
 
  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender
    #self.movies = movies
    
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
      'gender': self.gender
    }
    
  
class Movie(db.Model):
  __tablename__ = 'movies'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  release_date = db.Column(db.Date)
  #actors = db.relationship("Actor", back_populates="movies")
 
  def __init__(self, title, release):
    self.title = title
    self.release = release
    #self.actors = actors
    
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
      'release': self.release
    } 