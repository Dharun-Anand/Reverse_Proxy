#!/usr/bin/env python3

"""
Created on Fri Mar 26 20:54:56 2021

@author: dharun
"""

import socket

HOST = '127.0.0.1'
PORT = 50001



if __name__ == "__main__":
    try:
        print("Starting Server")
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
                         conn.sendall(data)
                     
    except KeyboardInterrupt:
        pass


                
            