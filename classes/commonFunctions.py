#!/usr/bin/python
import sys
from gi.repository import GObject
from gi.repository import Notify


class cf:
    @staticmethod
    def print_v(message_to_console):
        if (len(sys.argv)>1 and sys.argv[1]=='-v'):
            print(message_to_console);

    @staticmethod            
    def sendmessage(title, message, file_path_to_icon=""):
        Notify.init("app-name")
        n = Notify.Notification.new(title, message, file_path_to_icon)
        n.show()
        #subprocess.Popen(['notify-send', message])
        return
    
    