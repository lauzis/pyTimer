#!/usr/bin/python
import requests
import json
import sqlite3
from gi.repository import Gtk


class pyTimerActiveColab:
    def __init__(self):
        return None
    
    def ac_api_get_projects():
        project_list_url= self.time_api_url + "?path_info=projects&format=json&auth_api_token="+self.settings.api_key;
        request = requests.get(project_list_url)
        projects = json.loads(request.content)
        print(projects)

class pyTimerDb():
    db_name = "pyTimer.dbo";
    def __init__(self):
        if not(self.db_exists()):
            self.setup_db()
        return None
    
    def connect(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        return cursor
    
    
    def db_exists(self):
        #TODO maybe there is better way to check if there is already settings
        
        cursor = self.connect()
    
        cursor.execute("SELECT settings FROM sqlite_master WHERE type='table' AND name='settings'");
        print(cursor);
        conn.close()
        
    def save_settings(obj_settings):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        return True;
        

    def setup_db(self):
            
        #create tables if not exist
        #settings table
        cursor = self.connect()
        cursor.execute('''CREATE TABLE settings
                            (
                            api_key text,
                            api_url text,
                            api_secret text,
                            username text,
                            password text
                            )''')
        return 1
    
    




class pyTimerSettings():
    ac_api_key=""
    ac_api_url=""

    def __init__(self):
        return None
    
    def read_settings():
        #reading settings from table
        return False
    
    def save(self):
        db = pyTimerDb();
        return db.save_settings(self);



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
        
        
        
        self.ux_win_main_link_signals()
        
        #linkint settings window signals/events with functions
        self.ux_win_settings_link_signals()
        
        self.ux_win_main.show_all()
        
        
        
        #menu exit
        #self.mainWindow.
            
        Gtk.main()
        
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
        self.settings.ac_api_key=ac_api_key.get_text();
        
        ac_api_url=self.builder.get_object('input_settings_ac_api_url')
        self.settings.ac_api_url = ac_api_url.get_text();
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
        ac_api_key.set_text(self.settings.ac_api_key);
        
        ac_api_url=self.builder.get_object('input_settings_ac_api_url')
        ac_api_url.set_text(self.settings.ac_api_url);
        
        
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
    app = pyTimer()

    
