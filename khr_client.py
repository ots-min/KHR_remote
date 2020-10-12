# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 14:59:39 2020

@author: Minoru Otsuka
"""

import socket
import serial
import tkinter
from tkinter import ttk
from tkinter import messagebox
import ctypes

def key_scan(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key)&0x8000))

def com_start():
    global com_on
    global sock, ser
    global str_com, str_stat, str_mode
    
    try:
        if(str_mode.get() == "KRC"):
            ser = serial.Serial(str_com.get(), 115200, parity=serial.PARITY_EVEN)
            print("シリアルポートをオープンしました: ",str_com.get())

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("ソケットをオープンしました")
        
        str_stat.set("通信中")
        com_on = True
    except:
        print("シリアルポートがオープンできません")
        messagebox.showerror("エラー", "シリアルポートがオープンできません")
    
def com_end():
    global com_on
    global sock, ser
    global str_stat, str_mode
    
    com_on = False

    sock.close()
    print("ソケットをクローズしました")
    
    if(str_mode.get() == "KRC"):
        ser.close()
        print("シリアルポートをクローズしました")
    
    str_stat.set("通信終了")

def scan_button():
    global f, com_on
    global sock, ser
    global str_ip, str_port, str_mode

    refresh_rate = 50 #ボタンデータ読み取り間隔(ms)
    
    if(com_on == True):
        if(str_mode.get() == "KRC"):
            com_line = [0xBF,0x7F,0x00,0x02]
            ser.write(com_line)
    
            r_data = ser.read(12)
            data = r_data[8]*4096 + r_data[9]*256 + r_data[10]*16 + r_data[11]
        else:
            data = 0
            if(key_scan(87)): #w
                data |= 1 
            if(key_scan(65)): #a
                data |= 8
            if(key_scan(83)): #s
                data |= 2
            if(key_scan(68)): #d
                data |= 4
            if(key_scan(81)): #q(a+s)
                data |= 10
            if(key_scan(69)): #e(d+s)
                data |= 6
            if(key_scan(38)): #UP
                data |= 16
            if(key_scan(85)): #U
                data |= 4096 #シフト4(起き上がり)

        s_data = data.to_bytes(2,"big")
        #print(s_data[0],s_data[1])
        sock.sendto(s_data, (str_ip.get(),int(str_port.get())))
    
    f.after(refresh_rate, scan_button)

def mode_change():
    global e_com, str_mode

    if(str_mode.get() == "キーボード"):
        e_com.configure(state="disable")
    else:
        e_com.configure(state="enable")
    
def main():
    global f, com_on, e_com
    global str_ip, str_port, str_com, str_stat, str_mode

    w = tkinter.Tk()
    w.title("プレイヤーUI")

    f = ttk.Frame(w, padding=10) 
    f.pack()

    label4 = ttk.Label(f, text="入力デバイス")
    label4.grid(row=0, column=0)
    
    str_mode = tkinter.StringVar()
    f_mode = ttk.Frame(f) 
    r_mode1 = ttk.Radiobutton(f_mode, text="KRC", value="KRC", variable=str_mode, command=mode_change)
    r_mode1.grid(row=0, column=0)
    r_mode2 = ttk.Radiobutton(f_mode, text="キーボード", value="キーボード", variable=str_mode, command=mode_change)
    r_mode2.grid(row=0, column=1)
    str_mode.set("KRC")
    f_mode.grid(row=0, column=1, columnspan=2)

    label5 = ttk.Label(f, text="ネットワーク")
    label5.grid(row=1, column=0)
    
    b_start = ttk.Button(f, text="通信開始", command=com_start)
    b_start.grid(row=1, column=1)
    
    b_end = ttk.Button(f, text="通信終了", command=com_end)
    b_end.grid(row=1, column=2)

    label1 = ttk.Label(f, text="サーバーIPアドレス")
    label1.grid(row=2, column=0)
    
    str_ip = tkinter.StringVar()
    str_ip.set("192.168.1.23")
    e_ip = ttk.Entry(f, textvariable=str_ip)
    e_ip.grid(row=2, column=1, columnspan=2)
    
    label2 = ttk.Label(f, text="ポート番号")
    label2.grid(row=3, column=0)
    
    str_port = tkinter.StringVar()
    str_port.set("10000")
    e_port = ttk.Entry(f, textvariable=str_port)
    e_port.grid(row=3, column=1, columnspan=2)
    
    label3 = ttk.Label(f, text="COM番号")
    label3.grid(row=4, column=0)
    
    str_com = tkinter.StringVar()
    str_com.set("COM3")
    e_com = ttk.Entry(f, textvariable=str_com)
    e_com.grid(row=4, column=1, columnspan=2)

    label9 = ttk.Label(f, text="ステータス")
    label9.grid(row=5, column=0)
    
    str_stat = tkinter.StringVar()
    str_stat.set("開始待ち")
    l_stat = ttk.Label(f, textvariable=str_stat)
    l_stat.grid(row=5, column=1, columnspan=2)

    com_on = False
    
    f.after(0,scan_button)
    f.mainloop()

main()
