import unittest
from App import app
import json 
# import firebase_admin
# from firebase_admin import auth
# from firebase_admin import credentials
# from firebase_admin import firestore

# cred = credentials.Certificate('parkflask-firebase-adminsdk-wplsp-87a9bb6106.json')
# firebase_admin.initialize_app(cred)

# db = firestore.client()


class TestHello(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_homePage(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status, '200 OK')


    def test_login(self):
        taster = app.test_client(self)
        print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        rv = taster.post('/login' , data=dict(email="mor0981@gmail.com",password="123456"),follow_redirects=True)
        rv = taster.get('/login',follow_redirects=True)
        self.assertTrue('משתמשים'.encode() in rv.data)
        rv= taster.get('/logout',follow_redirects=True)

if __name__ == '__main__':
    unittest.main()