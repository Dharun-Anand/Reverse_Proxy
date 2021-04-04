Author: Dharun Anandayuvaraj
Contact: dharun99@gmail.com
Description: This repository contains a reverse proxy system, implemented with round robin based load balancing. 
Upcoming Updates: The system will soon be updated with a multi-threaded reverse proxy that can handle multiple simultaneous connections.
 

To test:

$ ./revproc.py --port 50001
$ ./server.py --id A1 --pp AAA --listen 50002 --revproc 50001
$ ./server.py --id A2 --pp AAA --listen 50003 --revproc 50001
$ ./server.py --id B1 --pp BBB --listen 50004 --revproc 50001
$ ./client.py --id A1 --revproc 50001 --pkt pktA1.json & ./client.py --id B1 --revproc 50001 --pkt pktB1.json & ./client.py --id A2 --revproc 50001 --pkt pktA2.json

