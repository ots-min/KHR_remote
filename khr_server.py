# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:03:42 2020

@author: Minoru Otsuka
"""

import socket
import serial
import tkinter
from tkinter import ttk
from tkinter import messagebox

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
    
def khr_start():
    global str_ip, str_port, str_com, str_stat
    global ser, sock, com_on
    
    try:
        ser = serial.Serial(str_com.get(), 115200, parity=serial.PARITY_EVEN)
        print("シリアルポートをオープンしました")
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("ソケットをオープンしました")

        sock.settimeout(0.01)
        sock.bind((str_ip.get(),0))
        print("port = ", sock.getsockname()[1])
        str_port.set(sock.getsockname()[1])
        
        str_stat.set("パケット待ち")
        com_on = True

    except:
        messagebox.showerror("エラー", "シリアルポートがオープンできません")

def khr_end():
    global str_stat
    global ser, sock, com_on

    com_on = False
    
    sock.close()
    print("ソケットをクローズしました")

    ser.close()
    print("シリアルポートをクローズしました")
    
    str_stat.set("通信終了")

def wait_data():
    global sock
    global f, com_on, com_line, old_data
    global str_stat
    
    if(com_on == True):
        try:
            data, c_address = sock.recvfrom(2)
            str_stat.set("パケット受信中")
            if(data != old_data):
                print(data[0], data[1], c_address)
                send_command(data)
                old_data = data
        except socket.timeout:
            str_stat.set("パケット待ち")
    
    f.after(10, wait_data)

def main():
    global str_ip, str_port, str_com, str_stat
    global f, com_on, com_line, old_data
    
    com_line = [0x0D,0x00,0x02,0x50,0x03,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x62]
    old_data = 0
    
    w = tkinter.Tk()
    w.title("KHRサーバー")
    
    f = ttk.Frame(w, padding=10) 
    f.pack()
    
    b_start = ttk.Button(f,text="接続開始",command=khr_start)
    b_start.grid(row=0, column=0, columnspan=2)
    
    b_end = ttk.Button(f,text="接続切断",command=khr_end)
    b_end.grid(row=1, column=0, columnspan=2)
    
    label1 = ttk.Label(f,text="サーバーIPアドレス")
    label1.grid(row=2, column=0)

    str_ip = tkinter.StringVar()
    str_ip.set("192.168.1.23")
    e_ip = ttk.Entry(f,textvariable=str_ip)
    e_ip.grid(row=2, column=1)
    
    label2 = ttk.Label(f,text="ポート番号")
    label2.grid(row=3, column=0)

    str_port = tkinter.StringVar()
    str_port.set("00000")
    l_port = ttk.Label(f,textvariable=str_port)
    l_port.grid(row=3, column=1)
    
    label3 = ttk.Label(f,text="COM番号")
    label3.grid(row=4, column=0)

    str_com = tkinter.StringVar()
    str_com.set("COM5")
    e_com = ttk.Entry(f,textvariable=str_com)
    e_com.grid(row=4, column=1)
    
    label4 = ttk.Label(f,text="ステータス")
    label4.grid(row=5, column=0)
    
    str_stat = tkinter.StringVar()
    str_stat.set("開始待ち")
    l_stat = ttk.Label(f,textvariable=str_stat)
    l_stat.grid(row=5, column=1)

    com_on = False
    
    f.after(0, wait_data)
    f.mainloop()

main()
