from appsettings import Settings
import pyodbc
import copy

# Read dataset from table LastStatement_Accounts,

class ReceivedStatement:

    def __init__(self, ):
        self.settings = Settings()
        self.data = []
        self.load_data()
        return

    def _conn_str_(self, ):
        server = self.settings.get('sqlserver')
        database = self.settings.get('sqldb')
        driver = 'DRIVER={ODBC Driver 17 for SQL Server}'
        driver = driver + ';SERVER=' + server + ';DATABASE=' + database + ';'
        if self.settings.get('sql-trusted').lower() == 'y':
            driver = driver + 'Trusted_Connection=yes;'
        else:
            driver = driver + 'UID=' + self.settings.get('sql-user') + ';PWD='+ self.settings.get('sql-password')
        return driver

    def load_data(self):
        result = []
        conn = pyodbc.connect(self._conn_str_())
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
