#!/usr/bin/python

from .pyTimerDb import pyTimerDb
from .commonFunctions import cf

class pyTimerSettings():
    data = None

    def __init__(self):
        if self.read():
            cf.print_v("We got some settings")
        else:
            cf.print_v("There is no settings")
        return None
    
    def is_settings(self):
        if (self.data==None or len(self.data)==0):
            return False
        else:
            return True
    
    def read(self):
        #reading settings from table
        db = pyTimerDb();
        self.data=db.read_settings();
        return self.is_settings();
    
    def save(self):
        db = pyTimerDb();
        
        if (self.data==None or len(self.data)==0):
            cf.print_v("no data to save");
            return 1
        else:
            cf.print_v("Saving data to the DB");
            return db.save_settings(self.data);