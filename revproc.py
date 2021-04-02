#!/usr/bin/env python3

"""
Created on Fri Mar 26 20:54:56 2021

@author: dharun
"""

import json
import socket
import sys, getopt


def get_cmdArgs():
    argumentList = sys.argv[1:]
    short_options = ""
    long_options = ["port="]
    arguments, values = getopt.getopt(argumentList, short_options, long_options)
    for current_argument, current_value in arguments:
        if current_argument in ("--port"):
            port = current_value
    
    return [port]
            

if __name__ == "__main__":
    try:        
        cmdArgs = get_cmdArgs()
        
        print("Starting Reverse Proxy Server at Port " + cmdArgs[0])
        HOST = '127.0.0.1'
        PORT = int(cmdArgs[0])
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                         data = conn.recv(1024)
                         if not data:
                             break
                         print(data.decode("utf-8"))
                         conn.sendall(data)


    except KeyboardInterrupt:
        pass
  