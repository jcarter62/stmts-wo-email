from appsettings import Settings
from .connection import Connection
import pyodbc
import copy


class ReceivedStatement:

    def __init__(self, ):
        self.settings = Settings()
        self.data = []
        self.load_data()
        return

    def load_data(self):
        result = []
        conn = pyodbc.connect(Connection().value())
        cursor = conn.cursor()
        cmd = 'select name_id, fullname from LastStatement_Accounts order by name_id'
        try:
            for row in cursor.execute(cmd):
                rowdata = self._extract_row(row)
                record = {
                    'account': rowdata['name_id'],
                    'name': rowdata['fullname']
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
