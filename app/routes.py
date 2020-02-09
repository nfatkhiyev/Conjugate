import os
import json
from datetime import date
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

    current_date = date.today()

    matched_class = Classes.query.filter(Classes.class_name == class_name).filter(Classes.class_start_time == class_start_time).filter(Classes.class_end_time == class_end_time).filter(Classes.class_building == class_building).filter(Classes.class_room_number).all()
    if matched_class == None:
        new_class = Classes(class_name, class_start_time, class_end_time, class_building, class_room_number)
        db.session.add(new_class)
        db.session.flush()
        db.session.commit()
        db.session.expire(new_class)
        matched_class = Classes.query.order_by(Classes.class_id.desc()).first()

    class_id = matched_class.class_id
    homework = Homeworks(user_name, class_id, homework_title, homework_due_date, current_date.strftime(%d%m%y))

    db.session.add(homework)
    db.session.flush()
    db.session.commit()
    db.session.expire(homeowrk)

    return "homework added to db"

@app.route("/remove_homework")
def remove_homework():
    body = request.json
    homework_id = body['homework_id']
    user_name = body['user_name']

    homework = Homeworks.query.filter(Homeworks.user_name == user_name).filter(Homeworks.homework_id == homework_id).first()

    if homework == None:
        return "User not authorized to remove this homework"

    db.session.delete(homework)
    db.session.flush()
    db.session.commit()

    return "Homework has been deleted"

@app.route("/get_homework/<string:user_name>", methods=["POST"])
def get_homework(user_name):
    homeworks = Homeworks.query.filter_by(user_name=user_name).all()

    json = { "user_name":str(user_name) }

    count = 0
    for homework in homeworks:
        class_info = Classes.query.filter_by(class_id=homework.class_id).first()
        hw_json = { "homework_"+str(count): [{
                    "Title":str(homework.homework_title),
                    "Class":str(class_info.class_name),
                    "Due":str(homework.homework_due_date),
                    }]}
        json.update(hw_json)
        count+=count

    return json

@app.route("/check_homework/<int:date>")
def check_homework(date):
    class_name = body['class_name']
    class_start_time = body['class_start_time']
    class_end_time = body['class_end_time']
    class_building = body['class_building']
    class_room_number = body['class_room_number']
    get_class_id(class_name, class_start_time, class_end_time, class_building, class_room_number)
    matched_homeworks = Homeworks.query.filter(Homeworkds.class_id == class_id).filter(Homeworks.date_created == date).all()
    
    if matched_homeworks == None:
        json = {"created_assignments":str(0)}
        return json
        
    json = {"created_assignments":str(matched_homeworks.len())}

    return json


def get_class_id(class_name, class_start_time, class_end_time, class_building, class_room_number):
    matched_class = Classes.query.filter(Classes.class_name == class_name).filter(Classes.class_start_time == class_start_time).filter(Classes.class_end_time == class_end_time).filter(Classes.class_building == class_building).filter(Classes.class_room_number).first()
    class_id = matched_class.class_id
    return class_id
