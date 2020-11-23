from appsettings import Settings
import pyodbc
import copy
from .connection import Connection


# Read dataset from query:
#     select la.name_id as account, la.fullname as name
#     from LastStatement_Accounts la
#     left join LastStatement_Email e on la.name_id = e.name_id
#     where e.name_id is null
#     order by la.name_id

class CustNoEmail:

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
            select la.name_id, la.fullname
            from LastStatement_Accounts la
            left join LastStatement_Email e on la.name_id = e.name_id
            where e.name_id is null
            order by la.name_id
        """
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
