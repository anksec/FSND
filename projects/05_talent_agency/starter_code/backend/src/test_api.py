import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import base64

from models import setup_db, db_drop_and_create_all, Actor, Movie 
from auth import AuthError, requires_auth
from app import create_app
full_token = 'bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9SVEhYeDhhYjlkSTBCRjZCQUdVbCJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWFuay51cy5hdXRoMC5jb20vIiwic3ViIjoiY250aXZ0Qm4yQUQ1c1N6N2JtY2FDamtyTmdjZTBydnJAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vY2FzdGluZy1hcGkvIiwiaWF0IjoxNjM5MzQyMDk0LCJleHAiOjE2Mzk0Mjg0OTQsImF6cCI6ImNudGl2dEJuMkFENXNTejdibWNhQ2prck5nY2UwcnZyIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOltdfQ.x8dP5bv29ePpUr2vAh4HZY1hi4nBFs2oOeENkaeziXjYiwFRHxNrV8CSfHtc1obfzdv2CTG39-SuNPdFrui6qMijQ-EJoKvADB7RsCN6YJh_zJ0pJXqhXOcGAWt8X3wOGbIEqrrKMD0LoP7ozhSeSLIfQs4ynWtIRN1S7Kj3P3uVBAiai2HGWrhKIg0ermY0dG71jKazrSh-Gl6LwUI_dOjoi77zueu7Ciggb-WoHAonJz5vSYuiPO8_mNEQ3uBhSlfPYc7zmpZRqLWtC9IihDQzQ6XTlRTZ9MCVZjeOc16Vocnxhsj6luAeVNoBeGcNCEoJfZXvzDYhWLDBaQokdg'
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
