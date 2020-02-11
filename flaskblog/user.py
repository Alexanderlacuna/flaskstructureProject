import jwt

import datetime
from functools import wraps

from flask import jsonify,request,Blueprint

from   flaskblog import app,db

# from flaskblog import create_app as app

from flaskblog.models import User,Article

from werkzeug.security import generate_password_hash,check_password_hash
import uuid


# from flaskblog.utils import token_required

from flaskblog.utils import *


userBlueprint=Blueprint("userBlueprint",__name__)






@userBlueprint.route("/")
@token_required
def home(user):
	return jsonify({"message":user})



@userBlueprint.route("/signup",methods=["POST"])
def signup():

	data=request.get_json()





	try:

		# also try to validate the password  use decorator
		email=data["email"]
		password=data["password"]



	except:

		return jsonify({"message":"email and password required"}),401


	user=User.query.filter_by(email=email).first()

	if user is None:
		password=generate_password(password)
		register_user(email,password)
		return f'the password is {password}'


	return jsonify({"message" :"User already exists"})


	

	






		





	
@userBlueprint.route("/signin/<name>")
def signin(name):
	return "This is the signnin page"

@userBlueprint.route("/login",methods=["POST","GET"])
def login():

	# expect json data

	data=request.get_json()



	email=data["email"]
	password=data["password"]

	user=User.query.filter_by(email=email).first()


	if not user:
		return jsonify({"message":"user does exists"}),401
		
	validity=check_password_hash(user.password,password)

	if(validity==False):

		return jsonify({"message":"error1 in user or password"}), 401




	try:
		token=jwt.encode({"data":"alexis",
			"exp":datetime.datetime.utcnow()+datetime.timedelta(seconds=60)
			},"secret",).decode("utf-8")
	except:
		return jsonify({"message":"error in token"}), 401


	return jsonify({
		"token":token
		})

# delete user 

@userBlueprint.route("/deleteUser",methods=["DELETE"])
def delUser():

	data=request.get_json()

	id=data["id"]
	

	try:
		user=user_exists(id)
		db.session.delete(user)
		db.session.commit()

	except:
		return jsonify({"message":"edwfwf"}),401

	return jsonify({"message":"successfully deleted user"}),200




	# check if user exists
	

@userBlueprint.route("/promoteUser",methods=["PUT"])
def promote():
	data=request.get_json()
	id=data["id"]
	user=user_exists(id)

	if user:
		user.role=True
		db.session.commit()

		return jsonify({"message":"successfully promoted user"}),200

	return jsonify({"message":"user not found"}),401


	

	

# @userBlueprint.route()
# get all users 
@userBlueprint.route("/getAllUser",methods=["GET"])
def getUsers():

	user_lists=[]
	users=User.query.all()
	try:
		for user in users:
			new_user=user.objectData()
			user_lists.append(new_user)
		
	except:
		return jsonify({"message":"an error occurred"}),401

		# print(new_user)
		

	return jsonify({"users":user_lists}),200



@app.route("/getSpecificUser/<string:id>",methods=["GET"])
def getOneUser(id):

	user=user_exists(id)

	if  user:


		user_to_return=user.objectData()

		return jsonify(user_to_return),200


	return jsonify({"message":"user does not exists"})
	# return(user_to_return)