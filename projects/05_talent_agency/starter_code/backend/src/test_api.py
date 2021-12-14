import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import base64

from models import setup_db, db_drop_and_create_all, Actor, Movie 
from auth import AuthError, requires_auth
from app import create_app
#producer_token = 'bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9SVEhYeDhhYjlkSTBCRjZCQUdVbCJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWFuay51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFiNTMyYjBjNWEwOTgwMDZiZmU4MzA4IiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFwaS8iLCJpYXQiOjE2Mzk0ODY5MTIsImV4cCI6MTYzOTQ5NDExMiwiYXpwIjoiUDQ0UnRMSVhsZU1CMjFlcUpaR3plaU1lVWZZUm5yNU0iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwidXBkYXRlOmFjdG9yIiwidXBkYXRlOm1vdmllIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.vQ7RRk7aUtU55crJOwWHaitLogBCt9gmuVJ3tppyf8JQeyc8Uzy6sIxb_a8QYf64eVdz9G3HALYgh05AXVY3MRIZmyqX205ifJiUDLBRRXchPMPlKr-mDZLM4WGOslvWQcjviKbWO8QJqpxo7c05vJPzvXfVbi2_kPqQTY1EksEyJ9Z4qYepQhVIJjdSDEqTBO7qHAnxvB_WYDgtjPnB44g2ULZspDPZZMfgzK6lC2u1Po-Eij9tcGqgLtMchgaQGAyaWsqu_nG0ern-8Yqq05SLSh4cVOhHjd_bO8z08EDqxswY5K55M082opyc8DSuEVNrDfkznM0mLxtsG5E33Q'
#producer_token =  str(os.getenv('executive_producer_token'))
#director_token =  str(os.getenv('casting_director_token'))
#assistant_token =  str(os.getenv('casting_assistant_token'))
full_token = str(os.getenv('full_token'))
assistant_token = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9SVEhYeDhhYjlkSTBCRjZCQUdVbCJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWFuay51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFiNTU4NjNmNjRkNGEwMDcyYWQ5OWQ0IiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFwaS8iLCJpYXQiOjE2Mzk1MTk5NzcsImV4cCI6MTYzOTUyNzE3NywiYXpwIjoiUDQ0UnRMSVhsZU1CMjFlcUpaR3plaU1lVWZZUm5yNU0iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.VraIiFSIUtaY0aMpwTuxwogYmD1QQ74ly9TF-RskLhlnwqLnBDKl6-eclLBKUTpt7ZdhDGkXA8b_gVs7gUNuP_s6GE6EUGGdWuRioxnmK2n7ZVKPBjhNGOpFO0lt7TQYpHFX9AlxxghEXpp-GNx8LjYrwy6N9C4gT2yPTZZpyacqype_CBljYIglkyYlYcb2_EtkLglC8Da04tiMOfNCPytBmNfkmJXcWiM-DfvQ8hY49HnMC5c2SfaymXZB5HnjG6gWP80Xhq568wGCN7Ozd_bXVOFGcUstTwIRjra3oJFkt3VpZvFn8SXkbIPm99gUBRFfi-q1375gN22SbeHTnw'
director_token = producer_token = full_token
#print("Assistant_token", assistant_token)
#producer_token =  'bearer ' + str(os.getenv('full_access_token'))

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
    
    def test_add_actor(self):
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
        print("\nPassed GET actor #1 test with permissions of Casting Director")
    
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

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
