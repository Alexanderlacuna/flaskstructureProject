# hash password functions

from functools import wraps


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

