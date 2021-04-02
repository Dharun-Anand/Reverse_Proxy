#!/usr/bin/env python3

"""
Created on Fri Mar 26 20:54:56 2021

@author: Dharun Anand
"""

import socket

HOST = '127.0.0.1'
PORT = 50001


if __name__ == "__main__":
    try:
        print("Starting Client")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b'Hello, world')
            data = s.recv(1024)
    
        print('Received', repr(data))
    except KeyboardInterrupt:
        pass
  




