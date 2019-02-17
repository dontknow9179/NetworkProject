import socket
import threading
import tkinter
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
import sys

host = '127.0.0.1'
port = 65432

login = '0'
logout = '1'
broadcast = '2'
secret = '3'
failsend = '6'
repeated = '7'
overflow = '8'
disconnect = '9'
nick = ''
text0 = None
text1 = None
sock = None
top = None

def connect_to_server():
    global nick
    global sock
    nick = entry_1.get()
    print(login + nick)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建套接字
    sock.connect((host,port))
    sock.send((login + nick).encode('utf-8'))
    Login()


def Login():
    instring = str(sock.recv(1024).decode("utf-8"))
    if instring.startswith(repeated):
        tkinter.messagebox.showinfo('warning', 'This name has been used.')
    elif instring.startswith(overflow):
        tkinter.messagebox.showinfo('warning', 'The room is full.')
    elif instring.startswith(login):
        chatwindow(instring[1:])

def chatwindow(instring):
    global text0
    global text1
    global top
    root.withdraw()
    top = tkinter.Toplevel()

    top.resizable(False, False)  # 固定窗口大小
    windowWidth = 500  # 获得当前窗口宽
    windowHeight = 460  # 获得当前窗口高
    screenWidth, screenHeight = top.maxsize()  # 获得屏幕宽和高
    geometryParam = '%dx%d+%d+%d' % (windowWidth, windowHeight, (screenWidth - windowWidth) / 2, (screenHeight - windowHeight) / 2)
    top.geometry(geometryParam)

    text0 = scrolledtext.ScrolledText(top,width=80,height=23)
    text0.configure(bg='black')
    text0.configure(foreground='white')
    text0.insert(tkinter.END, '▶ ' + instring + ' has entered the room.\n\n')
    text0.pack()

    top.title('Chat Room (' + instring + ')')

    text1 = tkinter.Text(top,width=80,height=9)
    text1.pack()

    frame_2 = tkinter.Frame(top)
    frame_2.pack()
    button1 = tkinter.Button(frame_2, text='SEND', command=Sendout)
    button1.pack(side='left')

    button2 = tkinter.Button(frame_2, text='LOGOUT', command=Logout)
    button2.pack(side='left')

    print(instring)

    thread = threading.Thread(target=receive)  # 创建一个接收信息的线程
    thread.start()

def Logout():
    global top
    global sock
    global root
    sock.send(logout.encode())
    top.destroy()
    sock.close()
    root.quit()

def receive():
    global text0
    global sock
    while True:
        try:
            instring = sock.recv(1024).decode("utf-8")
            print(instring)
            if instring.startswith(login):

                message = '▶ ' + instring[1:] + ' has entered the room.\n\n'
                text0.insert(tkinter.END,message)
            elif instring.startswith(logout):

                message = '▷ ' + instring[1:] + ' has left.\n\n'
                text0.insert(tkinter.END,message)
            elif instring.startswith(broadcast):

                message = instring[1:]
                text0.insert(tkinter.END,message)
            elif instring.startswith(secret):
                message = instring[1:]
                text0.insert(tkinter.END,message)
            elif instring.startswith(failsend):
                message = instring[1:]
                tkinter.messagebox.showinfo('warning', message)
            elif instring.startswith(disconnect):

                tkinter.messagebox.showinfo('warning','Disconnected.')
            else:
                break
        except Exception:
            break


def Sendout():
    global text0
    global text1
    global sock
    message = str(text1.get('0.0',tkinter.END))
    if message.startswith('@'):
        outstring = nick + message + '\n'
        text0.insert(tkinter.END,outstring)
        sock.send((secret + outstring).encode('utf-8'))
        text1.delete('0.0',tkinter.END)
    else:
        outstring = nick + ': ' + text1.get('0.0',tkinter.END) + '\n'
        text0.insert(tkinter.END,outstring)
        sock.send((broadcast + outstring).encode('utf-8'))
        text1.delete('0.0', tkinter.END)

root = tkinter.Tk()
root.title('DRRR!!!')  # 窗口标题
root.resizable(False, False)  # 固定窗口大小
windowWidth = 360  # 获得当前窗口宽
windowHeight = 425  # 获得当前窗口高
screenWidth, screenHeight = root.maxsize()  # 获得屏幕宽和高
geometryParam = '%dx%d+%d+%d' % (windowWidth, windowHeight, (screenWidth - windowWidth) / 2, (screenHeight - windowHeight) / 2)
root.geometry(geometryParam)  # 设置窗口大小及偏移坐标

backg = tkinter.Frame(root)
backg.pack()

img_gif = tkinter.PhotoImage(file='dollars2.gif')
label_img = tkinter.Label(backg, image=img_gif)
label_img.pack()

frame_1 = tkinter.Frame(backg)
label_1 = tkinter.Label(frame_1, text="USER NAME:")
label_1.pack(side='left')

entry_1 = tkinter.Entry(frame_1)
entry_1.pack(side='left')
frame_1.pack()

button = tkinter.Button(backg, text='LOGIN', command=connect_to_server)
button.pack()

root.mainloop()
exit()