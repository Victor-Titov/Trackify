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
