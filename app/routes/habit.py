from flask import Blueprint, request, jsonify
from ..models import db, Habit, Person
from datetime import time, datetime
habit_bp = Blueprint('habit_bp', __name__, url_prefix='/habits/')

@habit_bp.route('', methods=["POST"])
def createHabit():  
    try:
        data = request.get_json()
        name = data.get('name')
        time_iso = data.get('time')
        person_id = data.get('person_id') 
        description = data.get('description')
        ctime = time.fromisoformat(time_iso)
        


        if not name or not description or not person_id or not time_iso:
            return jsonify({
                "status": 400,
                "message": "Missing information in request body."
            }), 400
        if not ctime:
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
        
        habit = Habit(name=name, desc=description, time=ctime, person_id=person_id)
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
                'person_id': habit.person_id,
                'Created At': habit.created_at.isoformat()
            })

        return jsonify({
            'status': 200,
            'habits': result
        }), 200

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500
    
@habit_bp.route('/<int:habit_id>', methods=["GET"])
def getHabit(habit_id):
    try:
        habit = Habit.query.get_or_404(habit_id)
        return jsonify({
            'status': 200,
            'habit': {
                'id': habit.id,
                'name': habit.name,
                'time': time.isoformat(habit.time),
                'description': habit.desc,
                'person_id': habit.person_id
            }
        }), 200

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500
    
@habit_bp.route('/<int:habit_id>', methods=["DELETE"])
def deleteHabit(habit_id):
    try:
        habit = Habit.query.get_or_404(habit_id)
        db.session.delete(habit)
        db.session.commit()

        return jsonify({
            'status': 200,
            'message': 'Habit deleted successfully'
        }), 200

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500
    

@habit_bp.route('/<int:habit_id>', methods=["PATCH"])
def updateHabit(habit_id):
    try:
        data = request.get_json()
        habit = Habit.query.get_or_404(habit_id)

        name = data.get('name')
        time_iso = data.get('time')
        description = data.get('description')
        created_at = data.get('created_at')
        if created_at:
            habit.created_at = datetime.fromisoformat(created_at)
        if name:
            habit.name = name
        if time_iso:
            ctime = time.fromisoformat(time_iso)
            habit.time = ctime
        if description:
            habit.desc = description

        db.session.commit()

        return jsonify({
            'status': 200,
            'message': 'Habit updated successfully',
            'habit_id': habit.id
        }), 200

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500
    
@habit_bp.route('/<int:habit_id>/Do', methods=["PATCH"])
def increaseHabitStreak(habit_id):
    try:
        habit = Habit.query.get_or_404(habit_id)

        person = Person.query.get_or_404(habit.person_id)
        person.habits_completed_today += 1
        habit.current_streak += 1
        if habit.current_streak > habit.longest_streak:
            habit.longest_streak = habit.current_streak
        db.session.commit()

        return jsonify({
            'status': 200,
            'message': 'Habit streak increased successfully',
            'habit_id': habit.id,
            'current_streak': habit.current_streak,
            'longest_streak': habit.longest_streak
        }), 200

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500
    
@habit_bp.route('/<int:habit_id>/ResetStreak', methods=["PATCH"])
def resetHabitStreak(habit_id):
    try:
        habit = Habit.query.get_or_404(habit_id)
        habit.current_streak = 0
        db.session.commit()

        return jsonify({
            'status': 200,
            'message': 'Habit streak reset successfully',
            'habit_id': habit.id,
            'current_streak': habit.current_streak
        }), 200

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500