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
        
def add_Server(pkt):
    global serverList
    
    indServer = next((index for (index, d) in enumerate(serverList) if (d["privPoliId"] == pkt["privPoliId"]) ), None)
    if indServer is None:
        serverList.append({ "privPoliId":pkt["privPoliId"], "id":[pkt["id"]], "listenport":[pkt["listenport"]], "roundrobin":0 })
    else:
        serverList[indServer]['id'].append(pkt["id"]); serverList[indServer]['listenport'].append(pkt["listenport"])
        
def client2server(pkt):
    global serverList
    
    indServer = next((index for (index, d) in enumerate(serverList) if (d["privPoliId"] == pkt["privPoliId"]) ), None)
    port = serverList[indServer]["listenport"][ serverList[indServer]["roundrobin"] ]
    serverID = serverList[indServer]["id"][ serverList[indServer]["roundrobin"] ]
    print("Forwarding a data message to server id",serverID,"payload:",pkt["payload"])
    
    serverList[indServer]["roundrobin"] = serverList[indServer]["roundrobin"] + 1
    if ( serverList[indServer]["roundrobin"] >= len(serverList[indServer]["id"]) ):
        serverList[indServer]["roundrobin"] = 0
    
    
    host = '127.0.0.1'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        pkt = bytes(json.dumps(pkt),encoding="utf-8") 
        s.sendall(pkt)
        
        pktHash = s.recv(1024)
        pktHash = json.loads(pktHash.decode("utf-8"))
        print("Received a data message from server id",pktHash["srcid"],"payload:",pktHash["payload"])
        print("Forwarding a data message to client id",pktHash["destid"],"payload:",pktHash["payload"])
        pktHash = bytes(json.dumps(pktHash),encoding="utf-8") 
        return pktHash    

serverList = {}
    
if __name__ == "__main__":
    try:        
        cmdArgs = get_cmdArgs()
        
        print("Running Reverse Proxy Server on Port",cmdArgs[0])
        HOST = '127.0.0.1'
        PORT = int(cmdArgs[0])
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    while True:
                         pkt = conn.recv(1024)
                         if not pkt:
                             break
                         pkt = json.loads(pkt.decode("utf-8"))
                         pktType = int(pkt["type"])
                         if pktType == 1:
                             print("Receiving setup message from server id",pkt["id"],"privacy policy",pkt["privPoliId"],"from port",pkt["listenport"])
                             add_Server(pkt)
                         elif pktType == 0:
                             print("Received a data message from client id",pkt["srcid"],"privacy policy",pkt["privPoliId"],"payload:",pkt["payload"])
                             conn.sendall(client2server(pkt))

    except KeyboardInterrupt:
        pass
    