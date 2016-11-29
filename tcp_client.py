# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 14:58:16 2016

@author: Dominik
"""

import socket
 
 
TCP_IP = "141.24.42.20"
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "asdfsdfsfsfsefsefsefsfsea"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print("send message...")
s.send(MESSAGE.encode())
print("message sent.")
data = s.recv(BUFFER_SIZE)
s.close()

print("received data:", data.decode())