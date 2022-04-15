from flask import Flask

def create_app():
    app = Flask(__name__)
    # key for cookie auth
    app.config['SECRET KEY'] = 'asdf'
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    return app

