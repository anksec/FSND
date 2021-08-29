import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
   
    # Test cases based on Section 3, Lesson 4 - API Testing and
    # expected behavior of the trivia API
    def test_get_categories(self):
        response = self.client().get("/categories")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        print("\nPassed GET categories test")
        
    def test_get_paginated_questions(self):
        response = self.client().get("/questions?page=1")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 10)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])
        self.assertTrue(data["categories"])
        print("\nPassed GET paginated questions test")
    
    def test_404_requesting_beyond_valid_page(self):
        response = self.client().get("/questions?page=10")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        print("\nPassed 404 beyond valid question page test")
    
    def test_get_questions_from_category(self):
        response = self.client().get("/categories/1/questions")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])
        print("\nPassed GET questions from category test")
  
    # Comment out as it will only work once unless database is refreshed
    ''' 
    def test_delete_question(self):
        response = self.client().delete("/questions/9")
        data = json.loads(response.data)
        question = Question.query.filter(Question.id == 9).one_or_none()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(question, None)
        
        print("\nPassed DELETE question test")
    '''
      
    def test_get_quiz_question(self):
        response = self.client().post("/quizzes", json={'previous_questions': [], 
                                                    'quiz_category': {'type': 'Science', 'id': '1'} })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        
        print("\nPassed retrieve quiz question based on category")
 
    # Comment out to avoid adding same question
    # During test, id was 24
    ''' 
    def test_adding_question(self):
        response = self.client().post("/questions", json={'question': 'What is 1+1?', 
                                                          'answer': '3',
                                                          'difficulty' : 2,
                                                          'category': 1
                                                    })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        print("\nPassed add quiz question")
    '''     
    
    def test_searching_question(self):
        response = self.client().post("/questions", json={ 'searchTerm': 'What is 1+1?' })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])
        
        print("\nPassed search for question")
    
    def test_422_response_with_search(self):
        response = self.client().post("/questions", json={ 'searchTerm': 'abracadabrawhosethere' })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        
        print("\nPassed 422 response")
        
        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()