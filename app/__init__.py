from flask import Flask

def create_app():
    app = Flask(__name__)

    UPLOAD_FOLDER = 'Python/webapp/uploaded-files'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    ALLOWED_EXTENSIONS = {'txt', 'csv', 'doc', 'docx'}

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app