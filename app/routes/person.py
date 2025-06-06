from flask import Blueprint, request, jsonify
from ..models import db, Person
from datetime import datetime

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
            result.append({
                'id': person.id,
                'name': person.name,
                'email': person.email
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
        return jsonify({
            'status': 200,
            'person': {
                'id': person.id,
                'name': person.name,
                'email': person.email
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