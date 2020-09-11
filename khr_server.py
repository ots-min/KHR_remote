# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:03:42 2020

@author: Minoru Otsuka
"""

import socket
import serial
import sys

def send_command(data):
    global ser, com_line
    
    com_line[6] = data[0]
    com_line[7] = data[1]
    com_line[12] = (0x62 + data[0] + data[1])%256 #チェックサム
    
    ser.write(com_line)
    print("コマンド送信: ", com_line)
    
    try:
        r_num = ord(ser.read(1))
        r_data = ser.read(r_num-1)
        print("受信データ: ", r_data)
    except:
        print("データ受信失敗") 
    
def main():
    global ser, com_line
    
    s_address = "192.168.1.19"
    com_num = "COM6"
    
    com_line = [0x0D,0x00,0x02,0x50,0x03,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x62]
    
    try:
        ser = serial.Serial(com_num, 115200, parity=serial.PARITY_EVEN)
        print("シリアルポートをオープンしました")
    except:
        print("シリアルポートがオープンできません")
        sys.exit()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("create socket")

    sock.bind((s_address,0))
    print("port = ", sock.getsockname()[1])

    while True:
        print("Waiting")
        data, c_address = sock.recvfrom(2)
        print(data[0], data[1], c_address)
        send_command(data)

    sock.close()
    print("close socket")

    ser.close()
    print("シリアルポートをクローズしました")
main()
