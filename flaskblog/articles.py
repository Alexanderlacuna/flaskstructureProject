
import jwt

import datetime
from functools import wraps

from flask import jsonify,request,Blueprint

from   flaskblog import app,db

from flaskblog.models import User,Article

from flaskblog.utils import *


import uuid


articleBlueprint=Blueprint("articleBlueprint",__name__)



@articleBlueprint.route("/testRoute")
def test():
	return "loud and clear"



@articleBlueprint.route("/createArticle",methods=["POST"])
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

@articleBlueprint.route("/getAllArticles",methods=["GET"])
def getArticles():

	articlesList=[]


	articles=Article.query.all()

	print(f'the length off articles is  {len(articles)}')

	if len(articles)<1:

		print("failed")
		return jsonify({"message":"no article exists"})
	try:
		for article in articles:
			modifiedArticle=article.articleObject()
			articlesList.append(modifiedArticle)

	except:
		return jsonify({"message":"articles  were not found"}),401


	return jsonify({articles:articlesList})

@articleBlueprint.route("/getOneArticle/<id>",methods=["GET"])
def getArticle(id):
	try:
		article=Article.query.filter_by(article_id=id).first()

		if article is None:
			return jsonify({"message":"Article does not exists"}),401

		modifiedArticle=article.articleObject()


	except:
		return jsonify({"message":"Article could not be found"})

	return jsonify({"article":article})

@articleBlueprint.route("/deleteArticle/<id>",methods=["DELETE"])
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
