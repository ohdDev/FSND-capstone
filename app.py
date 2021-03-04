import os
from flask import Flask, request, abort, jsonify
from models import setup_db, Movies, Actors
from flask_cors import CORS
from auth import AuthError, requires_auth
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    app=Flask(__name__)
    setup_db(app)
    CORS(app)


    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response


    @app.route('/')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"


    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
      
      actors = Actors.query.all()

      actors_format = [actor.format() for actor in actors]

      if len(actors_format) == 0:
            abort(404)
      else:
          return jsonify({
              'success':True,
              'actors': actors_format
          }),200



    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
      
      movies = Movies.query.all()
      movies_format = [movie.format() for movie in movies]

      if len(movies_format) == 0:
            abort(404)
      else:
          return jsonify({
              'success':True,
              'movies': movies_format
          }),200



    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def submit_actors(jwt):

      body = request.get_json()  

      new_name = body.get('name',None)
      new_age = body.get('age',None)
      new_gender = body.get('gender',None)

      if new_name is None or new_age is None or new_gender is None:
        abort(400)

      try:
        actors = Actors(name=new_name, age=new_age, gender=new_gender)
        actors.insert()

        return jsonify({
            'success':True,
            'actors':actors.format()
        }),200

      except:
        abort(422)


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def submit_movies(jwt):

      body = request.get_json()  

      new_name = body.get('name',None)
      new_release_date = body.get('release_date',None)

      if new_name is None or new_release_date  is None:
        abort(400)

      try:
        movies = Movies(name=new_name, release_date=new_release_date)
        movies.insert()

        return jsonify({
            'success':True,
            'movies':movies.format()
        }),200

      except:
        abort(422)


    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actors(token, id):

        try:
            body = request.get_json()
            actor = Actors.query.filter(Actors.id == id).one_or_none()

            if actor is None:
                abort(404)
            
            if 'name' in body:
                actor.name = body.get('name')
            if 'age' in body:
                actor.age = body.get('age')
            if 'gender' in body:
                actor.gender = body.get('gender')

            actor.update()


            return jsonify({
                'success':True,
                'actors': actor.format()
                }), 200

        except:
            abort(400)


    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movies(token, id):

        try:
            body = request.get_json()
            movie = Movies.query.filter(Movies.id == id).one_or_none()

            if movie is None:
                abort(404)
            
            if 'name' in body:
                movie.name = body.get('name')
            if 'release_date' in body:
                movie.release_date = body.get('release_date')

            movie.update()


            return jsonify({
                'success':True,
                'movies': movie.format()
                }), 200

        except:
            abort(400)



    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(token, id):
        
        try:
            actor = Actors.query.filter(Actors.id == id).one_or_none()

            if actor is None:
                abort(404)
            
            actor.delete()

            return jsonify({
                'success':True,
                'delete': id
            }), 200

        except:
            abort(422)


    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(token, id):
        
        try:
            movie = Movies.query.filter(Movies.id == id).one_or_none()

            if movie is None:
                abort(404)
            
            movie.delete()

            return jsonify({
                'success':True,
                'delete': id
            }), 200

        except:
            abort(422)


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                "success": False, 
                "error": 422,
                "message": "unprocessable"
                }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404


    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': "unauthorized"
        }), 401


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400


    @app.errorhandler(AuthError)
    def not_authenticated(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), 401


    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)