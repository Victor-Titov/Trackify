from flask import Blueprint, request, jsonify
from ..models import db, Leaderboard, Person

leaderboard_bp = Blueprint('leaderboard_bp', __name__, url_prefix='/leaderboards/')
@leaderboard_bp.route('', methods=["POST"])
def createLeaderboard():
    try:
        data = request.get_json()
        name = data.get('name')

        if not name:
            return jsonify({
                "status": 400,
                "message": "Missing information in request body."
            }), 400

        leaderboard = Leaderboard(name=name)
        db.session.add(leaderboard)
        db.session.commit()

        return jsonify({
            'status': 201,
            'message': 'Leaderboard created successfully',
            'leaderboard_id': leaderboard.id
        }), 201

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500
    
@leaderboard_bp.route('', methods=["GET"])
def getLeaderboards():
    try:
        leaderboards = Leaderboard.query.all()
        result = []
        for leaderboard in leaderboards:
            participants = [{'id': p.id, 'name': p.name} for p in leaderboard.participants]
            result.append({
                'id': leaderboard.id,
                'name': leaderboard.name,
                'last_updated': str(leaderboard.last_updated),
                'participants': participants
            })

        return jsonify({
            'status': 200,
            'leaderboards': result
        }), 200

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500
    
@leaderboard_bp.route('/<int:leaderboard_id>', methods=["GET"])
def getLeaderboard(leaderboard_id):
    try:
        leaderboard = Leaderboard.query.get_or_404(leaderboard_id)
        participants = [{'id': p.id, 'name': p.name} for p in leaderboard.participants]
        
        result = {
            'id': leaderboard.id,
            'name': leaderboard.name,
            'last_updated': str(leaderboard.last_updated),
            'participants': participants
        }

        return jsonify({
            'status': 200,
            'leaderboard': result
        }), 200

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500
    
@leaderboard_bp.route('/<int:leaderboard_id>', methods=["DELETE"])
def deleteLeaderboard(leaderboard_id):
    try:
        leaderboard = Leaderboard.query.get_or_404(leaderboard_id)
        db.session.delete(leaderboard)
        db.session.commit()

        return jsonify({
            'status': 200,
            'message': 'Leaderboard deleted successfully'
        }), 200

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500



@leaderboard_bp.route('/<int:leaderboard_id>', methods=["PATCH"])
def updateLeaderboard(leaderboard_id):
    try:
        data = request.get_json()
        name = data.get('name')


        leaderboard = Leaderboard.query.get_or_404(leaderboard_id)

        if name:
            leaderboard.name = name
        

        db.session.commit()

        return jsonify({
            'status': 200,
            'message': 'Leaderboard updated successfully'
        }), 200

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500

@leaderboard_bp.route('/<int:leaderboard_id>/participants', methods=["POST"])
def addParticipant(leaderboard_id):
    try:
        data = request.get_json()
        person_id = data.get('person_id')

        if not person_id:
            return jsonify({
                "status": 400,
                "message": "Missing person_id in request body."
            }), 400

        leaderboard = Leaderboard.query.get_or_404(leaderboard_id)
        person = Person.query.get_or_404(person_id)

        if person in leaderboard.participants:
            return jsonify({
                "status": 400,
                "message": "Person already a participant in this leaderboard."
            }), 400

        leaderboard.participants.append(person)
        person.leaderboards.append(leaderboard)
        db.session.commit()

        return jsonify({
            'status': 200,
            'message': 'Participant added successfully'
        }), 200

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500
    

@leaderboard_bp.route('/<int:leaderboard_id>/participants/<int:person_id>', methods=["DELETE"])
def removeParticipant(leaderboard_id, person_id):
    try:
        leaderboard = Leaderboard.query.get_or_404(leaderboard_id)
        person = Person.query.get_or_404(person_id)

        if person not in leaderboard.participants:
            return jsonify({
                "status": 400,
                "message": "Person not a participant in this leaderboard."
            }), 400

        leaderboard.participants.remove(person)
        person.leaderboards.remove(leaderboard)
        db.session.commit()

        return jsonify({
            'status': 200,
            'message': 'Participant removed successfully'
        }), 200

    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)}), 500
    
