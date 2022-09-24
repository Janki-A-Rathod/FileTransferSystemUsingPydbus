#!/usr/bin/env python3
#!
# Importing...
from pydbus import SessionBus  # from pydbus import SystemBus
from gi.repository import GLib
import signal
# Instantiation, Constants , Variables...
bus = SessionBus()
BUS =  "server.example.demo.test"
loop = GLib.MainLoop()
server_object = bus.get(BUS)
INTERVAL = 2
from datetime import datetime
import os
import base64
def deletefile():
    arg=(input("Which file you want to delete: "))
    #print(arg)
    reply = server_object.DeleteFileGivenByClient(arg)
    #print("Returned data is of type: {}".format(type(reply)))
    print("Sended From Server_:{}".format(reply))
    return True

def GetProperties():
    arg=(input("Enter File name: "))
    #print(arg)
    reply = server_object.FileInfo(arg)

def cb_signal_emission(*args):
    print("inside function")
    listofdatafiles = args[4][0]
    print("Client received files via signal: {}".format(listofdatafiles))

def uploadfileintoServer():
    if os.path.exists("abc.jpg"):
        with open("abc.jpg", "rb") as image2string:
            converted_string = base64.b64encode(image2string.read())
            reply= server_object.UploadGivenFile((converted_string.decode()))
    else:
        print("File Not Exist")
    return True

def DownloadfileGivenByServer():
    reply = server_object.DownloadFile()
    #print(reply)
    img_file = open('FileFromServer.jpg', 'wb')
    img_file.write(base64.b64decode(reply))
    img_file.close()
    return True

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)
def Getfileinfofromserver():
    arg=(input("Which file data you want: "))
    reply= server_object.FileInfo(arg)
    print("File name=",arg)
    print("The size of the file=",reply[0])
    print("File's last modified date=",reply[1])
    print("Last creation date in Unix systems",reply[2])
    return True
    

def main_method():
    print("File Transfer System")
    while (True):
        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGABRT,handler)
        print("1.Delete File\n2.Upload File\n3.File Info\n4.Download File")
        option = int(input('Enter your choice: ')) 
        if option == 1:
            print('Handle option \'Option 1\'')
            deletefile()
        elif option == 2:
            print('Handle option \'Option 2\'')
            uploadfileintoServer()
        elif option == 3:
            print('Handle option \'Option 3\'')
            Getfileinfofromserver()
        elif option == 4:
            print('Handle option \'Option 4\'')
            DownloadfileGivenByServer()
        else:
            print("\nChoose right option")
    return True
    

if __name__=="__main__":
    print("Starting Client...")
    dbus_filter = "/" + "/".join(BUS.split("."))
    bus.subscribe(object = dbus_filter, signal_fired = cb_signal_emission)
    GLib.timeout_add_seconds(interval=INTERVAL, 
                             function=main_method)
    loop.run()

