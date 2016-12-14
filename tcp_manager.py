#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 14:36:12 2016

@author: Dominik
"""

import socket
import sys
import time_manager as tm
from datetime import datetime, timedelta

class TCPManager():
    def __init__(self, tcp_ip, tcp_port, buffer_size):
        self.TCP_IP = tcp_ip
        self.TCP_PORT = tcp_port
        self.BUFFER_SIZE = buffer_size
        
        self.create_socket()
        
        self.has_server_stopped = False
        
    def stop_server(self):
        print("Shutting down socket...")
        self.s.shutdown(socket.SHUT_RDWR)
        print("Closing socket...")
        self.s.close()
        self.has_server_stopped = True
        
    def create_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.TCP_IP, self.TCP_PORT))
        self.s.listen(5)
        
    def start_input_loop(self):
        try:
            while not self.has_server_stopped:
                print("Waiting for connection...")
                
                conn, addr = self.s.accept()
                print("Connection address:", addr)
                data = conn.recv(BUFFER_SIZE)
                data = data.decode("utf-8")
                print("Received data:", data)
                if data == "":
                    print("Error: Empty data received.")
                    conn.send(data.encode())
                    conn.close()
                elif data == "-stop":
                    print("Closing connection...")
                    conn.send(data.encode())
                    conn.close()
                    break
                elif data == "-check":
                    print("Checking.")
                    conn.send("check".encode())
                    conn.close()
                else:
                    self.handle_data(data.split(" "),conn)
                
        except:
            print(sys.exc_info()[0])
        finally:
            self.stop_server()
        
    def handle_data(self, data, conn):
        check_code = "check".encode()
        fail_code = "fail".encode()

        if "-a" in data:
            try:
                delta_seconds = int(data[1])
                tm.add_secs_to_end_time(delta_seconds)
                conn.send(check_code)
            except:
                conn.send(fail_code)
            
        elif "-s" in data:
            try:
                delta_seconds = int(data[1])
                tm.add_secs_to_end_time(-delta_seconds)
                conn.send(check_code)
            except:
                conn.send(fail_code)

        elif "-settext" in data:
            try:
                text_list = data[1:]
                text = " ".join(text_list)
                tm.save_hint_text_to_txt(text)
                conn.send(check_code)
            except:
                conn.send(fail_code)

        elif "-setendtime" in data:
            try:
                end_time_string = data[1]
                end_time = datetime.strptime(end_time_string,"%H:%M:%S")
                conn.send(check_code)
            except:
                conn.send(fail_code)

        elif "-setremainingtime" in data:
            try:
                conn.send(check_code)
            except:
                conn.send(fail_code)

            
        elif "-getremainingtime" in data:
            conn.send(tm.get_hint_text_from_txt("remaining_time.txt").encode())
            
        elif "-gethinttext" in data:
            conn.send(tm.get_hint_text_from_txt("hint_text.txt").encode())
            
        elif "-getendtime" in data:
            end_time = str(tm.get_time_from_txt("end_time.txt"))
            print(end_time)
            conn.send(end_time.encode())
                
        conn.close()

if __name__ == "__main__":   
    TCP_IP = socket.gethostbyname(socket.gethostname())
    TCP_PORT = 5005
    BUFFER_SIZE = 1024
    
    tcp_manager = TCPManager(TCP_IP, TCP_PORT, BUFFER_SIZE)
    print("Created TCP Socket at %s:%s." %(TCP_IP,TCP_PORT))
    tcp_manager.start_input_loop()
    print("Stopped TCP Server.")
