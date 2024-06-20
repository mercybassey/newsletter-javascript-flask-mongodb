import os

class Config:
    CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'
    RESULT_BACKEND = 'mongodb://localhost:27017/celery_results'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '<your-gmail-username>@gmail.com'
    MAIL_PASSWORD = 'htue qczu rnxo codx'
    MAIL_DEFAULT_SENDER = '<your-gmail-username>@gmail.com'
    ALLOWED_IPS = ['127.0.0.1']
    MONGO_URI = 'mongodb://localhost:27017/newsletter'





