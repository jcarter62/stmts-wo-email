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
    my_logger = AppLog()
    serve(app, host='0.0.0.0', port=5000)
