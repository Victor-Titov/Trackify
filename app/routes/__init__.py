from .person import person_bp


def register_routes(app):
        app.register_blueprint(person_bp)