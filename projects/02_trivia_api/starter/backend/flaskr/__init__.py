import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  
  # Cross Origin Resource Sharing configuration
  cors=CORS(app, resources={r"/": {"origins": "*"}})
  setup_db(app)
 
  # Using after_request decorator to set Access-Control-Allow  
  @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods','GET,PATCH,POST,DELETE,OPTIONS')
        return response



  def retrieve_categories():
    # Get categories and put into a dictionary
    return {question.id:question.type for question in Category.query.all() }
  
  def paginate_questions(request, selection):
    # Pagination
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE 
    end = start + QUESTIONS_PER_PAGE 
    
    questions = [question.format() for question in selection] 
    current_questions = questions[start:end] 
    return current_questions
  
  # Endpoint to handle GET requests for all available categories
  @app.route('/categories', methods=['GET']) 
  def get_categories():
    return jsonify({
      'success' : True,
      'categories' : retrieve_categories() 
    })
        
  
  # Endpoint to handle GET requests for questions      
  @app.route('/questions', methods=['GET'])
  def get_questions():
    #Grab all questions ordering by ID
    selection = Question.query.order_by(Question.id).all()
    
    # paginate questions
    current_questions = paginate_questions(request, selection)
   
    # HTTP 404 response if no questions  
    if len(current_questions) == 0:
          abort(404)
          
    return jsonify({
      'success' : True,
      'questions' : current_questions, 
      'total_questions' : len(selection),
      'current_category' : None,
      'categories' : retrieve_categories() 
    })
 
  # Endpoint to DELETE question using question ID 
  @app.route('/questions/<int:id>', methods=['DELETE'])     
  def delete_question(id):
    try:
      question = Question.query.filter(Question.id == id).one_or_none()
          
      if question is None:
        abort(404)
          
      question.delete()
          
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)
         
    except:
      abort(422)
    
    return jsonify({
      'success' : True,
      'questions' : current_questions, 
      'total_questions' : len(selection),
      'current_category' : None,
      'categories' : retrieve_categories() 
    }) 
  
 # POST Endpoint - Used to Endpoint to add a new trivia question or to search for a question
  @app.route('/questions', methods=["POST"])      
  def post_endpoint():
    body = request.get_json()
   
    # Check to see if searchTerm is in the body, this is based on ./frontend/src/components/QuestionView.js
    if (body.get('searchTerm')):
      try:
        # Grab the string to search for
        phrase = body.get('searchTerm')
        
        # Search for questions that mach the search string and order by id #
        selection = Question.query.filter(Question.question.ilike(f'%{phrase}%')).order_by(Question.id).all()
   
      except:
        abort(422) 
    else:
      # Populate the variables for each of the question fields
      new_question = body.get('question')    
      new_answer = body.get('answer')
      new_difficulty = body.get('difficulty')
      new_category = body.get('category')

      # Validate that all the fields were filled out
      if any(q == None for q in [new_question, new_answer, new_difficulty, new_category]):
        abort(422)
      
      try:
        # Create new question and add into database using insert
        question = Question(question=new_question, answer=new_answer, 
                          difficulty=new_difficulty, category=new_category)
        question.insert()
        selection = Question.query.order_by(Question.id).all()
    
      except:
        abort(422)
    
    # Whether we added or searched,  paginate the questions before returning them
    current_questions = paginate_questions(request, selection)
      
    return jsonify({
      'success' : True,
      'questions' : current_questions, 
      'total_questions' : len(selection),
      'current_category' : None,
      'categories' : retrieve_categories() 
    }) 



  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    