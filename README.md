## Capston Full Stack project

### Description
this project is about casting agency models a company that is responsible for creating movies and managing and assigning actors to those movies.
**URL where the application is hosted:**
- https://castingapp.herokuapp.com/

### Install dependencies

```
pip install -r requirements.txt

```

**Capstone project contains:**

- Models:
    - Movies with attributes title and release date
    - Actors with attributes name, age and gender

- Endpoints:
    - GET /actors and /movies
    - DELETE /actors/ and /movies/
    - POST /actors and /movies 
    - PATCH /actors/ and /movies/
    
- Roles for authorization:
    - Casting Assistant
        - Can view actors and movies
            - user account:
                - as-user@assistant.com
                - password!123


    - Casting Director
        - All permissions a Casting Assistant has
        - Add or delete an actor from the database
        - Modify actors or movies
            - user account:
                    - dir-user@director.com
                    - password!123
    - Executive Producer
        - All permissions a Casting Director has
        - Add or delete a movie from the database
            - user account:
                    - examplemail@example.com
                    - password!123
    
    **to create new tokens use the following url, and sign in with previous accounts**
    - ` https://dev-ohoud.us.auth0.com/authorize?audience=movie&response_type=token&client_id=zMKTIzfn2HuvsPiURCiDFWl9XxmicXad&redirect_uri=http://127.0.0.1:8100/tabs/user-page
`

- Tests:
    - One test for success behavior of each endpoint
    - One test for error behavior of each endpoint
    - tests of RBAC for each role



### Error handling:
the API returns errors as json object for example:

```
{
    "success": False, 
    "error": 404,
    "message": "resource not found"
}

```
the errors that handeling by the api:
- 422 , unprocessable
- 404 , resource not found
- 401 , unauthorized
- 400 , bad request
- 401 , not authenticated

### Endpoints:
**GET /actors**
- description
    - returnes list of actors, with success message
    - ` curl https://castingapp.herokuapp.com/actors `

    ```
    {
    "actors": [
        {
            "age": 33,
            "gender": "f",
            "id": 4,
            "name": "oh"
        },
        {
            "age": 33,
            "gender": "f",
            "id": 1,
            "name": "oh-2-edit"
        }
    ],
    "success": true
    }

    ```


**POST /actors**
- description
    - create new actor and return it, with success message
    - ` curl https://castingapp.herokuapp.com/actors -X POST -H "Content-Type: application/json" -d '{"name":"noora","age":33,"gender":"female"}' `

    ```
    {
    "actors": {
        "age": 33,
        "gender": "female",
        "id": 7,
        "name": "noora"
    },
    "success": true
    }

    ```


**POST /movies**
- description
    - create new movie and return it, with success message
    - ` curl https://castingapp.herokuapp.com/movies -X POST -H "Content-Type: application/json" -d '{"name":"movie-ex","release_date":"2018-03-29T13:34:00.000"}' `

    ```
    {
    "movies": {
        "id": 4,
        "name": "movie-ex",
        "release_date": "Thu, 29 Mar 2018 00:00:00 GMT"
    },
    "success": true
    }

    ```

**PATCH /actors/{id}**
- description
    - update specific actor and return it, with success message
    - ` curl https://castingapp.herokuapp.com/actors/7 -X PATCH -H "Content-Type: application/json" -d '{"name":"nadia"}' `

    ```
    {
    "actors": {
        "age": 33,
        "gender": "female",
        "id": 7,
        "name": "nadia"
    },
    "success": true
    }

    ```


**PATCH /movies/{id}**
- description
    - update specific movie and return it, with success message
    - ` curl https://castingapp.herokuapp.com/movies/7 -X PATCH -H "Content-Type: application/json" -d '{"name":"movie-edit"}' `

    ```
    {
    "movies": {
        "id": 4,
        "name": "movie-edit",
        "release_date": "Thu, 29 Mar 2018 00:00:00 GMT"
    },
    "success": true
    }

    ```

**DELETE /actors/{id}**
- description
    - delete specific actor and return its id, with success message
    - ` curl -X DELETE https://castingapp.herokuapp.com/actors/7 `

    ```
    {
    "delete": 7,
    "success": true
    }

    ```

**DELETE /movies/{id}**
- description
    - delete specific movie and return its id, with success message
    - ` curl -X DELETE https://castingapp.herokuapp.com/movies/4 `

    ```
    {
    "delete": 4,
    "success": true
    }

    ```
