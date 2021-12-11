import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

from .database.models import setup_db, db_drop_and_create_all, Actor, Movie 
from .auth.auth import AuthError, requires_auth

def create_app(test_cinfig=None):
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  '''
  db_drop_and_create_all is for initial testing.  Comment out when application goes to production
  '''
  db_drop_and_create_all()

# ROUTES

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,PATCH,POST,DELETE,OPTIONS')
    return response 


  @app.route('/movies/', methods=['GET'])
  #@requires_auth('view:movies')
  def get_movies():
    selection = Movie.query.order_by(Movie.id).all()
    movies = [movie.format() for movie in selection]
    
    if len(movies) == 0:
      abort(404)
      
    return jsonify({
      'success' : True,
      'total_movies' : len(movies),
      'movies' : movies
    })

    
  @app.route('/actors', methods=['GET'])
  @requires_auth('view:actors')
  def get_actors(payload):
  
    selection = Actor.query.order_by(Actor.id).all()
  
    actors = [actor.format() for actor in selection]
  
    if len(actors) == 0:
      abort(404)
      
    return jsonify({
      'success' : True,
      'total_actors' : len(actors),
      'actors' : actors
    })  
    
  @app.route('/actors/<int:id>', methods=['GET'])
  @requires_auth('view:actors')
  def show_actor(payload,id):
    actor = Actor.query.get(id)
    
    if len(actor) == 0:
      abort(404)
 
    return jsonify({
      'success' : True,
      'actor' : actor.format()
    })  
    
  @app.route('/movies/<int:id>', methods=['GET'])
  @requires_auth('view:movies')
  def show_movie(payload,id):
    movie = Movie.query.get(id)
    
    if not movie: 
      abort(404)

    return jsonify({
      'success' : True,
      'movie' : movie
    })  
    
  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actor')
  def delete_actor(payload,id):
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
  @requires_auth('delete:movie')
  def delete_movie(payload,id):
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
  @requires_auth('add:actor')
  def add_actor(payload,id):
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
  @requires_auth('add:movie')
  def add_movie(payload,id):
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
  @requires_auth('update:actor')
  def update_actor(payload,id):
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
  @requires_auth('update:movie')
  def update_movie(payload,id):
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
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
      }), 422
    
  @app.errorhandler(404)    
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404, 
      "message": "resource not found"
      }), 404
    

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400, 
      "message": "bad request"
      }), 400

# Based on Auth0 Auth Error example - https://auth0.com/docs/quickstart/backend/python/01-authorization
# Class AuthError is in ./backend/src/auth/auth.py
  @app.errorhandler(AuthError)
  def auth_error(error):
    response = jsonify(error.error)
    response.status_code = error.status_code 
    return response

  return app



APP = create_app()  

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
# Error Handling
# Current supported codes - 400, 404, 422
