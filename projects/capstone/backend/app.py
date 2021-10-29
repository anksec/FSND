import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

#import database.models
#import auth.auth
from database.models import db_drop_and_create_all, setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  app.url_map.strict_slashes = False
  setup_db(app)
  #CORS(app)
 
   
  db_drop_and_create_all()
  
  print([actor.format() for actor in Actor.query.order_by(Actor.id).all()])
  
  @app.route('/movies/', methods=['GET'])
  #@requires_auth('get:movies')
  def get_movies():
    print("Attempting to get movies")
    selection = Movie.query.order_by(Movie.id).all()
    movies = [movie.format() for movie in selection]
    
    if len(movies) == 0:
      abort(404)
      
    return jsonify({
      'success' : True,
      'movies' : movies
    })

    
  @app.route('/actors', methods=['GET'])
  def get_actors():
    selection = Actor.query.order_by(Actor.id).all()
    
    actors = [actor.format() for actor in selection]
    
    if len(actors) == 0:
      abort(404)
      
    return jsonify({
      'success' : True,
      'actors' : actors
    })  
    
  @app.route('/actors/<int:id>', methods=['GET'])
  #@requires_auth('get:actors')
  def show_actor(id):
    actor = Actor.query.get(id)
    
    if len(actor) == 0:
      abort(404)
 
    return jsonify({
      'success' : True,
      'actor' : actor.format()
    })  
    
  @app.route('/movies/<int:id>', methods=['GET'])
  #@requires_auth('get:movies')
  def show_movie(id):
    movie = Movie.query.get(id)
    
    if not movie: 
      abort(404)
 
    return jsonify({
      'success' : True,
      'movie' : movie
    })  
    
  @app.route('/actors/<int:id>', methods=['DELETE'])
  #@requires_auth('delete:actors')
  def delete_actor(id):
    actor = Actor.query.get(id)
    
    if not actor:
      abort(404) 
      
    try:
      actor.delete()
    except:
      abort(400)
   
    return jsonify({
        'success' : True,
        'delete' : id 
    }) 

    
  @app.route('/movies/<int:id>', methods=['DELETE'])
  #@requires_auth('delete:movies')
  def delete_movie(id):
    movie = Movie.query.get(id)
    
    if not movie:
      abort(404) 
      
    try:
      movie.delete()
    except:
      abort(400)
   
    return jsonify({
        'success' : True,
        'delete' : id 
    })
    
  @app.route('/actors/<int:id>', methods=['POST'])
  #@requires_auth('add:actors')
  def add_actor(id):
    body = request.get_json()
    try:
      name = body.get('name')
      age = body.get('age')
      gender = body.get('gender')
      #movies = body.get('movies')
      
      actor = Actor(name=name, age=age, gender=gender)
      actor.insert()
   
    except:
      abort(400)
      
    return jsonify({
        'success' : True,
        'actor' : [actor.format()]
    }) 
       
  @app.route('/movies/<int:id>', methods=['POST'])
  #@requires_auth('add:movies')
  def add_movie(id):
    body = request.get_json()
    try:
      title = body.get('title')
      release = body.get('release')
      #actors = body.get('actors')
      
      movie = Movie(title=title, release=release)
      movie.insert()
   
    except:
      abort(400)
      
    return jsonify({
        'success' : True,
        'movie' : [movie.format()]
    })
    
  @app.route('/actors/<int:id>', methods=['PATCH'])
  #@requires_auth('update:actors')
  def update_actor(id):
    actor = Actor.query.get(id)
    
    if not actor:
      abort(404)
    
    body = request.get_json()
    try:
      name = body.get('name')
      age = body.get('age')
      gender = body.get('gender')
      #movies = body.get('movies') 
      if name:
        actor.name = name
      if age: 
        actor.age = age
      if gender:
        actor.gender = gender
      #if movies:
      #  actor.movies = movies
        
    except:
      abort(400)
      
    return jsonify({
        'success' : True,
        'actors' : [actor.format()]
    })     
    
  @app.route('/movies/<int:id>', methods=['PATCH'])
  #@requires_auth('update:movies')
  def update_movie(id):
    movie = Movie.query.get(id)
    
    if not movie:
      abort(404)
    
    body = request.get_json()
    try:
      title = body.get('title')
      release = body.get('release')
      #actors = body.get('actors')
      
      if title:
        movie.title = title
      if release: 
        movie.release = release 
      #if actors: 
      #  movie.actors = actors 
        
    except:
      abort(400)
      
    return jsonify({
        'success' : True,
        'actors' : [movie.format()]
    }) 

  return app

app = create_app()




if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)