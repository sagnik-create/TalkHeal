#Downloading the Background Image from OneDrive
import urllib.request
import base64

def download(link):
    s=(base64.b64encode(bytes(link, 'utf-8'))).decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
    return f"https://api.onedrive.com/v1.0/shares/u!{s}/root/content"
link = "https://1drv.ms/i/s!Apzf3AWnJd9sijH6u7KpbVZLXdXv"
urllib.request.urlretrieve(download(link),"temp.jpg")

#The Main Window, Frame, Image and Heading
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

window = Tk()
window.title("PeacePulse")
window.geometry("1700x980")
frame1 = Frame(window,bg="#E8C7C8",bd=5,relief = RIDGE)
frame1.place(x = 10, y = 10, width = 1680, height = 960)
image1 = Image.open("temp.jpg")
image1 = image1.resize((1680,940))
image1 = ImageTk.PhotoImage(image1)
background_label = Label(frame1, image=image1, bg="#E8C7C8")
background_label.place(x=0, y=0, relwidth=1, relheight=1)
heading = Label(frame1,text="Your Personal AI-based Mental Health Assistant:)",font=("Comic Sans MS",20,"bold"),bg="light cyan",bd=5,relief = RIDGE)
heading.pack(side = TOP)

#Function-Issue
import requests
import webbrowser
import webview

def issue():
    webview.create_window("Your Guide 1 at your Service:)","https://www.helpguide.org/?s="+str(entry1.get().lower().replace(" ","-"))+"&g-recaptcha-response=03AKH6MRHf5ftBK7yWWcyyzLoV9JhasM2RlC90WfjVHd3boA1UFwuz2We0-rf3d7gm8nUnOpF4s19xCt7jr_j5d7D1BVDTXclAS0ufHEraIoXVnWm-tY_seYafoXg2F-L6talBCmQ6sHuamCwxbo6BR7ZtVjPm_W3CYJ070DYtuqgMEoZnF-fzf1lmGDy6d8NfpNmoRr2dm0qGP7hYh2dVH9iHfaPjpk2CIxa3UykSejAmiVaVadrT3TWPXevb8168RNDQ4p2-F-itvq5sjv6qfsBB43GBcDWe2QwK_jccL9l7R5mzMHvIr8tceJre7cuHTXB5rJ08Yvk3AsGE8Owvhg4nbRkvCOxO725Y_8oUnnQ3qZUGMGymoLARkEvu5uSTuDy7h0xaMj0iHUT2yIlO3Es6I9NndCMNrV9PJynLsFSeikB7vB_NXmkLwB-JSR6uK-GdK2-b41qMSaU1KFDQfGJ1_jwyzeAYAZ3O0o6SquXKbHPg0hNOKhg_MXdux0lSb2SJY6h8RW2DOQgZTxa9Avl0XoBxs8PFP2_J-3gCy7PeZtSTzUJxGG3ZEXPL1-dM7ZBrRNuwbI1r",width=1000,height=1000)
    webview.create_window("Your Guide 2 at your Service:)","https://www.nimh.nih.gov/search-nimh?q="+str(entry1.get().lower().replace(" ","-")), width=800,height=800)
    webview.create_window("Your Guide 3 at your Service:)","https://www.mind.org.uk/search-results/?q="+str(entry1.get().lower().replace(" ","-"))+'#'+"stq="+str(entry1.get().lower().replace(" ","-"))+"&stp=1")
    webview.start()

#Issue
from gtts import gTTS
import os

label = Label(frame1,text="What's your Issue ^-*?",font=("Comic Sans MS",15,"bold"),bg="#E8C7C8")
label.place(x = 650, y = 80)
label1 = Text(frame1,font=("Comic Sans MS",9,"bold"),bg="#E8C7C8",wrap=WORD)
label1.place(x=1150,y=80,width=500,height=60)
label1.insert(tk.END, "I'm At Your Service:)") 
entry1 = Entry(frame1,bg="light cyan",font=("Comic Sans MS",10),bd=5,relief = RIDGE)
entry1.place(x = 530, y = 130, width = 500)
def clicked():
    myQn = entry1.get()
    label1.place_configure(height=600)
    label1.config(state=tk.NORMAL)
    label1.delete(1.0,tk.END)
    os.system("start response.mp3")
button1=Button(window, text="Search", command = lambda: issue())
button1.place(x = 1050, y = 150, width = 100)

#Function-Location
def location():
    k = webview.create_window("Care Centres for You:)","https://www.google.com/maps/search/Mental+Hospitals+and+trauma+care+centres+in+"+str(entry2.get().lower().replace(" ","-"))+"/")
    webview.start()

#Location
label2 = Label(frame1,text="Where Do You Stay Friend?",font=("Comic Sans MS",15,"bold"),bg="#E8C7C8")
label2.place(x = 20, y = 700)
entry2 = Entry(frame1,bg="light cyan",font=("Comic Sans MS",15,"bold"),bd=5,relief = RIDGE)
entry2.place(x = 20, y = 750, width = 200)
button2=Button(window, text="Search", command = lambda: location())
button2.place(x = 240, y = 770, width = 50)

#Function-Professionals
def professionals():
    webview.create_window("Some Professionals Who Can Help You:)","https://www.goodtherapy.org/therapists/search")
    webview.start()

#Professionals
label3 = Label(frame1,text="Some Specialists Who Can Help You:)",font=("Comic Sans MS",15,"bold"),bg="#E8C7C8")
label3.place(x = 1200, y = 700)
button3=Button(window, text="Search", command = lambda: professionals())
button3.place(x = 1410, y = 770, width = 50)

#Displayin' the Developers
label4 = Label(frame1,text="Developed By: ",font=("Comic Sans MS",11,"bold"),bg="#E8C7C8")
label4.place(x = 30, y = 820)
name = "The Quantum Tech Mystifiers"
label5 = Label(frame1,text= name + '\n"It'+"'"+'s absolutely okay not to be okay:)"',font=("Comic Sans MS",11,"italic"),bg="#E8C7C8")
label5.place(x = 230, y = 820)

#Displayin' the date
import time

date = time.strftime("%d/%m/%y")
label6 = Label(frame1,text="Date :" + date,font=("Comic Sans MS",11,"bold"),bg="#E8C7C8")
label6.place(x = 230, y = 880)

window.mainloop()
