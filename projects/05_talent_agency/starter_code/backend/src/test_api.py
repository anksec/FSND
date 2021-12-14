import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import base64

from models import setup_db, db_drop_and_create_all, Actor, Movie 
from auth import AuthError, requires_auth
from app import create_app
full_token = 'bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklEZjNhdGJVQU11X3JUSXI1Q2t6WCJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYW5rLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJaaFNTbWZnbTB3ZHZ1cW0yVk1iZVFyNU5nbUoxWU84UUBjbGllbnRzIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYzOTM0MTIzNywiZXhwIjoxNjM5NDI3NjM3LCJhenAiOiJaaFNTbWZnbTB3ZHZ1cW0yVk1iZVFyNU5nbUoxWU84USIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyJ9.oQM6WnbxAKUaM1ipzvnYQm_PyGc07CqgKF-6HjMyaBRcU6OfWBWFmvNCtXSWyykdTpmmw6UmmnB7KW8M7uxqWnFFJKcZ1zmgD7YEiwMqITnC1EmSVskitUFH5xss77OhHCU-kBaFqxKGLyXIaSQBSGdUvulC5ciAq0nzsem7x9Xxm7-nzq4uKs6M_vb5EP0TLvrpMh-kT_KAQe9X7s118HT_7zzJc83J7X-VZ2XrTAXEXhIoaN_kiVqHfkxQwemLWdea1f2qpe0Ay5Utz1ju3BgI1h9oa-8W-hBP3fHpB7VyRwOUDC5fBw_-nbEdfiIpsw3_9qpUf2-tbHkIDIKecg'
#producer_token =  'bearer ' + str(os.getenv('executive_producer_token'))
#director_token =  'bearer ' + str(os.getenv('casting_director_token'))
#assistant_token =  'bearer ' + str(os.getenv('casting_assistant_token'))
#print("Assistant_token", assistant_token)
#full_token =  'bearer ' + str(os.getenv('full_access_token'))

class CastingTestCase(unittest.TestCase):
    """This class represents the Casting test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("Test")
        self.client = self.app.test_client
        # Shouldn't need this as the api sets up the database
        #self.database_path = DB_PATH 
        #setup_db(self.app, self.database_path)

        # binds the app to the current context
        #with self.app.app_context():
        #    self.db = SQLAlchemy()
        #    self.db.init_app(self.app)
            # create all tables
        #    self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
   
    # Test cases based on Section 3, Lesson 4 - API Testing and
    # expected behavior of the trivia API
    def test_get_movies(self):
        response = self.client().get("/movies", headers={'Authorization' : full_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])
        print("\nPassed GET movies test with permissions of Casting Assistant")
    
    def test_get_actors(self):
        response = self.client().get("/actors", headers={'Authorization' : full_token})
        print("Response is:", response)
        data = json.loads(response.data)
        print("Printing output of GET actors test")
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])
        print("\nPassed GET actors test with permissions of Casting Assistant")
    """
        
    def test_get_movie(self):
        response = self.client().get("/movies/1", headers={'Authorization' : assistant_token})
        data = json.loads(response.data)
        print("Printing output of GET movie #1 test")
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])
        print("\nPassed GET movie #1 test with permissions of Casting Assistant")

    def test_get_actor(self):
        response = self.client().get("/actors/1", headers={'Authorization' : assistant_token})
        data = json.loads(response.data)
        print("Printing output of GET #1 actor test")
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])
        print("\nPassed GET actor #1 test with permissions of Casting Assistant")

    def test_delete_actor(self):
        response = self.client().delete("/actors/1", headers={'Authorization' : director_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["delete"], 1)
        print("\nPassed DELETE actor #1 test with permissions of Casting Director")
        
    def test_delete_movie(self):
        response = self.client().delete("/movies/1", headers={'Authorization' : producer_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["delete"], 1)
        print("\nPassed DELETE movie #1 test with permissions of Executive Producer")

    def test_add_movie(self):
        movie = {
            'title':'Desperado',
            'release_date':'1995-08-25'
        } 

        response = self.client().post("/movies", json=movie, headers={'Authorization' : producer_token})
        data = json.loads(response.data)
        print("Printing output of ADD movie test")
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])
        print("\nPassed ADD movie test with permissions of Executive Producer")

    def test_add_actor(self):
        actor = {
            'name':'Selma Hayek',
            'age':55,
            'gender':'Female',
        } 
        response = self.client().post("/actors", json=actor, headers={'Authorization' : director_token})
        data = json.loads(response.data)
        print("Printing output of ADD actor test")
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])
        print("\nPassed GET actor #1 test with permissions of Casting Director")

    def test_update_movie(self):
        updated_movie = {
            'title':'The Wedding Singer',
            'release_date':'1998-02-13'
        } 
        response = self.client().patch("/movies/2", json=updated_movie, headers={'Authorization' : director_token})
        data = json.loads(response.data)
        print("Printing output of UPDATE movie test")
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])
        print("\nPassed UPDATE movie test with permissions of Casting Director")
        
    def test_update_actor(self):
        updated_actor = {
            'name':'Drew Barrymore',
            'age':46,
            'gender':'Female'
        } 
        response = self.client().patch("/actors/2", json=updated_actor, headers={'Authorization' : director_token})
        data = json.loads(response.data)
        print("Printing output of UPDATE actor test")
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])
        print("\nPassed UPDATE actor test with permissions of Casting Director")
    
    def test_404_requesting_invalid_actor(self):
        response = self.client().get("/actors/99", headers={'Authorization' : full_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        print("\nPassed 404 Getting Invalid actor test")

    def test_404_deleting_invalid_actor(self):
        response = self.client().delete("/actors/99", headers={'Authorization' : full_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        print("\nPassed 404 Deleting Invalid actor test")

    def test_403_actor_update_without_perms(self):
        updated_actor = {
            'name':'Drew Barrymore',
            'age':50,
            'gender':'Female'
        } 
        response = self.client().patch("/actors/1", json=updated_actor, headers={'Authorization' : assistant_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "invalid permissions")
        print("\nPassed 403 Invalid permissions test for updating actors (permissions of Casting Assistant)" )

    def test_404_requesting_invalid_movie(self):
        response = self.client().get("/movies/99", headers={'Authorization' : full_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        print("\nPassed 404 Getting Invalid movie test")

    def test_404_deleting_invalid_actor(self):
        response = self.client().delete("/movies/99", headers={'Authorization' : full_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        print("\nPassed 404 Deleting Invalid movie test")

    def test_403_update_movie_without_perms(self):
        updated_movie = {
            'title':'The Wedding Singer',
            'release_date':'1996-02-13'
        } 
        response = self.client().patch("/movies/1", json=updated_movie, headers={'Authorization' : assistant_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "invalid permissions")
        print("\nPassed 403 Invalid permissions test for updating movies (permissions of Casting Assistant)")
    """ 

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
