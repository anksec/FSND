import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

# Used for pagination to determine the number of questions per page
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

  # Get categories and put into a dictionary
  def retrieve_categories():
    return {category.id:category.type for category in Category.query.all() }
  
  # take in list of questions and paginate them 
  def paginate_questions(request, selection):
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
      'current_category' : 'ALL',
      'categories' : retrieve_categories() 
    })
 
  # Endpoint to DELETE question using question ID 
  @app.route('/questions/<int:question_id>', methods=['DELETE'])     
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
          
      if question is None:
        abort(422)
          
      question.delete()
          
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)
         
    except:
      abort(422)
    
    return jsonify({
      'success' : True,
    }), 200
  
  # POST Endpoint - Used to Endpoint to add a new trivia question or to search for a question
  @app.route('/questions', methods=['POST'])      
  def post_endpoint():
    body = request.get_json()
   
    # Check to see if searchTerm is in the body, this is based on ./frontend/src/components/QuestionView.js
    if (body.get('searchTerm')):
      try:
        # Grab the string to search for
        phrase = body.get('searchTerm')
        
        # Search for questions that mach the search string and order by id #
        selection = Question.query.filter(Question.question.ilike(f'%{phrase}%')).order_by(Question.id).all()
        if len(selection) == 0:
          abort(422)
        current_questions = paginate_questions(request, selection)
   
      except:
        abort(422) 
      
      return jsonify({
        'success' : True,
        'questions' : current_questions, 
        'total_questions' : len(selection),
        'current_category' : 'ALL',
      })  
      
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
    
      except:
        abort(422)
        
      return jsonify({
        'success' : True,
      }), 200
    
  # GET endpoint to get questions based on category
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_category(category_id):
    selection = Question.query.filter(Question.category == int(category_id)).order_by(Question.id).all()
    
    current_questions = paginate_questions(request, selection)
    
    # Get name of current category based on the ID
    current_category = retrieve_categories()[category_id]
    
    return jsonify({
      'success' : True,
      'questions' : current_questions, 
      'total_questions' : len(selection),
      'current_category' : current_category, 
    }) 
    
  # POST endpoint to get questions to play quiz
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    body = request.get_json()
    category_id = body.get('quiz_category')['id']
    
    # List of questions that have already been asked of the user for the session
    previous_questions = body.get('previous_questions')
   
    # All categories is a category_id of 0
    if category_id == 0:
      selection = Question.query.all()
    else:
      selection = Question.query.filter(Question.category == category_id).all()

    # Create a list of all questions that haven't been asked before
    valid_questions = []
    for question in selection:
      if question.id not in previous_questions:
        valid_questions.append(question)
        
    # if all trivia questions in the category have been asked, don't return any questions
    if len(valid_questions) == 0:
      return jsonify({
        'success' : False
      })
    else:
      return jsonify({
      'success' : True,
      'question' : random.choice(valid_questions).format(), 
    })
      

  # Error handlers for 400, 404, 405 & 422
  # Based on Section 3, Lesson 3 - Flask Error Handling 
  @app.errorhandler(404)    
  def not_found(error):
    return (
      jsonify({"success": False, "error": 404, "message": "resource not found"}),
      404,
    )
    
  @app.errorhandler(422)
  def unprocessable(error):
    return (
      jsonify({"success": False, "error": 422, "message": "unprocessable"}),
      422,
    )

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "bad request"}), 400
      
    
  return app