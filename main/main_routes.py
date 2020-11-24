from flask import Blueprint, render_template, jsonify, redirect, request, g
from appsettings import Settings
from data import StatementPrintDate

main_routes = Blueprint('main_routes', __name__, static_folder='static', template_folder='templates')

@main_routes.route('/', methods=['GET'])
def main_root():
    settings = Settings()
    spd = StatementPrintDate()
    spd_data = spd.data[0]['maildate']
    context = {
        'settings': settings.items,
        'auth': g.auth,
        'statement_print_date': spd_data
    }
    return render_template('main.html', context=context)

@main_routes.route('/about', methods=['GET'])
def main_about():
    settings = Settings()
    context = {
        'settings': settings.items,
        'auth': g.auth
    }
    return render_template('about.html', context=context)
