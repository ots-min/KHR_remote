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
    global ser, com_line, khr_on
    
    if(khr_on == False ):
        return
    
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
    
def net_start():
    global str_ip, str_port, str_stat
    global sock, com_on
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("ソケットをオープンしました")

    sock.settimeout(0.05) #クライアントの更新レートに合わせる
    
    try:
        sock.bind((str_ip.get(),int(str_port.get())))
        print("port = ", sock.getsockname()[1])
        
        str_stat.set("パケット待ち")
        com_on = True
    except:
        print("バインド失敗") 
        str_stat.set("バインド失敗")

def net_end():
    global str_stat, l_stat
    global sock, com_on

    com_on = False
    
    sock.close()
    print("ソケットをクローズしました")
    
    str_stat.set("通信終了")
    l_stat.config(foreground="black")

def khr_start():
    global str_com, str_stat2, l_stat2
    global ser, khr_on

    try:
        ser = serial.Serial(str_com.get(), 115200, parity=serial.PARITY_EVEN)
        print("シリアルポートをオープンしました")
        
        str_stat2.set("接続中")
        l_stat2.config(foreground="green")
        khr_on = True
    except:
        messagebox.showerror("エラー", "シリアルポートがオープンできません")
    
def khr_end():
    global str_stat2, l_stat2
    global ser, khr_on
    
    khr_on = False
    
    ser.close()
    print("シリアルポートをクローズしました")
    
    str_stat2.set("通信終了")
    l_stat2.config(foreground="black")
    
def wait_data():
    global sock
    global f, com_on, com_line, old_data
    global str_stat, l_stat
    
    if(com_on == True):
        try:
            data, c_address = sock.recvfrom(2)
            str_stat.set("パケット受信中")
            l_stat.config(foreground="green")
            if(data != old_data):
                print(data[0], data[1], c_address)
                send_command(data)
                old_data = data
        except socket.timeout:
            str_stat.set("パケット待ち")
            l_stat.config(foreground="black")
    
    f.after(10, wait_data)

def main():
    global str_ip, str_port, str_com, str_stat, str_stat2, l_stat, l_stat2
    global f, com_on, khr_on, com_line, old_data
    
    com_line = [0x0D,0x00,0x02,0x50,0x03,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x62]
    old_data = 0
    
    w = tkinter.Tk()
    w.title("KHRサーバー")
    
    f = ttk.Frame(w, padding=10) 
    f.pack()

    label5 = ttk.Label(f,text="ネットワーク")
    label5.grid(row=0, column=0)
    
    b_start = ttk.Button(f,text="受信開始",command=net_start)
    b_start.grid(row=0, column=1)
    
    b_end = ttk.Button(f,text="通信切断",command=net_end)
    b_end.grid(row=0, column=2)

    label6 = ttk.Label(f,text="KHR")
    label6.grid(row=1, column=0)
    
    b2_start = ttk.Button(f,text="接続開始",command=khr_start)
    b2_start.grid(row=1, column=1)
    
    b2_end = ttk.Button(f,text="接続終了",command=khr_end)
    b2_end.grid(row=1, column=2)

    label1 = ttk.Label(f,text="サーバーIPアドレス")
    label1.grid(row=2, column=0)

    str_ip = tkinter.StringVar()
    str_ip.set(socket.gethostbyname(socket.gethostname()))
    
    e_ip = ttk.Entry(f,textvariable=str_ip,state="readonly")
    e_ip.grid(row=2, column=1, columnspan=2)
    
    label2 = ttk.Label(f,text="ポート番号")
    label2.grid(row=3, column=0)

    str_port = tkinter.StringVar()
    str_port.set("54141")
    e_port = ttk.Entry(f,textvariable=str_port)
    e_port.grid(row=3, column=1, columnspan=2)
    
    label3 = ttk.Label(f,text="COM番号")
    label3.grid(row=4, column=0)

    str_com = tkinter.StringVar()
    str_com.set("COM5")
    e_com = ttk.Entry(f,textvariable=str_com)
    e_com.grid(row=4, column=1, columnspan=2)
    
    label4 = ttk.Label(f,text="ネットステータス")
    label4.grid(row=5, column=0)
    
    str_stat = tkinter.StringVar()
    str_stat.set("開始待ち")
    l_stat = ttk.Label(f,textvariable=str_stat)
    l_stat.grid(row=5, column=1, columnspan=2)
    
    label7 = ttk.Label(f,text="KHRステータス")
    label7.grid(row=6, column=0)
    
    str_stat2 = tkinter.StringVar()
    str_stat2.set("開始待ち")
    l_stat2 = ttk.Label(f,textvariable=str_stat2)
    l_stat2.grid(row=6, column=1, columnspan=2)

    com_on = False
    khr_on = False
    
    f.after(0, wait_data)
    f.mainloop()

main()
