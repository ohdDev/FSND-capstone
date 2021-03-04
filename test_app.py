import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors, db
casting_assistant_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE3QlE1eFRTMlZTVXVfR1ZNU0RhUiJ9.eyJpc3MiOiJodHRwczovL2Rldi1vaG91ZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAxNjk4YTYzYjJkMzQwMDY5ZDEyOWY3IiwiYXVkIjoibW92aWUiLCJpYXQiOjE2MTQ5MDAxMDIsImV4cCI6MTYxNDkwNzMwMiwiYXpwIjoiek1LVEl6Zm4ySHV2c1BpVVJDaURGV2w5WHhtaWNYYWQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.UDQHP2LYaukzUH1QcjZbUAml5Xu0JjkRnyd88x70Eyr486pLZ7JRsVK9mYBOoXeXA9Ap2YhhOeYEYaPw5X3mQLD0ZaObE8fij1np1g1ps2kbhgNVFz8Exiz6t1IiA7EODwB_JiJoKkvyZxkE6yYE3nrQabM5FQwpC-i6Ot9QqY-K7nSh8Xv_rI8weErv0RT5cnO1nv69gRmjVgYNAOsZcZsSRb7UeSxNRGhb_FlhRThLz5Y_BD6EQelsXq0cZ7AJKqfxd-58qYdaLoSYV4Yf81bG5EyX5vT7JlVm14_QDi4HM6AMihzJm1tNobX_qsm2sm5zGkv8Of-x3gZzP8dpig'
casting_director_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE3QlE1eFRTMlZTVXVfR1ZNU0RhUiJ9.eyJpc3MiOiJodHRwczovL2Rldi1vaG91ZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAwNTVkZDcxMzA5ZTMwMDY5YzRhYmFjIiwiYXVkIjoibW92aWUiLCJpYXQiOjE2MTQ5MDAxOTAsImV4cCI6MTYxNDkwNzM5MCwiYXpwIjoiek1LVEl6Zm4ySHV2c1BpVVJDaURGV2w5WHhtaWNYYWQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.q7lInwr_ZU9wXe1u3g_YEQ_mhG0XO4qGZDuHmfkylUZwLoJEGzg9Snhy6Vgr53guQIDv4PWpKFWdQ_wsrs8EUl8-RjD08x-Mtc3CyTluXPxiGxuHMh9KlXpTb7NNH7_eSPepgtovGE0Nbx65lv0SMnJ_961eVHWpNSjAEcnM3qV3tRA3VOhs8n_21AzQPE6lwjMDK-Tzh4v8-uzBn46SNYjKDTYF5XKENKmf0qcR7UIAJItGxE_HgQsfRMIPZZCJY0-JodQE4gBvBLHv2v76GW3iF8s1gyGdBfmPi0ui7DZ2sbIbY1VV8ZdAbPSJv7iknn47NntayZ6YIS6zuhMSDQ'
casting_producer_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE3QlE1eFRTMlZTVXVfR1ZNU0RhUiJ9.eyJpc3MiOiJodHRwczovL2Rldi1vaG91ZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0MDIxNzFlYjRkNjAwMDcwZmY4OWIwIiwiYXVkIjoibW92aWUiLCJpYXQiOjE2MTQ4OTc4MDgsImV4cCI6MTYxNDkwNTAwOCwiYXpwIjoiek1LVEl6Zm4ySHV2c1BpVVJDaURGV2w5WHhtaWNYYWQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.NxXLmB4A1MGDbiNSH9Zt7shlqirt6y7jjxhpdMhrf1RS9UpOmb6_oZet5uRInbd2EJosBRL2wTyQ_DpQUvgw3OSLuH3OdsWk9j7xQHmNwe0M8msD2ERVHPPFOTXp0yRxS5Ey8yC-yH_jr5QVEd_e3uUGZQ-K9BhBtamCSBMlt2JATZjaO0i-BmKqeEBXKxQKUb8IBXMFs0svHimsnhoTW5OxAn8LzzBh8Z5Nzj0ubwYT5M-PKbSXTB_WTSDsrPWPaUdLmHQPTgCx7aaqVKDJHkG4y8_e0b6n43MeY9avttjYu34Nnlcxg3kPo2EKqaLMX41yiwiqoWrJotISIzmijg'



class AppTest(unittest.TestCase):
    """Setup test suite for the routes"""

    def setUp(self):
        """Setup application """
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castdb"
        self.database_path = 'postgresql://ohoud@localhost:5432/castdb'
        setup_db(self.app, self.database_path)


    def tearDown(self):
        """Executed after each test"""
        pass




    def test_create_new_actor(self):

        new_actor = {
            "name": "ohoud",
            "age": 25,
            "gender": "female"
        }
        res = self.client().post(
            '/actors',
            headers={"Authorization": " Bearer " + casting_producer_token},
            json=new_actor
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_400_post_actor(self):
        new_actor = {
            'name': 'actor1'
        }
        response = self.client().post(
            '/actors',
            headers={"Authorization": " Bearer " + casting_producer_token}, json=new_actor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "bad request")

    # create movies
    def test_create_new_movie(self):
        new_movie = {
            "name": "movie1",
            "release_date": "2021-02-01"
        }
        res = self.client().post(
            '/movies',
            headers={"Authorization": " Bearer " + casting_producer_token},
            json=new_movie
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_post_movie(self):
        new_movie = {
            'name': 'mov2'
        }
        response = self.client().post(
            '/movies',
            headers={"Authorization": " Bearer " + casting_producer_token}, json=new_movie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "bad request")

    # # get actors
    def test_get_actors(self):
        res = self.client().get('/actors', headers={
            'Authorization': " Bearer " + casting_assistant_token
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_404_sent_requesting_invalid_endopint_actors(self):
        res = self.client().get('/actors/var=33', json={'age': 33}, headers={
            'Authorization': " Bearer " + casting_assistant_token
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    # # get movies
    def test_get_movies(self):
        res = self.client().get('/movies', headers={
            'Authorization': " Bearer " + casting_assistant_token
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_404_sent_requesting_invalid_endopint_movies(self):
        res = self.client().get('/movies/var=33', json={'name': 'some'}, headers={
            'Authorization': " Bearer " + casting_assistant_token
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    # # edit actors
    def test_update_actor_name(self):
        res = self.client().patch('/actors/1', json={'name': 'ahmad'}, headers={
            'Authorization': " Bearer " + casting_producer_token
        })

        data = json.loads(res.data)
        actor = Actors.query.filter(Actors.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.format()['name'],'ahmad')

    def test_400_if_edit_actor_failed(self):
        res = self.client().patch('/actors/1', headers={
            'Authorization': " Bearer " + casting_producer_token
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # # edit movies
    def test_update_movie_name(self):
        res = self.client().patch('/movies/1', json={'name': 'mov-ed'}, headers={
            'Authorization': " Bearer " + casting_producer_token
        })

        data = json.loads(res.data)
        movie = Movies.query.filter(Movies.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.format()['name'],'mov-ed')

    def test_400_if_edit_movie_failed(self):
        res = self.client().patch('/movies/1', headers={
            'Authorization': " Bearer " + casting_producer_token
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


    # def test_delete_actor(self):
    #     res = self.client().delete('/actors/11', headers={
    #         'Authorization': " Bearer " + casting_director_token
    #     })
    #     data = json.loads(res.data)

    #     actor = Actors.query.filter(Actors.id == 11).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(actor, None)

    def test_422_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/500', headers={
            'Authorization': " Bearer " + casting_director_token
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # # delete movie
    # def test_delete_movie(self):
    #     res = self.client().delete('/movies/5', headers={
    #     'Authorization': " Bearer " + casting_producer_token
    #     })
    #     data = json.loads(res.data)

    #     movie = Movies.query.filter(Movies.id == 5).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(movie, None)

    def test_422_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/500', headers={
            'Authorization': " Bearer " + casting_producer_token
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()