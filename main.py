from database import create_database, get_subscription, insert_email
from flask import Flask, request
from logger import logger
from scheduler import start_schedule, start_schedules

app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        form = request.form
        args = form.to_dict()
        if "email" not in args:
            return "Email not included in form", 400
        insert_email(**args)
        subscription = get_subscription(args["email"])
        start_schedule(subscription)
        return "Subscription created", 201
    return ""


if __name__ == "__main__":
    create_database()
    start_schedules()
    app.run()
