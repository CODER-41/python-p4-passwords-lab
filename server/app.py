#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username']
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()

        # Save user ID in session
        session['user_id'] = user.id


        return user.to_dict(), 201

class CheckSession(Resource):

    def get(self):
        # Check if user_id exists in session
        user_id = session.get('user_id')

        if user_id:
            user = db.session.get(User, user_id)
            if user:
                return user.to_dict(), 200
        
        # Return empty response with 204 if not authenticated
        return {}, 204
    # pass

class Login(Resource):
    def post(self):
        json = request.get_json()
        username = json.get('username')
        password = json.get('password')

        #Find user by username
        user = User.query.filter_by(username=username).first()

        #Verify user exists and password is correct
        if user and user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        
        return {'error': 'Invalid username or password'}, 401

    # pass

class Logout(Resource):

    def delete(self):
        # Remove user_id from session
        session.pop('user_id', None) 
        return {}, 204

 
    # pass

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')





if __name__ == '__main__':
    app.run(port=5555, debug=True)
