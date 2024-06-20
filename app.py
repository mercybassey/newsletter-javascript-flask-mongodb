from flask import Flask
from flask_mail import Mail
from pymongo import MongoClient
from celery import Celery

app = Flask(__name__)
app.config.from_object('config.Config')

mail = Mail(app)
client = MongoClient(app.config['MONGO_URI'])
db = client.get_database()

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from routes import *
from tasks import *

if __name__ == '__main__':
    app.run(debug=True)
