from flask import Blueprint, request, jsonify
from ..models import db, Habit, Person
from datetime import time
habit_bp = Blueprint('habit_bp', __name__, url_prefix='/habits/')

@habit_bp.route('', methods=["POST"])
def createHabit():  
    try:
        data = request.get_json()
        name = data.get('name')
        time_iso = data.get('time')
        person_id = data.get('person_id') 
        description = data.get('description')
        dtime = time.fromisoformat(time_iso)
        


        if not name or not description or not person_id or not time_iso:
            return jsonify({
                "status": 400,
                "message": "Missing information in request body."
            }), 400
        if not dtime:
            return jsonify({
                "status": 400,
                "message": "Invalid time format."
            }), 400
        person = Person.query.get(person_id)

        if not person:
            return jsonify({
                "status": 404,
                "message": "Person not found."
            }), 404
        
        habit = Habit(name=name, desc=description, time=dtime, person_id=person_id)
        person.habits.append(habit)

        db.session.add(habit)
        person.habits.append(habit)
        db.session.commit()

        return jsonify({
            'status': 201,
            'message': 'Habit created successfully',
            'habit_id': habit.id
        }), 201
    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500


@habit_bp.route('', methods=["GET"])
def getHabits():
    try:
        habits = Habit.query.all()
        result = []
        for habit in habits:
            result.append({
                'id': habit.id,
                'name': habit.name,
                'time': time.isoformat(habit.time),
                'description': habit.desc,
                'person_id': habit.person_id
            })

        return jsonify({
            'status': 200,
            'habits': result
        }), 200

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500