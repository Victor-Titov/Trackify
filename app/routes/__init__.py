from .person import person_bp
from .habit import habit_bp
from .leaderboard import leaderboard_bp
def register_routes(app):
        app.register_blueprint(person_bp)
        app.register_blueprint(habit_bp)
        app.register_blueprint(leaderboard_bp)
