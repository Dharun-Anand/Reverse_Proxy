#!/usr/bin/env python3

"""
Created on Fri Mar 26 20:54:56 2021
@author: Dharun Anand
"""

import json
import socket
import sys, getopt


def get_cmdArgs():
    argumentList = sys.argv[1:]
    short_options = ""
    long_options = ["id=", "revproc=", "pkt="]
    arguments, values = getopt.getopt(argumentList, short_options, long_options)
    for current_argument, current_value in arguments:
        if current_argument in ("--id"):
            srcid = current_value
        elif current_argument in ("--revproc"):
            revproc = current_value
        elif current_argument in ("--pkt"):
            pktName = current_value
    
    return [srcid, revproc, pktName]
            
def get_pktData(pktName):
    with open(pktName) as f:
        return (json.load(f))
    

if __name__ == "__main__":
    try:        
        cmdArgs = get_cmdArgs()
        pkt = get_pktData(cmdArgs[2])
        
        HOST = '127.0.0.1'
        PORT = int(cmdArgs[1])
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print("Sending message",pkt["payload"],"to privacy policy",pkt["privPoliId"],"through reverse proxy running on port",PORT)
            
            pkt = bytes(json.dumps(pkt),encoding="utf-8") 
            s.sendall(pkt)
            
            pkt = s.recv(1024)
            pkt = json.loads(pkt.decode("utf-8"))
            
            print("Receiving a response from the server",pkt["srcid"],"payload:",pkt["payload"])

    except KeyboardInterrupt:
        pass