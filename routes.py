from flask import render_template, request, abort, jsonify
from app import app, db
from tasks import send_emails

@app.before_request
def limit_remote_addr():
    if 'X-Forwarded-For' in request.headers:
        remote_addr = request.headers['X-Forwarded-For'].split(',')[0]
    else:
        remote_addr = request.remote_addr
    
    if request.endpoint == 'admin' and remote_addr not in app.config['ALLOWED_IPS']:
        abort(403)

@app.route('/')
def home():
    return render_template('subscribe.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    first_name = request.form['firstname']
    last_name = request.form['lastname']
    email = request.form['email']

    if db.subscribers.find_one({'email': email}):
        return """
        <div class="response error">
            <span class="icon">&#x2716;</span> This email is already subscribed!
        </div>
        """, 409

    db.subscribers.insert_one({'firstname': first_name, 'lastname': last_name, 'email': email, 'subscribed': True})
    return """
    <div class="response success">
        <span class="icon">&#x2714;</span> Subscribed successfully!
    </div>
    """, 200

@app.route('/send-newsletters', methods=['POST'])
def send_newsletters():
    title = request.form['title']
    body = request.form['body']
    subscribers = list(db.subscribers.find({'subscribed': True}))

    for subscriber in subscribers:
        subscriber['_id'] = str(subscriber['_id'])

    send_emails.apply_async(args=[subscribers, title, body])
    return jsonify({'message': 'Emails are being sent!'}), 202







