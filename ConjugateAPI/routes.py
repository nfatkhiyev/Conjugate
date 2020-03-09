import os
import json
from datetime import date, datetime
from flask import request, jsonify
from ConjugateAPI import app
import requests
import flask_migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user

db = SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

from ConjugateAPI.models import Classes, Homeworks, User
from ConjugateAPI.auth import is_user_authenticated

requests.packages.urllib3.disable_warnings()


@app.route("/add_homework", methods=["POST"])
def add_homework():
    if is_user_authenticated():
        body = request.json
        user_email = body["user_email"]
        class_name = body["class_name"]
        class_start_time = body["class_start_time"]
        class_end_time = body["class_end_time"]
        class_building = body["class_building"]
        class_room_number = body["class_room_number"]
        homework_title = body["homework_title"]
        homework_due_date = body["homework_due_date"]

        if current_user.email == user_email:

            # pass without slashes. ex. yyyymmdd
            current_date = date.today()
            # due_date = homework_due_date
            # due_date = datetime(year=int(due_date[0:4]), month=int(due_date[4:6]), day=int(due_date[6:8]))
            matched_class = (
                Classes.query.filter(Classes.class_name == class_name)
                .filter(Classes.class_start_time == class_start_time)
                .filter(Classes.class_end_time == class_end_time)
                .filter(Classes.class_building == class_building)
                .filter(Classes.class_room_number == class_room_number)
                .first()
            )
            print(matched_class)

            if matched_class == None or matched_class == []:
                new_class = Classes(
                    class_name,
                    class_start_time,
                    class_end_time,
                    class_building,
                    class_room_number,
                )
                db.session.add(new_class)
                db.session.flush()
                db.session.commit()
                db.session.expire(new_class)
                matched_class = Classes.query.order_by(Classes.class_id.desc()).first()

            class_id = matched_class.class_id
            homework = Homeworks(
                user_email, class_id, homework_title, homework_due_date, current_date
            )

            db.session.add(homework)
            db.session.flush()
            db.session.commit()
            db.session.expire(homework)

            homework_id = (
                Homeworks.query.order_by(Homeworks.homeworks_id.desc())
                .first()
                .homeworks_id
            )

            return_json = {"homeworks_id": str(homework_id)}

            return return_json, 200

        return "you are not the correct user", 403

    return "User not logged in", 403


@app.route("/remove_homework")
def remove_homework():
    body = request.json
    homeworks_id = body["homework_id"]
    user_email = body["user_email"]

    homework = (
        Homeworks.query.filter(Homeworks.user_email == user_email)
        .filter(Homeworks.homeworks_id == homeworks_id)
        .first()
    )

    if homework == None:
        return "User not authorized to remove this homework", 403

    db.session.delete(homework)
    db.session.flush()
    db.session.commit()

    return "Homework has been deleted", 200


@app.route("/get_homework/<string:user_email>")
def get_homework(user_email):
    if is_user_authenticated():
        homeworks = Homeworks.query.filter_by(user_email=user_email).all()

        json = {"user_name": str(current_user.user_name)}

        count = 0
        for homework in homeworks:
            class_info = Classes.query.filter_by(class_id=homework.class_id).first()
            hw_json = {
                "homework_"
                + str(count): [
                    {
                        "homeworks_id": str(homework.homeworks_id),
                        "Title": str(homework.homework_title),
                        "Class": str(class_info.class_name),
                        "Due": homework.homework_due_date.strftime("%d/%m/%y"),
                    }
                ]
            }
            json.update(hw_json)
            count += count

        return json, 200
    return "Not logged in", 403


@app.route("/check_homework/<int:date>")
def check_homework(date):
    body = request.json
    class_name = body["class_name"]
    class_start_time = body["class_start_time"]
    class_end_time = body["class_end_time"]
    class_building = body["class_building"]
    class_room_number = body["class_room_number"]

    date = str(date)
    date = datetime(year=int(date[0:4]), month=int(date[4:6]), day=int(date[6:8]))

    class_id = get_class_id(
        class_name, class_start_time, class_end_time, class_building, class_room_number
    )
    matched_homeworks = (
        Homeworks.query.filter(Homeworks.class_id == class_id)
        .filter(Homeworks.date_created == date)
        .all()
    )

    if matched_homeworks == None:
        json = {"created_assignments": str(0)}
        return json, 200

    json = {"created_assignments": str(matched_homeworks.len())}

    return json, 200


def get_class_id(
    class_name, class_start_time, class_end_time, class_building, class_room_number
):
    matched_class = (
        Classes.query.filter(Classes.class_name == class_name)
        .filter(Classes.class_start_time == class_start_time)
        .filter(Classes.class_end_time == class_end_time)
        .filter(Classes.class_building == class_building)
        .filter(Classes.class_room_number)
        .first()
    )

    class_id = matched_class.class_id
    return class_id
