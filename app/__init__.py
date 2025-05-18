from flask import Flask

def create_app():
    app = Flask(__name__)

    from .controller.helloworld_controller import helloworld_bp
    from .controller.chat_controller import chat_bp
    app.register_blueprint(helloworld_bp)
    app.register_blueprint(chat_bp)
    return app
