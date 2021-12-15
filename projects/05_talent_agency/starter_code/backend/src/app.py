import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS
from flask_migrate import Migrate
import json

from models import db,setup_db, db_drop_and_create_all,db_populate, Actor, Movie 
from auth import AuthError, requires_auth

def create_app(test_config=None):
  app = Flask(__name__)


  if test_config == "Test":
    setup_db(app, database_path=os.getenv('TEST_DATABASE_URL'))
  else:
    setup_db(app)
  CORS(app, resources={"*":{"origins":"*"}})

  # For testing and development, this line should be commented out for Production
  db_populate()

# ROUTES

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,PATCH,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Origin','*')
    return response 


  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(payload):
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
  @requires_auth('get:actors')
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
    selection = Movie.query.order_by(Movie.id).all()
    movies = [movie.format() for movie in selection]
    print("Movie database", movies)
    movie = Movie.query.get(id)
    if not movie:
      print("There is no movie")
      abort(404) 
      
    try:
      print("Trying to delete movie")
      movie.delete()
    except:
      abort(400)
   
    return jsonify({
      'success' : True,
      'delete' : id 
    })
    
  @app.route('/actors', methods=['POST'])
  @requires_auth('add:actor')
  def add_actor(payload):
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
       
  @app.route('/movies', methods=['POST'])
  @requires_auth('add:movie')
  def add_movie(payload):
    body = request.get_json()
    try:
      title = body.get('title')
      release_date = body.get('release_date')
      #actors = body.get('actors')
      
      movie = Movie(title=title, release_date=release_date)
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
      'movie' : [movie.format()]
      }) 
    
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

  @app.errorhandler(403)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 403, 
      "message": "invalid permissions"
      }), 403

  @app.errorhandler(401)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 401, 
      "message": "unauthorized"
      }), 401

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'Unprocessable'
    }), 422

# Catch errors from auth.py
  @app.errorhandler(AuthError)
  def handle_auth_error(ex):
      response = jsonify(ex.error)
      response.status_code = ex.status_code
      return response


# Based on Auth0 Auth Error example - https://auth0.com/docs/quickstart/backend/python/01-authorization
# Class AuthError is in ./backend/src/auth/auth.py
  @app.errorhandler(AuthError)
  def auth_error(error):
    response = jsonify(error.error)
    response.status_code = error.status_code 
    return response

  return app


app = create_app()  
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)