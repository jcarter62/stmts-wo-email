import pyodbc
from appsettings import Settings
import copy

class SpCall:

    def __init__(self):
        self.settings = Settings()
        
