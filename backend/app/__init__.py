from flask import Flask, request, jsonify
from flask_cors import CORS
from ariadne import graphql_sync, make_executable_schema, load_schema_from_path
from ariadne.explorer import ExplorerGraphiQL
from .models import db

from .resolvers import resolvers
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    type_defs = load_schema_from_path("app/schema.gql")
    schema = make_executable_schema(type_defs, resolvers)
    @app.route("/graphql", methods=["GET"])
    def graphql_playground():
        return ExplorerGraphiQL().html(None), 200


    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        data = request.get_json()
        success, result = graphql_sync(
            schema,
            data,
            context_value=request,
            debug=app.debug
        )
        return jsonify(result), 200 if success else 400
    
    db.init_app(app)

    with app.app_context():
        print("✅ Connecting to DB:", app.config["SQLALCHEMY_DATABASE_URI"])
        db.create_all()

    return app
