import unittest
from app import create_app, db
from app.models import User, Role

class UserModelCase(unittest.TestCase):

	def setUp(self):
		self.app = create_app('testing')
		# self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		Role.insert_roles()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_create_user(self):
		user = User(email="463216638@qq.com",
					username="19372300",
					password="111111",
					avatar_img='/static/assets/qq.jpg')
		self.assertEqual(user.email, "463216638@qq.com")

	def test_user_photo(self):
		user = User(email="463216638@qq.com",
					username="19372300",
					password="111111",
					avatar_img='/static/assets/qq.jpg')
		self.assertEqual(user.avatar_img, "/static/assets/qq.jpg")

	def test_user_about_me(self):
		user = User(email="463216638@qq.com",
					username="19372300",
					password="111111",
					avatar_img='/static/assets/qq.jpg')
		self.assertEqual(user.about_me, None)

if __name__ == '__main__':
	unittest.main()