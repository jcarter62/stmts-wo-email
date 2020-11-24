from flask import Blueprint, render_template, jsonify, redirect, request, g
from appsettings import Settings
from data import ReceivedStatement, CustNoEmail, CustomerHasEmail, CustomerViewStatus

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


@view_routes.route('/statement-no-email', methods=['GET'])
def route_statement_no_email():
    settings = Settings()
    #
    # Load Data
    #
    rs = CustNoEmail()
    context = {
        'settings': settings.items,
        'auth': g.auth,
        'data': rs.data
    }

    return render_template('statement-no-email.html', context=context)


@view_routes.route('/statement-no-email/dl', methods=['GET'])
def route_statement_no_email_dl():
    import io
    import csv
    from flask import make_response

    settings = Settings()
    #
    # Load Data
    #
    rs = CustNoEmail()
    csvdata = convert_to_csv(rs.data)
    si = io.StringIO()
    #
    cw = csv.writer(si)
    for row in csvdata:
        r = row[0] + ',' + row[1]
        cw.writerow(row)
    output = make_response(si.getvalue())
    output.headers['Content-Disposition'] = 'attachment; filename=statement-no-email.csv'
    output.headers['Content-type'] = 'text/csv'
    return output


@view_routes.route('/customer-has-email', methods=['GET'])
def route_customer_has_email():
    settings = Settings()
    #
    # Load Data
    #
    rs = CustomerHasEmail()
    context = {
        'settings': settings.items,
        'auth': g.auth,
        'data': rs.data
    }
    return render_template('customer-has-email.html', context=context)


@view_routes.route('/customer-has-email/dl', methods=['GET'])
def route_customer_has_email_dl():
    import io
    import csv
    from flask import make_response

    settings = Settings()
    #
    # Load Data
    #
    rs = CustomerHasEmail()
    csvdata = convert_to_csv(rs.data)
    si = io.StringIO()
    #
    cw = csv.writer(si)
    for row in csvdata:
        r = row[0] + ',' + row[1]
        cw.writerow(row)
    output = make_response(si.getvalue())
    output.headers['Content-Disposition'] = 'attachment; filename=customer-has-email.csv'
    output.headers['Content-type'] = 'text/csv'
    return output


@view_routes.route('/customer-view-status', methods=['GET'])
def route_customer_view_status():
    settings = Settings()
    #
    # Load Data
    #
    rs = CustomerViewStatus()
    context = {
        'settings': settings.items,
        'auth': g.auth,
        'data': rs.data
    }
    return render_template('customer-view-status.html', context=context)




def convert_to_csv(data):
    result = []
    result.append(["account", "name"])
    for d in data:
        a = [d['account'], d['name']]
        result.append(a)

    return result
