from flask import Blueprint, request, jsonify
from ..models import db, Person


person_bp = Blueprint('person_bp', __name__, url_prefix='/people/')


@person_bp.route('', methods=["POST"])
def createPerson():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return jsonify({
                "status": 400,
                "message": "Missing information in request body."
            }), 400

        person = Person(name=name, email=email)
        db.session.add(person)
        db.session.commit()

        return jsonify({
            'status': 201,
            'message': 'Person created successfully',
            'person_id': person.id
        }), 201

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500


@person_bp.route('', methods=["GET"])
def getPeople():
    try:
        people = Person.query.all()
        result = []
        for person in people:
            habits=[]
            for habit in person.habits:
                habits.append({
                    'id': habit.id,
                    'name': habit.name,
                    'time': str(habit.time),
                    'description': habit.desc
                })
            result.append({
                'id': person.id,
                'name': person.name,
                'email': person.email,
                'habits': habits,
                'habits_done_today': person.habits_done_today
            })

        return jsonify({
            'status': 200,
            'people': result
        }), 200

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500
    
@person_bp.route('/<int:person_id>', methods=["GET"])
def getPerson(person_id):
    try:
        person = Person.query.get_or_404(person_id)
        habits = []
        for habit in person.habits:
                habits.append({
                    'id': habit.id,
                    'name': habit.name,
                    'time': str(habit.time),
                    'description': habit.desc
                })
        return jsonify({
            'status': 200,
            'person': {
                'id': person.id,
                'name': person.name,
                'email': person.email,
                'habits': habits,
                'habits_done_today': person.habits_done_today
            }
        }), 200

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500
    

@person_bp.route('/<int:person_id>', methods=["DELETE"])
def deletePerson(person_id):
    try:
        person = Person.query.get_or_404(person_id)
        db.session.delete(person)
        db.session.commit()

        return jsonify({
            'status': 200,
            'message': 'Person deleted successfully'
        }), 200

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500
    
@person_bp.route('/<int:person_id>', methods=["PATCH"])
def updatePerson(person_id):
    try:
        data = request.get_json()
        person = Person.query.get_or_404(person_id)
        if 'name' in data:
            name = data.get('name')
        if 'email' in data:
            email = data.get('email')
        person.name = name
        person.email = email
        db.session.add(person)
        db.session.commit()

        return jsonify({
            'status': 200,
            'message': 'Person updated successfully',
            'person': {
                'id': person.id,
                'name': person.name,
                'email': person.email
            }
        }), 200

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500
    

@person_bp.route('/<int:person_id>/endDay', methods=["PATCH"])
def endDay(person_id):
    try:
        person = Person.query.get_or_404(person_id)

        person.habits_done_today = 0
        for habit in person.habits:
            if habit.done_today:
                
                if habit.current_streak < habit.longest_streak:
                    habit.longest_streak = habit.curent_streak
                habit.done_today = False
            else:
                habit.current_streak = 0
        db.session.commit()

        return jsonify({
            'status': 200,
            'message': 'Day ended successfully',
            'person_id': person.id
        }), 200

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500