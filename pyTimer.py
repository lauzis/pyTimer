#!/usr/bin/python
import requests
import json
import sched
import time
from gi.repository import Gtk



#including local classes
from classes.activeColab import activeColab
from classes.apiModel import apiModel
from classes.pyTimerSettings import pyTimerSettings
from classes.commonFunctions import cf








class pyTimer():
    
    settings=None
    builder=None
    
    #main window
    ux_win_main = None
    
    #settings window
    ux_win_settings=None;
    
    scheduler = sched.scheduler(time.time, time.sleep)
    
    def __init__(self):
        
        #init
        self.settings= pyTimerSettings()
        
        self.builder= Gtk.Builder()
        self.builder.add_from_file("pyTimer.glade")
        
        
        #main window
        self.ux_win_main = self.builder.get_object("win_main")
        
        #settings window
        self.ux_win_settings = self.builder.get_object("win_settings")
        
        #loading settings
        cf.print_v('Check if there is settings');
        if (not(self.settings.is_settings())):
            self.default_settings()
        self.ux_win_main_link_signals()
        
        #linking main window singals/events with functions
        
        
        
        #linkint settings window signals/events with functions
        cf.print_v('Linking signals');
        self.ux_win_settings_link_signals()
        
        self.ux_win_main.show_all()
        
        
        
        #menu exit
        #self.mainWindow.
            
        Gtk.main()
        
    def scheduled_task(sc): 
        print "Doing stuff..."
        # do your stuff
        cf.sendmessage("Working?","There is no active task, maybe you forgot to set tast?")
        sc.enter(60, 1, scheduled_task, (sc,))
        
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
    cf.print_v("Init");
    cf.sendmessage("pyTimer","Timer started!","");
    app = pyTimer()
    
    

    
