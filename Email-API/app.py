from flask import *
from flask_mail import Mail, Message
from celery import Celery
from flask_cors import CORS


app = Flask(__name__)
app.config['SECRET_KEY'] = 'IBDA3211-Sistem Terdistribusi-YehezkielPW-191900476'
CORS(app)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'mychicken.customerservice@gmail.com'
app.config['MAIL_PASSWORD'] = "mychickenisthebest123"
app.config['MAIL_DEFAULT_SENDER'] = "mychicken.customerservice@gmail.com"


# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://127.0.0.1:6379/0'


# Initialize extensions
mail = Mail(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def send_async_email(email_data):
    msg = Message(email_data["subject"], sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    with app.app_context():
        mail.send(msg)
        return "Async Email Sending Success"


@app.route('/send_mail', methods=["POST"])
def send_mail():
    email_data = request.json
    if email_data['key'] == "ibda3211-yehezkielpw":
        send_async_email.delay(email_data)
        return jsonify(status="success")
    else:
        return jsonify(status="failed")


if __name__ == '__main__':
    app.run(debug=True)
# {
#     "subject": "Tgas Sisbud",
#     "to": "ywijaya76@students.calvin.ac.id",
#     "body": "Success!",
#     "key": "ibda3211-yehezkielpw"
# }
