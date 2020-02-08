import os
from flask import request, jsonify
from app import app
import requests
import flask_migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

from ConjugateAPI.models import *

requests.packages.urllib3.disable_warnings()

@app.route("/add_homework", methods=["POST"])
def add_homework():
    body = request.json
    user_name = body['user_name']
    class_name = body['class_name']
    class_start_time = body['class_start_time']
    class_end_time = body['class_end_time']
    class_building = body['class_building']
    class_room_number = body['class_room_number']
    homework_title = body['homework_title']
    homework_due_date = body['homework_due_date']

    matched_class = Classes.query.filter(Classes.class_name == class_name).filter(Classes.class_start_time == class_start_time).filter(Classes.class_end_time == class_end_time).filter(Classes.class_building == class_building).filter(Classes.class_room_number).all()
    if matched_class = None:
        new_class = Classes(class_name, class_start_time, class_end_time, class_building, class_room_number)
        db.session.add(new_class)
        db.session.flush()
        db.session.commit()
        db.session.expire(new_class)
        matched_class = Classes.query.order_by(Classes.class_id.desc()).first()

    class_id = matched_class.class_id
    homework = Homeworks(user_name, class_id, homework_title, homework_due_date)

    db.session.add(homework)
    db.session.flush()
    db.session.commit()
    db.session.expire(homeowrk)

    return "homework added to db"
