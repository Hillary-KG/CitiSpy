import pyrebase
import firebase_admin
import datetime
import json
import pytz

from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import db
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone



# firebase_app = pyrebase.initialize_app(firebase_config)

# auth = firebase_app.auth()


# print(firebase_app)

# from firebase_admin import auth
# default_app =  firebase_admin.initialize_app()
# user = auth.get_user_by_email("rexwaki@gmail.com")
# print("user", user.uid)

# print("default app", default_app.name)


firebase_admin.initialize_app(cred, {
    'databaseURL': "https://citispy-91191.firebaseio.com"
})

def config():

    # firebase_admin.initialize_app(cred, {
    #     'databaseURL': "https://citispy-91191.firebaseio.com"
    # })

    db_ref = db.reference("7x1vUPvBtFNszHvmKHcI")
    alerts_ref = db_ref.child('alerts')

    mytz = pytz.timezone('Africa/Nairobi')
    nai = {
        "alert_1":
            {
                'location': [-1.286389, 36.817223],
                'raiser': None,
                'reveiver': None,
                'severity': "Bad",
                'status': "pending",
                'time_stamp': json.dumps(datetime.datetime.now(tz=pytz.timezone('Africa/Nairobi')),sort_keys=True, indent=1,cls=DjangoJSONEncoder),
                'title': 'Testing One'
            },
            "alert_2":
            {
                'location': [-1.286389, 36.817224],
                'raiser': None,
                'reveiver': None,
                'severity': "Bad",
                'status': "pending",
                'time_stamp': json.dumps(datetime.datetime.now(tz=pytz.timezone('Africa/Nairobi')),sort_keys=True, indent=1,cls=DjangoJSONEncoder),
                'title': 'Testing Two'
            },
            "alert_3":
            {
                'location': [-1.286389, 36.817225],
                'raiser': None,
                'reveiver': None,
                'severity': "Not Bad",
                'status': "pending",
                'time_stamp': json.dumps(datetime.datetime.now(tz=pytz.timezone('Africa/Nairobi')),sort_keys=True, indent=1,cls=DjangoJSONEncoder),
                'title': 'Testing Three'
            }
            
    }
    alerts_ref.set(nai)
    return True

#     print("db ref", alerts_ref.get('alert'))

# # from firebase_admin import auth

# user = auth.get_user_by_email(email)
# print('Successfully fetched user data: {0}'.format(user.uid))


def get_alerts():
    ALERT_CONTAINER = []

    db_ref = db.reference("7x1vUPvBtFNszHvmKHcI")
    alerts_ref = db_ref.child('alerts')

    print("db ref", alerts_ref.get())
    for alert in alerts_ref.get().items():
        ALERT_CONTAINER.append(json.dumps(alert))


    return ALERT_CONTAINER

    
# if __name__ == "__main__":
#     config()
#     print("Alerts", get_alerts())