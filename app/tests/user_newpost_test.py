import unittest
from app import create_app, db
from app.models import User, Role


class PostCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        # self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_new_post(self):
        # 注册新账户
        response = self.client.post('/auth/register', data={
            'user_name': "19372020",
            'email': "463216638@qq.com",
            'pwd': "111111",
            'confirm_pwd': '111111'
        })
        self.assertEqual(response.status_code, 302)
        # 使用新注册的账户登录
        response = self.client.post('/auth/login', data={
            'user': "463216638@qq.com",
            'pwd': "111111"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # 发送确认令牌
        user = User.query.filter_by(email="463216638@qq.com").first()
        token = user.generate_confirmation_token()
        response = self.client.get('/auth/confirm/{}'.format(token), follow_redirects=True)
        user.confirm(token)
        self.assertEqual(response.status_code, 200)

    def test_logout_user(self):
        # 注册新账户
        response = self.client.post('/auth/register', data={
            'user_name': "19372020",
            'email': "463216638@qq.com",
            'pwd': "111111",
            'confirm_pwd': '111111'
        })
        self.assertEqual(response.status_code, 302)
        # 使用新注册的账户登录
        response = self.client.post('/auth/login', data={
            'user': "463216638@qq.com",
            'pwd': "111111"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # 发送确认令牌
        user = User.query.filter_by(email="463216638@qq.com").first()
        token = user.generate_confirmation_token()
        response = self.client.get('/auth/confirm/{}'.format(token), follow_redirects=True)
        user.confirm(token)
        self.assertEqual(response.status_code, 200)

        self.assertIsNotNone(user)
        # 发一篇文章
        # 获取csrf_token
        # r=requests.get(base_url+)
        response = self.client.post('/new_post_md', data={
            'title': "TitleTest",
            'type': "testType",
            'body': "122",
            'test-editormd-html-code': '<p>122</p>'})
        self.assertEqual(response.status_code, 302)



if __name__ == '__main__':
    unittest.main()
