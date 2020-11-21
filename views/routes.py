from flask import Blueprint, render_template, jsonify, redirect, request, g
from appsettings import Settings
from data import ReceivedStatement

view_routes = Blueprint('view_routes', __name__, static_folder='static', template_folder='templates')

@view_routes.route('/received-a-statement', methods=['GET'])
def route_received_a_statement():
    settings = Settings()
    #
    # Load Data
    #
    rs = ReceivedStatement()
    context = {
        'settings': settings.items,
        'auth': g.auth,
        'data': rs.data
    }

    return render_template('received-a-statement.html', context=context)

@view_routes.route('/received-a-statement/dl', methods=['GET'])
def route_received_a_statement_dl():
    import io
    import csv
    from flask import make_response

    settings = Settings()
    #
    # Load Data
    #
    rs = ReceivedStatement()
    csvdata = convert_to_csv(rs.data)
    si = io.StringIO()
    #
    cw = csv.writer(si)
    for row in csvdata:
        r = row[0] + ',' + row[1]
        cw.writerow(row)
    output = make_response(si.getvalue())
    output.headers['Content-Disposition'] = 'attachment; filename=received-a-statement.csv'
    output.headers['Content-type'] = 'text/csv'
    return output

def convert_to_csv(data):
    result = []
    result.append(["account", "name"])
    for d in data:
        a = [d['account'], d['name']]
        result.append(a)

    return result
