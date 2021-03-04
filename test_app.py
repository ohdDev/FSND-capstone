import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors, db
casting_assistant_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE3QlE1eFRTMlZTVXVfR1ZNU0RhUiJ9.eyJpc3MiOiJodHRwczovL2Rldi1vaG91ZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAxNjk4YTYzYjJkMzQwMDY5ZDEyOWY3IiwiYXVkIjoibW92aWUiLCJpYXQiOjE2MTQ4OTA0MjYsImV4cCI6MTYxNDg5NzYyNiwiYXpwIjoiek1LVEl6Zm4ySHV2c1BpVVJDaURGV2w5WHhtaWNYYWQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.gYdHVFLJxoTcF8B_xff2EfROM-84CZPJkNJ23l7QhQNzbFqpj4CY-zvuBZTBvO9n0Ff68HiX8WyjYN_hjJAyOKNjyiMIL3b_hm5uTx_j9MWBORKoOIv9cysbGpVzPCLT8A4f5dsuzNyZNdUJSbwiGOqQhO2VhlWZPY1OITDhdY9U1n3EV7qb-XGVmLP4uwBhSVaJdoDNIVrRoNyYSpzGmYW6KLY8EO-O0eRb0Y_Ian7jl0DV53XqL0NROALtGRjoHLz3dJP7YJCJA3rjRvyijv84qLJwqHUDWm2bOqBJCK5L9wYvD7bqd5IFgbt_z3fIPXhLtaCSocS9uFjhvEebJg'
casting_director_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE3QlE1eFRTMlZTVXVfR1ZNU0RhUiJ9.eyJpc3MiOiJodHRwczovL2Rldi1vaG91ZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAwNTVkZDcxMzA5ZTMwMDY5YzRhYmFjIiwiYXVkIjoibW92aWUiLCJpYXQiOjE2MTQ3OTY2ODcsImV4cCI6MTYxNDgwMzg4NywiYXpwIjoiek1LVEl6Zm4ySHV2c1BpVVJDaURGV2w5WHhtaWNYYWQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.WMgHCNMtQXi5GI11sgReP3KzMmF3vYTPsckA7HQmtq4QwKpeNOZzrm5v8PAIms2lGj5n5V_pYWxwtKYyjxOUtUB4eJ5Faf2TWALbsoKJ7dC4y81L7v4uQ1baSliP-3cRbGMMMfugA2qcschxAMdZ8dtz4dQIthT1cdQqYinW7MoQeX2TrQeOfxl0qLOEnxx0caijpKHx-ubPCTTrzW65cqr0dq88MDFhwj6NrSeBR-G5gjFSfB4_mr-zXk7j0jvJV5BGACJ9MKXfERJXofFjWaYsATbl9l4KJ9rkl_-PGpBY-0oWymF3WUI6g1ocFqicu63pb8LlDKhEYlH-yTvQyQ'
casting_producer_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkE3QlE1eFRTMlZTVXVfR1ZNU0RhUiJ9.eyJpc3MiOiJodHRwczovL2Rldi1vaG91ZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0MDIxNzFlYjRkNjAwMDcwZmY4OWIwIiwiYXVkIjoibW92aWUiLCJpYXQiOjE2MTQ4ODU5ODgsImV4cCI6MTYxNDg5MzE4OCwiYXpwIjoiek1LVEl6Zm4ySHV2c1BpVVJDaURGV2w5WHhtaWNYYWQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.QQlBskUlHR8fDFk0uMpvdulEysRQBBdIc4hAIOhW5nib4YiEBX0Qb2KAskhlmH29onPMjeEO-QuGeZVa3XBOoZ1tWVNMsyQL5y_8Zzh7a87-dsnLIAkIKXakSfgNew07npTGXpL0VlGt0qSwrArpt3YJbH8MVZN5bj2ylSpthISWFw-pijh6FwSwMenmvAy6hRhSIm7a5hizPEtXoVCgNi6y3Es1Xwa1M7vel5x2fNXKQ54DAK9wAqCCboCJ_55832S7pe7twmYAQ2I9tYyre9CJdtoIUxqDMEtBG0z0Zkg9Ltiv9gFucSs3GflgMpAxFKxOf4a-i2zjtdZNYD3XWg'



class AppTest(unittest.TestCase):
    """Setup test suite for the routes"""

    def setUp(self):
        """Setup application """
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = 'postgresql://ohoud@localhost:5432/capstone_test'
        setup_db(self.app, self.database_path)


    def tearDown(self):
        """Executed after each test"""
        pass


    def test_get_all_actors(self):
        response = self.client().get(
            '/actors',
            headers={"Authorization": " Bearer " + casting_assistant_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


    # def test_create_new_actor(self):

    #     new_actor = {
    #         "name": "ohoud",
    #         "age": 25,
    #         "gender": "female"
    #     }
    #     res = self.client().post(
    #         '/actors',
    #         headers={"Authorization": " Bearer " + casting_producer_token},
    #         json=new_actor
    #     )
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_405_if_actor_creation_not_allowed(self):
    #     res = self.client().post('/actors/150', json=self.new_actor, headers={
    #         'Authorization': "Bearer {}".format(self.casting_producer_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'method not allowed')

    # # create movies
    # def test_create_new_movie(self):
    #     res = self.client().post('/movies', json=self.new_movie, headers={
    #         'Authorization': "Bearer {}".format(self.casting_producer_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['movies']))

    # def test_405_if_movie_creation_not_allowed(self):
    #     res = self.client().post('/movies', json=self.new_movie, headers={
    #         'Authorization': "Bearer {}".format(self.casting_producer_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'method not allowed')

    # # get actors
    # def test_get_actors(self):
    #     res = self.client().get('/actors', headers={
    #         'Authorization': "Bearer {}".format(self.casting_assistant_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['actors']))

    # def test_404_sent_requesting_invalid_endopint_actors(self):
    #     res = self.client().get('/actors', json={'age': 33}, headers={
    #         'Authorization': "Bearer {}".format(self.casting_assistant_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], 'resource not found')

    # # get movies
    # def test_get_movies(self):
    #     res = self.client().get('/movies', headers={
    #         'Authorization': "Bearer {}".format(self.casting_assistant_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['movies']))

    # def test_404_sent_requesting_invalid_endopint_movies(self):
    #     res = self.client().get('/movies', json={'name': "movie-ex"}, headers={
    #         'Authorization': "Bearer {}".format(self.casting_assistant_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], 'resource not found')

    # # edit actors
    # def test_update_actor_name(self):
    #     res = self.client().patch('/actors/1', json={'name': 'ahmad'}, headers={
    #         'Authorization': "Bearer {}".format(self.casting_producer_token)
    #     })

    #     data = json.loads(res.data)
    #     actor = Actors.query.filter(Actors.id == 1).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(actor.format()['name'],'ahmad')

    # def test_400_if_edit_actor_failed(self):
    #     res = self.client().patch('/actors/1', headers={
    #         'Authorization': "Bearer {}".format(self.casting_producer_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'bad request')

    # # edit movies
    # def test_update_movie_name(self):
    #     res = self.client().patch('/movies/1', json={'name': 'movie-edit'}, headers={
    #         'Authorization': "Bearer {}".format(self.casting_producer_token)
    #     })

    #     data = json.loads(res.data)
    #     movie = Movies.query.filter(Movies.id == 1).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(movie.format()['name'], 'movie-edit')

    # def test_400_if_edit_movie_failed(self):
    #     res = self.client().patch('/movies/1', headers={
    #         'Authorization': "Bearer {}".format(self.casting_producer_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()