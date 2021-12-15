import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import base64

from models import db,setup_db, db_drop_and_create_all, db_populate, Actor, Movie 
from auth import AuthError, requires_auth
from app import create_app
producer_token =  str(os.getenv('executive_producer_token'))
director_token =  str(os.getenv('casting_director_token'))
assistant_token =  str(os.getenv('casting_assistant_token'))

class CastingTestCase(unittest.TestCase):
    """This class represents the Casting test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(test_config="Test")
        self.client = self.app.test_client
        self.database_path = os.getenv('TEST_DATABASE_URL')
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            self.db.create_all()
            #db_populate()
        
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

   
    # Test cases based on Section 3, Lesson 4 - API Testing and
    # expected behavior of the trivia API
    def test_get_movies(self):
        response = self.client().get("/movies", headers={'Authorization' : assistant_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])
        print("\nPassed GET movies test with permissions of Casting Assistant")

    def test_get_actors(self):
        response = self.client().get("/actors", headers={'Authorization' : assistant_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])
        print("\nPassed GET actors test with permissions of Casting Assistant")
   
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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])
        print("\nPassed ADD movie test with permissions of Executive Producer")
    
    def test_401_add_actor(self):
        actor = {
            'name':'Selma Hayek',
            'age':55,
            'gender':'Female',
        } 
        response = self.client().post("/actors", json=actor, headers={'Authorization' : director_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])
        print("\nPassed ADD actor test with permissions of Casting Director")
    
    def test_update_movie(self):
        updated_movie = {
            'title':'The Wedding Singer',
            'release_date':'1998-02-13'
        } 
        response = self.client().patch("/movies/2", json=updated_movie, headers={'Authorization' : director_token})
        data = json.loads(response.data)
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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])
        print("\nPassed UPDATE actor test with permissions of Casting Director")
    
    def test_401_actor_update_without_perms(self):
        updated_actor = {
            'name':'Drew Barrymore',
            'age':50,
            'gender':'Female'
        } 
        response = self.client().patch("/actors/1", json=updated_actor, headers={'Authorization' : assistant_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unauthorized")
        print("\nPassed 401 unauthorized test for updating actors (permissions of Casting Assistant)" )

    def test_401_update_movie_without_perms(self):
        updated_movie = {
            'title':'The Wedding Singer',
            'release_date':'1996-02-13'
        } 
        response = self.client().patch("/movies/1", json=updated_movie, headers={'Authorization' : assistant_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unauthorized")
        print("\nPassed 401 unauhotirzed test for updating movies (permissions of Casting Assistant)")

    def test_401_delete_actor(self):
        response = self.client().delete("/actors/1", headers={'Authorization' : assistant_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unauthorized")
        print("\nPassed 401 unauthorized DELETE actor #1 test with permissions of Casting Assistant")
    
    def test_401_delete_movie(self):
        response = self.client().delete("/movies/1", headers={'Authorization' : assistant_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unauthorized")
        print("\nPassed 401 unauthorized DELETE movie #1 test with permissions of Executive Assistant")

    def test_401_add_movie(self):
        movie = {
            'title':'The Grinch',
            'release_date':'1990-01-01'
        } 
        response = self.client().post("/movies", json=movie, headers={'Authorization' : assistant_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unauthorized")
        print("\nPassed 401 unauthorized ADD movie test with permissions of Casting Assistant")
    
    def test_401_add_actor(self):
        actor = {
            'name':'Selma Hayek',
            'age':55,
            'gender':'Female',
        } 
        response = self.client().post("/actors", json=actor, headers={'Authorization' : assistant_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unauthorized")
        print("\nPassed 401 unauthorized ADD actor test with permissions of Casting Assistant")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
