from appsettings import Settings


class Connection:

    def __init__(self,):
        self.settings = Settings()
        return

    def value(self,):
        server = self.settings.get('sqlserver')
        database = self.settings.get('sqldb')
        driver = 'DRIVER={ODBC Driver 17 for SQL Server}'
        driver = driver + ';SERVER=' + server + ';DATABASE=' + database + ';'
        if self.settings.get('sql-trusted').lower() == 'y':
            driver = driver + 'Trusted_Connection=yes;'
        else:
            driver = driver + 'UID=' + self.settings.get('sql-user') + ';PWD='+ self.settings.get('sql-password')
        return driver

