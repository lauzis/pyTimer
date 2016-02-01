#!/usr/bin/python
import sqlite3
from .commonFunctions import cf
from .apiModel import apiModel
class pyTimerDb():
    db_name = "pyTimer.dbo"
    conn=""
    def __init__(self):
        if not(self.db_exists()):
            self.setup_db()
        return None
    
    def disconnect(self):
        self.conn.commit();
        self.conn.close();
    
    
    #connecting to sql lite db
    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.text_factory = str
        cursor = self.conn.cursor()
        return cursor
    
    #dissconectiong from sql lite db
    def dissconnect(self):
        self.conn.close()
    
    
    def db_exists(self):
        #TODO maybe there is better way to check if there is already settings
        
        cursor = self.connect()
    
        #so we try to read table, if there is no table, then there will be exception
        #
        #if there is no error, then return true;
        #if there was error, then we return false;
        try:
            cursor.execute("SELECT * FROM settings");
            self.dissconnect()
            return True
        except:
            self.dissconnect()
            return False
        
        
    def read_settings(self):
        cursor = self.connect()
        cursor.execute("SELECT * FROM settings");
        data={};
        while True:
            row = cursor.fetchone()
            if row == None:
                break
            data[row[0]]=apiModel();
            data[row[0]].api_name=row[0]
            data[row[0]].api_key=row[1]
            data[row[0]].api_url=row[2]
            data[row[0]].api_secret=row[3]
            data[row[0]].api_username=row[4]
            data[row[0]].api_password=row[5]
        return data
            
        
        
    def save_settings(self,settings):
        cursor =self.connect();
        
        # with keys
        
        for (api_name, api_obj) in settings.iteritems():
            sql = 'select * from settings where api_name=\''+api_name+'\'';
            cf.print_v(sql)
            cursor.execute(sql);
            cf.print_v("this is ok");
            there_is_items=False;
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                else:
                    there_is_items=True;
                    
            if there_is_items:
                #update
                sql = '''update settings
                    set
                        api_name = \''''+ api_obj.api_name+'''\',
                        api_key = \''''+ api_obj.api_key+'''\',
                        api_url = \''''+ api_obj.api_url+'''\',
                        api_secret = \''''+ api_obj.api_secret+'''\',
                        api_username =\''''+ api_obj.api_username+'''\',
                        api_password = \''''+ api_obj.api_password+'''\'    
                    where api_name=\''''+api_name+'''\'
                    '''
                cursor.execute(sql);
                cf.print_v("updated settings value");
                return 2;
            else:
                #insert
                sql = '''insert into settings
                    (
                        api_name,
                        api_key,
                        api_url,
                        api_secret,
                        api_username,
                        api_password
                    )
                    values
                    (
                    "'''+ api_obj.api_name+'''",
                    "'''+ api_obj.api_key+'''",
                    "'''+ api_obj.api_url+'''",
                    "'''+ api_obj.api_secret+'''",
                    "'''+ api_obj.api_username+'''",
                    "'''+ api_obj.api_password+'''"
                    )
                    '''
                    
                cursor.execute(sql);
                
                cf.print_v("insering new data");
                cf.print_v(sql);
                return 1
                
        
        self.disconnect();
        return 0;
        

    def setup_db(self):
            
        #create tables if not exist
        #settings table
        cursor = self.connect()
        cursor.execute('''CREATE TABLE settings
                            (
                            api_name text,
                            api_key text,
                            api_url text,
                            api_secret text,
                            api_username text,
                            api_password text
                            )''')
        return 1