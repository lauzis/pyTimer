#!/usr/bin/python
import requests
import json
import sqlite3
import sys
from gi.repository import Gtk

def print_v(message_to_console):
    if (len(sys.argv)>1 and sys.argv[1]=='-v'):
        print(message_to_console);


class pyTimerActiveColab:
    def __init__(self):
        return None
    
    def ac_api_get_projects():
        project_list_url= self.time_api_url + "?path_info=projects&format=json&auth_api_token="+self.settings.api_key;
        request = requests.get(project_list_url)
        projects = json.loads(request.content)
        print(projects)

class pyTimerDb():
    db_name = "pyTimer.dbo"
    conn=""
    def __init__(self):
        if not(self.db_exists()):
            self.setup_db()
        return None
    
    #connecting to sql lite db
    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
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
        while True:
            row = cursor.fetchone()
            if row == None:
                break
            print(row);
        
        
    def save_settings(self,settings):
        cursor =self.connect();
        
        # with keys
        print(settings['active-colab'].api_key)
        for (api_name, api_obj) in settings:
            print api_name
            sql = '''insert or replace into settings
                (
                    api_name text,
                    api_key text,
                    api_url text,
                    api_secret text,
                    api_username text,
                    api_password text
                )
                values
                (
                '''+ api_obj.api_name+''',
                '''+ api_obj.api_key+''',
                '''+ api_obj.api_url+''',
                '''+ api_obj.api_secret+''',
                '''+ api_obj.api_username+''',
                '''+ api_obj.api_password+'''
                )'''
            print(sql)
        return True;
        

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
    
    


class apiModel():
    api_name=""
    api_key=""
    api_url=""
    api_secret=""
    api_username=""
    api_password=""


class pyTimerSettings():
    data = None

    def __init__(self):
        self.read()
        return None
    
    def is_settings(self):
        if (self.data==None or len(self.data)>0):
            return False
        else:
            return True
    
    def read(self):
        #reading settings from table
        db = pyTimerDb();
        self.data=db.read_settings();
        return False
    
    def save(self):
        db = pyTimerDb();
        
        print(self.data['active-colab'].api_name);
        if (self.data==None or len(self.data)==0):
            print("no data so dont have to save");
            return 1
        else:
            print_v("Saving data to the DB");
            return db.save_settings(self.data);



class pyTimer():
    
    settings = pyTimerSettings()
    
    
    builder = Gtk.Builder()
    builder.add_from_file("pyTimer.glade")
    
    #main window
    ux_win_main = builder.get_object("win_main")
    
    #settings window
    ux_win_settings = builder.get_object("win_settings")
    
    
    def __init__(self):
        #linking main window singals/events with functions
        
        
        print_v('Check if there is settings');
        if (not(self.settings.is_settings())):
            self.default_settings()
        self.ux_win_main_link_signals()
        
        #linkint settings window signals/events with functions
        print_v('Linking signals');
        self.ux_win_settings_link_signals()
        
        self.ux_win_main.show_all()
        
        
        
        #menu exit
        #self.mainWindow.
            
        Gtk.main()
        
    def default_settings(self):
        tmp_api = apiModel()
        
        #acctive colab default settings
        tmp_api.api_name="active-colab"
        tmp_api.api_key=""
        tmp_api.api_url=""
        tmp_api.api_secret=""
        tmp_api.api_username=""
        tmp_api.api_password=""
        self.settings.data={tmp_api.api_name:tmp_api}
        
        
        
    def ux_win_settings_link_signals(self):
        ux_win_settings = self.ux_win_settings
        
        ux_btn_settings_cancel = self.builder.get_object("btn_settings_cancel")
        ux_btn_settings_cancel.connect("clicked", self.ux_show_main)
        
        
        ux_btn_settings_save = self.builder.get_object("btn_settings_save")
        ux_btn_settings_save.connect("clicked",self.ux_settings_save)
        
        
    def ux_settings_save(self,widget,*args):
        #TODO
        print("saving settings");
        
        print("then closing the settings window");
        ac_api_key=self.builder.get_object('input_settings_ac_api_key')
        self.settings.data['active-colab'].api_key=ac_api_key.get_text();
        
        ac_api_url=self.builder.get_object('input_settings_ac_api_url')
        self.settings.data['active-colab'].api_url = ac_api_url.get_text();
        self.settings.save();
        
        
        self.ux_win_settings.hide();
        self.ux_win_main.show();
        self.ux_win_main.activate();
        
        
    def ux_win_main_link_signals(self):
        ux_win_main = self.ux_win_main
        
        main_menu_exit = self.builder.get_object("main_menu_exit")
        main_menu_settings = self.builder.get_object("main_menu_settings")
        
        #window exist
        ux_win_main.connect("delete-event", self.exit)
        #menu (file->exit)
        main_menu_exit.connect("activate", self.exit)
        
        #setting window
        main_menu_settings.connect("activate", self.ux_show_settings)
        
    
    def ux_show_main(self,widget,*args):
        print("show main");
        self.ux_win_settings.hide();
        self.ux_win_main.show();
        self.ux_win_main.activate();
        
        
    def ux_show_settings(self,widget,*args):
        print("show settings");
        ac_api_key=self.builder.get_object('input_settings_ac_api_key')
        ac_api_key.set_text(self.settings.data['active-colab'].api_key);
        
        ac_api_url=self.builder.get_object('input_settings_ac_api_url')
        ac_api_url.set_text(self.settings.data['active-colab'].api_url);
        
        
        self.ux_win_main.hide();
        self.ux_win_settings.show();
        self.ux_win_settings.activate();
    
    def exit(self, widget,*args):
        import sys
        print('exit');
        Gtk.main_quit();
        sys.exit()
        
    def UX_quit():
        self.exit();

if __name__ == "__main__":
    print_v("Init");
    app = pyTimer()

    
