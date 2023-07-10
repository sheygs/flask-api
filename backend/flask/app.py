
import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# load env variables from .env file
load_dotenv('./dev.env')

app = Flask(__name__)

CORS(app)

BASE_URL=os.environ.get('BASE_URL')


@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        'code': 200,
        'status': 'success',
        'message': 'okay',
        'data': None
    })

@app.route('/users', methods=['POST'])
def create_user():
    """
    Get request body
    Parse request body to json
    Make http request
    if status code is 201, return record
    otherwise, return error code

    """
    endpoint  = f'{BASE_URL}/users'

    try:

      # retrieve the json data from the request body
      data = request.json

      response = requests.post(endpoint, json=data)

      print(response.status_code, response.ok)

      if response.status_code == 201:
        response = response.json()

        # print(response)

        return jsonify({'code': 201, 'status': 'success', 'message': 'user created', 'data': response}), 201
      else:
        return jsonify({'code': 400, 'status': 'failure', 'message': 'Failed to create user', 'data': None}), 400

    except Exception as e:
         #print(e)
     return jsonify({'code': '500', 'status': 'failure', 'message': f'{str(e)}', 'data': None})


@app.route('/users', methods=['GET'])
def read_users():
    """
    - Make a call to get users
    - if result is empty, return response
    - if result is not empty, return result
    - handle exceptions
    """

    endpoint = f'{BASE_URL}/users'

    try:

      response = requests.get(endpoint)
      # print('response', response.headers)

      if response.status_code == 200:
        users = response.json()

        # print('users: ', len(users))

        if len(users) > 0:
            return jsonify({'code': 200, 'status': 'success', 'message': 'users retrieved', 'data': users}), 200
        else:
            return jsonify({'code': 200, 'status': 'success', 'message': 'No record exists', 'data': None}), 200
      else:
        return  jsonify({'code': int(f'{response.status_code}'), 'status': 'failure', 'message': 'An error occured', 'data': None}), 200


    except Exception as e:
         print(e)
    return  jsonify({'code': 500, 'status': 'failure', 'message': f'{str(e)}', 'data': None}), 500


def is_valid_user_id(user_id):
    if isinstance(user_id, str) and user_id.isdigit():
       return True
    else:
       return False


@app.route('/users/<user_id>', methods=['GET'])
def read_user(user_id):
    """
     validate user_id
     make http request
     Return response for valid API request,
     otherwise, return error
    """

    if not is_valid_user_id(user_id):
      return jsonify({'code': 400, 'status': 'failure', 'message': 'Invalid user_id', 'data': None}), 400

    endpoint = f'{BASE_URL}/users/{user_id}'

    try:
       response = requests.get(endpoint)

       if response.ok == True or response.status_code == 200:
          response = response.json()

          return jsonify({'code': 200, 'status': 'success', 'message': 'user retrieved', 'data': response}), 200
       else:
         return jsonify({'code': 404, 'status': 'failure', 'message': 'user not found', 'data': None}), 404

    except Exception as e:
        return jsonify({'code': 500, 'status': 'failure', 'message': f'{str(e)}', 'data': None}), 500


@app.route('/users/<user_id>', methods=['PATCH'])
def update_user(user_id):
    """
     validate user_id
     pass req.body to update
     make http request
     Return response for valid API request,
     otherwise, return error
    """

    if not is_valid_user_id(user_id):
       return jsonify({'code': 400, 'status': 'failure', 'message': 'Invalid user_id', 'data': None}), 400

    try:

     endpoint = f'{BASE_URL}/users/{user_id}'

     data = request.json # parse body requests to json

     response = requests.patch(endpoint, json=data)

     # print(response.ok)

     if response.ok == True or response.status_code == 200:

        resource = response.json()

        # print(resource)

        return jsonify({'code': 200, 'status': 'success', 'message': 'user updated', 'data': resource}), 200
     else:
        return jsonify({'code': 404, 'status': 'failure', 'message': 'user not found', 'data': None}), 404

    except Exception as e:
      return jsonify({'code': 500, 'status': 'failure', 'message': f'{str(e)}', 'data': None}), 500



@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
     validate user_id
     make http request
     Return response for valid API request,
     otherwise, return error
    """
    if not is_valid_user_id(user_id):
      return jsonify({'code': 400, 'status': 'failure', 'message': 'Invalid user_id', 'data': None}), 400

    try:

      endpoint=f'{BASE_URL}/users/{user_id}'

      response = requests.delete(endpoint)

      print(response)

      if response.ok == True or response.status_code == 200:
        return jsonify({'code': 200, 'status': 'success', 'message': 'user deleted', 'data': None}), 200

      else:
        return jsonify({'code': 404, 'status': 'failure', 'message': 'user not found', 'data': None}), 404

    except Exception as e:
         return jsonify({'code': 500, 'status': 'failure', 'message': f'{str(e)}', 'data': None}), 500



if __name__ == '__main__':
    app.run(debug=True)

