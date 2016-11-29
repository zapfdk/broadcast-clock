#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 14:36:12 2016

@author: Dominik
"""

import socket

import time_manager as tm

class TCPManager():
    def __init__(self, tcp_ip, tcp_port, buffer_size):
        self.TCP_IP = tcp_ip
        self.TCP_PORT = tcp_port
        self.BUFFER_SIZE = buffer_size
        
        self.create_socket()
        
    def create_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.TCP_IP, self.TCP_PORT))
        self.s.listen(1)
        
    def start_input_loop(self):
        try:
            while 1:
                print("Waiting for connection...")
                
                conn, addr = self.s.accept()
                print("Connection address:", addr)
                data = conn.recv(BUFFER_SIZE)
                data = data.decode("utf-8")
                if data == "":
                    print("Error: Empty data received.")
                    conn.send(data.encode())
                    conn.close()
                    break
                print("Received data:", data)
                
                self.handle_data(data.split(" "))
                
                conn.send("Transmission successfull.")
                conn.close()
        finally:
            self.s.shutdown()
            self.s.close()
        
    def handle_data(self, data):
        if "-a" in data:
            delta_seconds = int(data[1])
            tm.add_secs_to_end_time(delta_seconds)        
        elif "-s" in data:
            delta_seconds = int(data[1])
            tm.add_secs_to_end_time(-delta_seconds)
        elif "-settext" in data:
            text = data[1]
            
        

if __name__ == "__main__":   
    TCP_IP = "141.24.42.20"
    TCP_PORT = 5005
    BUFFER_SIZE = 1024
    
    tcp_manager = TCPManager(TCP_IP, TCP_PORT, BUFFER_SIZE)
    tcp_manager.start_input_loop()
