#! /usr/bin/env python3
import sys, os, socket
from subprocess import call
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    if not os.fork():
        print("new child process handling connection from", addr)
        file = ""
        while True:
            payload = framedReceive(sock, debug)
            if debug: print("rec'd: ", payload)
            if payload: myFile += payload.decode().replace("\x00", "\n")
            else:
                textArr = myFile.split("//sep")
                myPath = os.path.join(os.getcwd()+"/sent/"+textArr[0])
                if(not call(["find", myPath])): #If file already exist
                    newName = input("File repeated. Please provide new name file: \n")
                    myPath=os.path.join(os.getcwd()+"/sent/"+newName)
                with open(myPath, 'w') as file:
                    file.write(textArr[1])
                    file.close()
                break
            payload += b"!"             # make emphatic!
            framedSend(sock, payload, debug)
