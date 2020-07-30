import pyrebase


config={
  "apiKey": "AIzaSyDab7tKKm11tgRuLsAPejXGGAYJ1d20cnQ",
  "authDomain": "parkflask.firebaseapp.com",
  "databaseURL": "https://parkflask.firebaseio.com",
  "projectId": "parkflask",
  "storageBucket": "parkflask.appspot.com",
  "messagingSenderId": "685599054335",
  "appId": "1:685599054335:web:db2d1d2890588a14772fca",
  "measurementId": "G-H8HGMEE4WB"
}

firebase = pyrebase.initialize_app(config)
auth= firebase.auth()

def Test_Correctdata():
    try:
        auth.sign_in_with_email_and_password("mor0981@gmail.com","12661266")
        return True
    except:
        return False

def Test_NotCorrectdata():
    try:
        auth.sign_in_with_email_and_password("mor01@gmail.com","12661266")
        return True
    except:
        return False



Test_Correctdata()
Test_NotCorrectdata()



