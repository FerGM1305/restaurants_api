from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
import os


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import routes, models,database
        spec = routes.generate_openapi_spec(app)
        with open('api_documentation.json', 'w') as f:
            json.dump(spec, f, indent=4)
        #import_csv_to_db('data/restaurantes.csv')
        return app