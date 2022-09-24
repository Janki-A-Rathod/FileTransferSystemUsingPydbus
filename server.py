#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# server_demo_1.py
# Objective: 
#   Test that a server program can receive a method call using pydbus.
#   The method call passes no arguments.
#   Uses the session bus
#
# Use gdbus to generate the method call
# $ gdbus call --session --dest org.example.demo.test --object-path /org/example/demo/test --method org.example.demo.test.server_no_args
#
# Ian Stewart
# 2019-11-22
# 
# Importing...
import sys
if int(sys.version[0]) < 3: sys.exit("Please use python 3. Exiting...")

# Importing...
from pydbus import SessionBus  # SystemBus
from gi.repository import GLib
from pydbus.generic import signal
# Variables / Constants / Instantiation...
bus = SessionBus()  # SystemBus
BUS = "server.example.demo.test"
loop = GLib.MainLoop()
message_count = 0
import os
INTERVAL = 2
from datetime import datetime
import base64
#import signal
class DBusService_XML():
    """
    DBus Service XML definition. 
    type="i" for integer, "s" string, "d" double, "as" list of string data.
    """
    dbus = """
    <node>
        <interface name="{}">
            <signal name="ListAllFiles">
                <arg type="as"/>
            </signal>
            <method name="FileInfo">
                <arg type="s" name="input" direction="in">
                </arg>
                <arg type="as" name="output" direction="out">
                </arg>
            </method>
            <method name="UploadGivenFile">
                <arg type="s" name="person" direction="in">
                </arg>
            </method>
            <method name="DownloadFile">
                <arg type="s" name="person" direction="out">
                </arg>
            </method>
            <method name="DeleteFileGivenByClient">
                <arg type="s" name="input" direction="in">
                </arg>
                <arg type="s" name="output" direction="out">
                </arg>
            </method>
        </interface>
    </node>
    """.format(BUS)
    ListAllFiles = signal()

    def FileInfo(self,arg_string):
        path = "/home/janki/Desktop/pythondbus"
        if os.path.exists(arg_string):
            print("File exist")  
            Modified_time = str(datetime.fromtimestamp(os.path.getmtime(arg_string)))
            createdtime = str(datetime.fromtimestamp(os.path.getctime(arg_string)))
            getinfo=[str(os.path.getsize(arg_string)),Modified_time,createdtime]
            #getinfo=[str(os.path.getsize(arg_string)),str(os.path.getmtime(arg_string)),str(os.path.getctime(arg_string))]
            print(type(getinfo))
            print(getinfo)
        else:
            getinfo="File Not exit"
        return getinfo

    def UploadGivenFile(self,name):
        #converted_bytes=name.encode('utf-8')
        img_file = open('janki.jpg', 'wb')
        img_file.write(base64.b64decode(name))
        img_file.close()
        return
            
    def DeleteFileGivenByClient(self,input_string):
        if os.path.exists(input_string):
        # removing the file using the os.remove() method
            os.remove(input_string)
            send_to_client = "File Deleted"
        else:
        # file not found message
            print("File not found in the directory")
            send_to_client = "File Not Found"
        return send_to_client

    def DownloadFile(self):
        #path = "/home/janki/Desktop/pythondbus"
        if os.path.exists("abc.jpg"):
            with open("abc.jpg", "rb") as image2string:
                converted_string = base64.b64encode(image2string.read())
                #reply= server_object.UploadGivenFile((converted_string.decode()))
                send_to_client= (converted_string.decode())
        else:
            send_to_client="File Not Exist"
        return send_to_client

def send():
    #SendOutAllTheFiles
    path = "/home/janki/Desktop/pythondbus"
    dir_list = os.listdir(path)
    print("Files and directories in '", path, "' :") 
    # print the list 
    print(dir_list) 
    emit.ListAllFiles(dir_list)
    return True

if __name__ == "__main__":
    emit = DBusService_XML()
    bus.publish(BUS,emit)
    print("Starting Server ...")
    GLib.timeout_add_seconds(interval=INTERVAL, function=send)
    #bus.publish(BUS,)
    loop.run()