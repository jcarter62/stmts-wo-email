from appsettings import Settings
from .connection import Connection
import pyodbc
import copy


class CustomerHasEmail:

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
            select la.* from LastStatement_Accounts la
            left join 
                (select x.name_id from LastStatement_Accounts x
                 left join LastStatement_Email e on x.name_id = e.name_id
                 where e.name_id is null) ne 
                 on la.name_id = ne.name_id 
            where ne.name_id is null
            order by la.name_id;
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
        cursor.close()
        conn.close()
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
