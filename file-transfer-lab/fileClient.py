#! /usr/bin/env python3

# Echo client program
import socket, sys, re
sys.path.append("../lib")       # for params
import params
from framedSock import framedSend, framedReceive

#Method to let the user decide if he wants to use proxy or localhost
def select():
    ans = input("Use proxy or to use localhost [p/l]: \n")
    if(ans=="p"):
        return "50000"
    elif(ans=="l"):
        return "50001"
    return ""

#Method to get infromation from the file
def readFile():
    #While not valid fail
    while (1):
        try:
            filename = input("Input filename: \n")
            f = open(filename,'r')
            break
        except IOError: #Send error keep asking
            print("File doesn't exist.")

    fileInfo = f.read().replace("\n", "\0")
    f.close()
    fileInfo = filename+"//sep"+fileInfo+'\n' #Concatination to identify file
    return fileInfo

while (True):
    ans = select()
    if(ans != ""):
        break

switchesVarDefaults = (
    (('-s', '--server'), 'server', ("127.0.0.1:"+ ans)),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "fileClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print("attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

text = readFile() #Get information to send

framedSend(s, text.encode(), debug)
framedReceive(s,debug) #Doesn't use the output,just want to make sure the file is completely sent before the filecloses