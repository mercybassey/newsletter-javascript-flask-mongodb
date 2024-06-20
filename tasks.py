from flask_mail import Message
from app import app, mail, db, celery
from datetime import datetime

@celery.task(bind=True)
def send_emails(self, subscribers, title, body):
    with app.app_context():
        for subscriber in subscribers:
            try:
                print(f"Sending email to {subscriber['email']}")
                msg = Message(title, recipients=[subscriber['email']])
                msg.body = body
                mail.send(msg)
                db.deliveries.insert_one({
                    'email': subscriber['email'],
                    'title': title,
                    'body': body,
                    'delivered_at': datetime.utcnow()
                })
                print("Email sent")

            except Exception as e:
                print(f"Failed to send email to {subscriber['email']}: {str(e)}")

        return {'result': 'All emails sent'}
