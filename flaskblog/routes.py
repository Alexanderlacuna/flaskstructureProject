import jwt

import datetime
from functools import wraps

from flask import jsonify,request

from   flaskblog import app,db

from flaskblog.models import User,Article

from werkzeug.security import generate_password_hash,check_password_hash
import uuid


def user_exists(id):
	user=User.query.filter_by(public_id=id).first()

	if user:
		return user

	if user is None:


		return None


	


def register_user(email,password):

	uid=str(uuid.uuid4())
	new_user=User(public_id=uid,email=email,password=password)



	try:

		db.session.add(new_user)
		db.session.commit()

	except:
		return jsonify({"message":"Creating a new user failed"}),401


	


def generate_password(password):
	return generate_password_hash(password,"sha256")
def token_required(f):
	@wraps(f)
	def inner_function(*args,**kwargs):

		token=request.args.get("token")

		if (token is None):
			return jsonify({"message":"Error occurred"}),401

		try:

			user=jwt.decode(token,"secret")
			

		except:
			return jsonify({"message":"Error2 occurred"}),401

		return f(user["data"],*args,**kwargs)

	return inner_function




@app.route("/")
@token_required
def home(user):
	return jsonify({"message":user})



@app.route("/signup",methods=["POST"])
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


	

	






		





	
@app.route("/signin/<name>")
def signin(name):
	return "This is the signnin page"

@app.route("/login",methods=["POST","GET"])
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

@app.route("/deleteUser",methods=["DELETE"])
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
	

@app.route("/promoteUser",methods=["PUT"])
def promote():
	data=request.get_json()
	id=data["id"]
	user=user_exists(id)

	if user:
		user.role=True
		db.session.commit()

		return jsonify({"message":"successfully promoted user"}),200

	return jsonify({"message":"user not found"}),401


	

	

# @app.route()
# get all users 
@app.route("/getAllUser",methods=["GET"])
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



# create article
@app.route("/createArticle",methods=["POST"])
@token_required
def createArticle(user):

	data=request.get_json()
	title=data["title"]
	description=data["description"]


	article_id=str(uuid.uuid4())
	newArticle=Article(article_id,title,description,creator_id=user.public_id)

	try:
		

		db.session.add(newArticle)
		db.session.commit()
	except:
		return jsonify({"message":"user could not be created"}),401

	return jsonify({"message":"Article successfully created"}),201

@app.route("/getAllArticles",methods=["GET"])
def getArticles():

	articlesList=[]


	articles=Article.query.all()

	if len(articles)<1:
		return jsonify({"message":"no article exists"})
	try:
		for article in articles:
			modifiedArticle=article.articleObject()
			articlesList.append(modifiedArticle)

	except:
		return jsonify({"message":"articles  were not found"}),401


	return jsonify({articles:articlesList})

@app.route("/getOneArticle/<id>",methods=["GET"])
def getArticle(id):
	try:
		article=Article.query.filter_by(article_id=id).first()

		if article is None:
			return jsonify({"message":"Article does not exists"}),401

		modifiedArticle=article.articleObject()


	except:
		return jsonify({"message":"Article could not be found"})

	return jsonify({"article":article})

@app.route("/deleteArticle/<id>",methods=["GET"])
@token_required
def deleteArticle(user,id):

	try:
		article=Article.query.filter_by(article_id=id).first()

		if article is None:
			return jsonify({"message":"Article does exists"})
	except:
		return jsonify({"message":"article not found"}),401

	if  (article.creator_id == user.public_id):
		db.session.delete(article)
		db.session.commit()

		return jsonify({"message":"article successfully deleted"}),200


	return jsonify({"message":"Action is forbidden"}),403


@app.errorhandler(404)
def not_found(e):
	return jsonify({"message":"the resource could not be found"}),404

@app.errorhandler(500)
def server_error(e):
	return jsonify({"message":"a server error occurred"}),500




	# check if article exists








	
	
	



