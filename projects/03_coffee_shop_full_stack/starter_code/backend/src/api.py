import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
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
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
# Returns the drink.short() data representation of all drinks
# if no drinks, returns 404
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


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
# Gets detailed drink info 
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail():
    selection = Drink.query.order_by(Drink.id).all()
    drinks = [drink.long() for drink in selection]
    
    if len(drinks) == 0:
        abort(404)
    
    return jsonify({
        'success' : True,
        'drinks' : drinks
    })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks():
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
        'drinks' : drink.long()
    }) 
         

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(id):
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
        'drinks' : drink.long()
    })  

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    
    try:
        drink.delete()
    except:
        abort(400) 
    
    return jsonify({
        'success' : True,
        'drinks' : id 
    }) 


# Error Handling
'''
Example error handling for unprocessable entity
'''


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
