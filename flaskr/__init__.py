from flask import Flask

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)

    from . import main
    app.register_blueprint(main.bp)

    return app
