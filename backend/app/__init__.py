from flask import Flask
from app.extensions import mongo
from pymongo.errors import ConnectionFailure
from flask_cors import CORS
from app.webhook.routes import webhook
from app.healthcheck.routes import healthcheck
from app.pollDB.routes import pollDB

def create_app():

    app = Flask(__name__)
    CORS(app)
    
    app.config["MONGO_URI"] = "mongodb://localhost:27017/techstax_dev_assignment"

    mongo.init_app(app)

    # Checking if connection to MongoDB is successfull
    with app.app_context():
        try:
            mongo.cx.admin.command('ping')
            print("Successfully connected to MongoDB")
        except ConnectionFailure as e:
            print("Failed to connect to MongoDB:", str(e))
    

    app.register_blueprint(healthcheck)
    app.register_blueprint(webhook)
    app.register_blueprint(pollDB)
    
    return app
