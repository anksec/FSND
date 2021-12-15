import os
from flask import Flask, request, jsonify, abort
from SQLAlchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
# Returns the drink.short() data representation of all drinks
# if no drinks, returns 404
# Does not require authentication
@app.route('/drinks', methods=['GET'])
def get_drinks():
    selection = Drink.query.order_by(Drink.id).all()
    drinks = [drink.short() for drink in selection]
    
    if len(drinks) == 0:
        abort(404)
    
    return jsonify({
        'success' : True,
        'drinks' : drinks
    })


# Gets detailed drink info 
# Requires authentication with the get:drinks-detail permission
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    print("Are we here")
    selection = Drink.query.order_by(Drink.id).all()
    print(selection)
    drinks = [drink.long() for drink in selection]
    
    if len(drinks) == 0:
        abort(404)
    
    return jsonify({
        'success' : True,
        'drinks' : drinks
    })

# Creates a new drink
# Requires authentication with post:drinks permissions
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):
    body = request.get_json()
    try: 
        title = body.get('title')
        recipe = body.get('recipe')
        
        # Recipe is a string representation.  models.py uses json.loads, using the reverse json.dumps here
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()
    
    except:
        abort(400)
    
    return jsonify({
        'success' : True,
        'drinks' : [drink.long()]
    }) 

# Updates a drink given the drink id
# Requires authentication with patch:drinks permissions
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(payload,id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    
    body = request.get_json()
    try: 
        title = body.get('title')
        recipe = body.get('recipe')
        if title:
            drink.title = title
        if recipe:
            drink.recipe = json.dumps(recipe)
        
        drink.update()
    except:
        abort(400)
    
    return jsonify({
        'success' : True,
        'drinks' : [drink.long()]
    })  

# Deletes a drink given the drink id
# Requires authentication with delete:drinks permissions
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload,id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    
    try:
        drink.delete()
    except:
        abort(400) 
    
    return jsonify({
        'success' : True,
        'delete' : id 
    }) 


# Error Handling
# Current supported codes - 400, 404, 422

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
