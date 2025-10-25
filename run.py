from app import create_app
from app.models import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = create_app()
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)