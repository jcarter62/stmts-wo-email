from appsettings import Settings
from .connection import Connection
import pyodbc
import copy
import arrow


class SWE_Process:

    def __init__(self, ):
        self.settings = Settings()
        self.process_date = None
        self.exists = self._check_exist_()
        if self.exists == False:
            self.create_swe_process()
        self.process_date = arrow.get(self.get_process_date())
        self.process_date_str = self.process_date.format(fmt='MM/DD/YYYY')
        return

    #
    # Determine if table exists
    #
    def _check_exist_(self):
        exists = False
        conn = pyodbc.connect(Connection().value())
        cursor = conn.cursor()
        cmd = "select * from sys.all_objects where name = 'swe_process';"
        rows = 0
        try:
            for row in cursor.execute(cmd):
                rows = rows + 1
        except Exception as e:
            print(str(e))
        if rows > 0:
            exists = True
        cursor.close()
        conn.close()
        return exists

    def get_process_date(self):
        conn = pyodbc.connect(Connection().value())
        cursor = conn.cursor()
        cmd = 'select top 1 process_date from swe_process order by process_date desc;'
        try:
            for row in cursor.execute(cmd):
                rowdata = self._extract_row(row)
                process_date = rowdata['process_date']
        except Exception as e:
            print(str(e))
        cursor.close()
        conn.close()
        return process_date

    def create_swe_process(self,):
        conn = pyodbc.connect(Connection().value())
        cursor = conn.cursor()
        cmd = """
            create table swe_process ( process_date datetime null );
            insert into swe_process (process_date) values ('1/1/1900');
        """
        cursor.execute(cmd)
        conn.commit()
        cursor.close()
        conn.close()
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
