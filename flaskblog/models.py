
from flask import jsonify

from flaskblog import db





class User(db.Model):

	id=db.Column(db.Integer,primary_key=True)
	public_id=db.Column(db.String(50),nullable=False)
	email=db.Column(db.String(50),nullable=False,unique=True)
	password=db.Column(db.String(60),nullable=False)

	role=db.Column(db.Boolean,default=False)
	articles=db.relationship("Article",backref="creator",lazy=True)

	def __str__(self):
		return f'the user is {self.email} with is of {self.public_id}'


	def objectData(self):
		user={}

		user["id"]=self.id
		user["public_id"]=self.public_id
		user["email"]=self.email
		user["password"]=self.password
		user["role"]=self.role

		return user

class Article(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	article_id=db.Column(db.String(50),nullable=False)
	title=db.Column(db.String(80),nullable=False)
	description=db.Column(db.Text,nullable=False)
	creator_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)


	def __str__(self):

		return f'the article id is {self.id}'

	def articleObject(self):
		article={}
		article[article_id]=self.article_id
		article[title]=article.title
		article[description]=article.description

		return article

	
