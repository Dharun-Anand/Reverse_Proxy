#!/usr/bin/env python3

"""
Created on Fri Mar 26 20:54:56 2021

@author: dharun
"""

import json
import socket
import hashlib
import sys, getopt


def get_cmdArgs():
    argumentList = sys.argv[1:]
    short_options = ""
    long_options = ["id=","pp=","listen=","revproc="]
    arguments, values = getopt.getopt(argumentList, short_options, long_options)
    for current_argument, current_value in arguments:
        if current_argument in ("--id"):
            srcid = current_value
        elif current_argument in ("--pp"):
            pp = current_value
        elif current_argument in ("--listen"):
            port = current_value
        elif current_argument in ("--revproc"):
            revproc = current_value
    
    return [srcid,pp,port,revproc]
            
def setup_Server(pkt,revproc):
    print("Connecting to the reverse proxy on port",revproc)
    HOST = '127.0.0.1'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, revproc))
        pkt = bytes(json.dumps(pkt),encoding="utf-8") 
        s.sendall(pkt)
    

if __name__ == "__main__":
    try:        
        cmdArgs = get_cmdArgs()
        init_pkt = {"type":1,"id":cmdArgs[0],"privPoliId":cmdArgs[1],"listenport":cmdArgs[2]}
        
        setup_Server(init_pkt)
        
        print("Running server with id",cmdArgs[0])
        print("Server serving privacy policy",cmdArgs[1])
        print("Listening on port",cmdArgs[2])
        
        HOST = '127.0.0.1'
        PORT = int(cmdArgs[2])
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                         pkt = conn.recv(1024)                         
                         if not pkt:
                             break
                         pkt = json.loads(pkt.decode("utf-8"))
                         print("Received a message from client",pkt["srcid"],"payload:",pkt["payload"])
                         
                         pktHash = hashlib.sha1(pkt["payload"].encode())
                         
                         pkt = {"type":2,"srcid":cmdArgs[0],"destid":pkt["srcid"],"payloadsize":pkt["payloadsize"],"payload":pktHash}
                         print("Sending a response to the client",pkt["destid"],"payload:",pkt["payload"])
                         pkt = bytes(json.dumps(pkt),encoding="utf-8") 
                         conn.sendall(pkt)


    except KeyboardInterrupt:
        pass
  