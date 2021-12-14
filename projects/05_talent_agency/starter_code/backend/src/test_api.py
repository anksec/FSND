import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import base64

from models import setup_db, db_drop_and_create_all, Actor, Movie 
from auth import AuthError, requires_auth
from app import create_app
#producer_token = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9SVEhYeDhhYjlkSTBCRjZCQUdVbCJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWFuay51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFiNTU4NjNmNjRkNGEwMDcyYWQ5OWQ0IiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFwaS8iLCJpYXQiOjE2Mzk0OTM5NjksImV4cCI6MTYzOTUwMTE2OSwiYXpwIjoiUDQ0UnRMSVhsZU1CMjFlcUpaR3plaU1lVWZZUm5yNU0iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.dnGISf81noWHeu0OG2OygkFp9Gd-W5ssq6_tiNQUX9myVx1LYTJx_aT74U4yWPgn3bAe3IPQ0xg39oZNfKsfSlfrtKypmCq25e74fxKxAIYXy4dbdKbQ2ZhS7vDqq4z9E0gBfm5m6lY030edw-UdlGYb_p-f1uHtNGk-nnT7l7Cu9YqatYq4lrRaYehxNIW3LlioJpMK5JLznVcKaYYer6poxUt3bxdQDYQ0FROnPDafqSNNv_HvW8SRRkpIRSJu136qIgwcMc7jsYgsyvjmZzNdNu-QDjB7cGa-9nHlOYkcHK9rM9-L3O5lwfI0KbxNeMMwQDwz7IcLcVFtPdPHHQ' 
producer_token =  str(os.getenv('executive_producer_token'))
#director_token = str(os.getenv('casting_director_token'))
assistant_token =  str(os.getenv('casting_assistant_token'))
#full_token =  'bearer ' + str(os.getenv('full_access_token'))

class CastingTestCase(unittest.TestCase):
    """This class represents the Casting test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("Test")
        self.client = self.app.test_client
    
    def tearDown(self):
        """Executed after reach test"""
        pass
   
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
