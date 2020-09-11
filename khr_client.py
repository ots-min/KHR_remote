# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 14:59:39 2020

@author: Minoru Otsuka
"""

import socket
import tkinter
import serial

def com_start():
    global com_on
    global sock, ser
    global com_num, speed
    
    try:
        ser = serial.Serial(com_num.get(), int(speed.get()), parity=serial.PARITY_EVEN)
        print("シリアルポートをオープンしました: ",com_num.get())
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("create socket")
        com_on = True
    except:
        print("シリアルポートがオープンできません: ",com_num.get())
    
def com_end():
    global com_on
    global sock, ser
    
    com_on = False
    
    ser.close()
    print("シリアルポートをクローズしました")
    
    sock.close()
    print("close socket")

def scan_button():
    global w, com_on, old_data
    global sock, ser
    global s_address, port

    refresh_rate = 10 #ボタンデータ読み取り間隔(ms)
    
    if(com_on == True):
        com_line = [0xBF,0x7F,0x00,0x02]
        ser.write(com_line)
    
        r_data = ser.read(12)
        data = r_data[8]*4096 + r_data[9]*256 + r_data[10]*16 + r_data[11]
        if(data != old_data):
            old_data = data
            s_data = data.to_bytes(2,"big")
            print(s_data[0],s_data[1])
        
            sock.sendto(s_data, (s_address.get(),int(port.get())))
    
    w.after(refresh_rate, scan_button)
    
def main():
    global w, com_on, old_data
    global s_address, port
    global com_num, speed

    w = tkinter.Tk()
    w.title("Player UI")

    s_address = tkinter.StringVar()
    e1 = tkinter.Entry(w, textvariable=s_address, width=20, font=("",15))
    e1.insert(0, "192.168.1.23")
    e1.pack()
    
    port = tkinter.StringVar()
    e2 = tkinter.Entry(w, textvariable=port, width=20, font=("",15))
    e2.insert(0, "59905")
    e2.pack()
    
    com_num = tkinter.StringVar()
    e3 = tkinter.Entry(w, textvariable=com_num, width=20, font=("",15))
    e3.insert(0, "COM3")
    e3.pack() 
    
    speed = tkinter.StringVar()
    e4 = tkinter.Entry(w, textvariable=speed, width=20, font=("",15))
    e4.insert(0, "115200")
    e4.pack()
    
    b_start = tkinter.Button(w,text="通信開始",font=("",20),command=com_start)
    b_start.pack()
    
    b_end = tkinter.Button(w,text="通信終了",font=("",20),command=com_end)
    b_end.pack()

    com_on = False
    old_data = 0
    
    w.after(0,scan_button)
    w.mainloop()

main()
