import flask
from flask import redirect, request, g
from flask_bootstrap import Bootstrap
from main import main_routes
from views import view_routes
from waitress import serve
from applog import AppLog

app = flask.Flask(__name__)
app.register_blueprint(main_routes, url_prefix='/main')
app.register_blueprint(view_routes, url_prefix='/views')
Bootstrap(app)


@app.before_request
def app_before_request():
    my_logger.log_request(request)
    auth = {'authenticated': False, 'user': False, 'admin': False, 'name': ''}
    #
    g.auth = auth


@app.after_request
def after_request_func(response):
    return response


@app.route('/')
def hello_world():
    return redirect('/main')


my_logger = None

if __name__ == '__main__':
    import os

    my_logger = AppLog()

    hostIP = os.environ.get('APP_HOST')
    if hostIP == None:
        hostIP = '0.0.0.0'
    portNum = os.environ.get('APP_PORT')
    if portNum == None:
        portNum = 5000

    serve(app, host=hostIP, port=portNum)
