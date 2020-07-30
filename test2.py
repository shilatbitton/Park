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
    #User login with correct details
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_homePage(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status, '200 OK')

    

    def test_login_logout(self):
        taster = app.test_client(self)
        rv = taster.post('/login' , data=dict(email="mor0981@gmail.com",password="123456"),follow_redirects=True)
        self.assertTrue(rv.status, '200 OK')
        self.assertTrue('ברוכים'.encode() in rv.data)
        rv= taster.get('/logout',follow_redirects=True)
        self.assertTrue('התנתקת בהצלחה'.encode() in rv.data)

    def test_login_session(self):
        taster = app.test_client(self)
        rv = taster.post('/login' , data=dict(email="mor0981@gmail.com",password="123456"),follow_redirects=True)
        rv = taster.get('/login',follow_redirects=True)
        self.assertTrue('ברוכים'.encode() in rv.data)
        rv= taster.get('/logout',follow_redirects=True)

    def test_delete_user(self):
        taster = app.test_client(self)
        rv = taster.post('/register' , data=dict(email="test@gmail.com",password="123456",name="test",last="test"),follow_redirects=True)
        rv = taster.post('/login' , data=dict(email="test@gmail.com",password="123456"),follow_redirects=True)
        self.assertTrue('ברוכים'.encode() in rv.data)
        rv = taster.post('/unregister' , data=dict(email="test@gmail.com",password="123456"),follow_redirects=True)
        rv = taster.post('/login' , data=dict(email="test@gmail.com",password="123456"),follow_redirects=True)
        self.assertTrue('שם משתמש או סיסמא לא נכונים'.encode() in rv.data)

    def test_comment(self):
        taster = app.test_client(self)
        rv = taster.post('/register' , data=dict(email="test2@gmail.com",password="123456",name="test",last="test"),follow_redirects=True)
        rv = taster.post('/login' , data=dict(email="test2@gmail.com",password="123456"),follow_redirects=True)
        rv = taster.post('/comments/פארק%20ליכטנשטיין',data=dict(comment="test"),follow_redirects=True)
        rv = taster.get('/comments/פארק%20ליכטנשטיין')
        self.assertTrue('test'.encode() in rv.data)
        rv = taster.post('/unregister',data=dict(email="test2@gmail.com",password="123456"),follow_redirects=True)

    def test_jasonPark_show(self):
        taster = app.test_client(self)
        with open('playgrounds.json', 'r',encoding="utf8") as myfile:
            arr=[]
            data=json.loads(myfile.read())
        arr.append(data[0]['Name'])
        rv = taster.post('/login' , data=dict(email="mor0981@gmail.com",password="123456"),follow_redirects=True)
        rv = taster.get('/parks')
        for p in arr:
            self.assertTrue(p.encode() in rv.data)


    def test_login_as_admin(self):
        taster = app.test_client(self)
        print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        rv = taster.post('/login' , data=dict(email="mor0981@gmail.com",password="123456"),follow_redirects=True)
        rv = taster.get('/login',follow_redirects=True)
        self.assertTrue('משתמשים'.encode() in rv.data)
        rv= taster.get('/logout',follow_redirects=True)

    def test_login_as_visit(self):
        taster = app.test_client(self)
        rv = taster.post('/login' , data=dict(email="dani@gmail.com",password="123456"),follow_redirects=True)
        rv = taster.get('/login',follow_redirects=True)
        self.assertFalse('משתמשים'.encode() in rv.data)
        rv= taster.get('/logout',follow_redirects=True)

    
    def test_add_admin(self):
        taster = app.test_client(self)
        rv = taster.post('/login' , data=dict(email="mor0981@gmail.com",password="123456"),follow_redirects=True)
        rv = taster.get('/login',follow_redirects=True)
        rv = taster.post('/registerByAdmin' , data=dict(name="טסט",last="טסט",email="test3@gmail.com",password="123456",Admin=True),follow_redirects=True)
        rv= taster.get('/logout',follow_redirects=True)
        rv = taster.post('/login' , data=dict(email="test3@gmail.com",password="123456"),follow_redirects=True)
        self.assertTrue('ברוכים'.encode() in rv.data)
        rv = taster.post('/unregister',data=dict(email="test3@gmail.com",password="123456"),follow_redirects=True)

        

    # def delet_comment(self):
    #     taster = app.test_client(self)
    #     rv = taster.post('/register' , data=dict(email="test3@gmail.com",password="123456",name="test",last="test"),follow_redirects=True)
    #     rv = taster.post('/login' , data=dict(email="test3@gmail.com",password="123456"),follow_redirects=True)
    #     rv = taster.post('/comments/פארק%20ליכטנשטיין',data=dict(comment="test"),follow_redirects=True)
    #     rv = taster.get('/comments/פארק%20ליכטנשטיין')
    #     self.assertTrue('test'.encode() in rv.data)

    
        

         
        
    # def test_correct(self):
    #     try:
    #         auth.sign_in_with_email_and_password("mor0981@gmail.com","123456")
    #         self.assertTrue(True)
    #     except:
    #         self.assertTrue(False)
    # #User login with incorrect details
    
    # def test_incorrect(self):
    #     try:
    #         auth.sign_in_with_email_and_password("mor081@gmail.com","12661266")
    #         self.assertTrue(False)
    #     except:
    #         self.assertTrue(True)
    


if __name__ == '__main__':
    unittest.main()