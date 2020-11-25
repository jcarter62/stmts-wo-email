from flask import Blueprint, render_template, jsonify, redirect, request, g
from appsettings import Settings
from data import StatementPrintDate, SWE_Process
import arrow

main_routes = Blueprint('main_routes', __name__, static_folder='static', template_folder='templates')

@main_routes.route('/', methods=['GET'])
def main_root():
    settings = Settings()
    spd = StatementPrintDate()
    spd_maildate = spd.maildate_str
    swe = SWE_Process()
    process_date = swe.process_date_str
    btn_txt = 'Process Not Recommended'
    btn_type = 'btn-primary'
    if swe.process_date < spd.maildate:
        btn_txt = 'Process Recommended'
        btn_type = 'btn-danger'


    context = {
        'settings': settings.items,
        'auth': g.auth,
        'statement_print_date': spd_maildate,
        'swe_process': process_date,
        'process_button_txt': btn_txt,
        'process_button_type': btn_type,
        'database_info': settings.get('sqldb'),
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

@main_routes.route('/process_data', methods=['POST'])
def main_process_post():
    swe = SWE_Process()
    swe.process_data()
    return redirect('/')

