import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate

from db import db
import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

from blocklist import BLOCKLIST

from flask_jwt_extended import JWTManager

def create_app(db_URL=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_URL or os.getenv("DATABASE_URL", "sqlite:///data.db")
    # This is something related to sqlalchemy that slow down the process and no needed so it is false
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    api = Api(app)

    migrate=Migrate(app,db)

    app.config["JWT_SECRET_KEY"]="279953559713017948055185980331502847475"
    jwt=JWTManager(app)

    @jwt.token_in_blocklist_loader
    def ckeck_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header,jwt_payload):
        return (
            jsonify({"description":"the token has been removed"})
        )


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return(
            jsonify({"Message":"The token has expired"}),401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({"Message": "Invalid token"}), 401
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({"Message": "Request doesn't include any access token."}), 401
        )

    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app

create_app()