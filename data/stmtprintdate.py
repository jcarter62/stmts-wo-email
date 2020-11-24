from appsettings import Settings
from .connection import Connection
import pyodbc
import copy


class StatementPrintDate:

    def __init__(self, ):
        self.settings = Settings()
        self.data = []
        self.load_data()
        return

    def load_data(self):
        result = []
        conn = pyodbc.connect(Connection().value())
        cursor = conn.cursor()
        cmd = """
            select top 1 
            b.statement_id, b.fromdate, b.todate, b.maildate, b.duedate
            from BillStatement b
            where printed = 1 and AccountID is null 
            order by maildate desc
        """
        try:
            for row in cursor.execute(cmd):
                rowdata = self._extract_row(row)
                record = {
                    'id': rowdata['statement_id'],
                    'from': rowdata['fromdate'],
                    'to': rowdata['todate'],
                    'maildate': rowdata['maildate'],
                    'duedate': rowdata['duedate']
                }
                result.append(record)
        except Exception as e:
            print(str(e))
        self.data = copy.deepcopy(result)
        return

    def _extract_row(self, row):
        r = {}
        i = 0
        for item in row.cursor_description:
            name = item[0]
            val = str(row[i])
            name = name.lower()
            i += 1
            r[name] = val
        return r
