import pandas as pd

import time

import tkinter as tk

from tkinter import *

src = r"" #insert path where you want the file to be created along with file_name.csv
src2 = r"Slots.csv" #insert path where you want the file to be created

#checking if file already exists
try:        
    g = open(src, 'x') 
    g.write("User ID,Password,Slot 1,Slot 2,Slot 3,Slot 4,Slot 5,Complete,Notified") #creates columns
    g.close()
    data = pd.read_csv(src);
except FileExistsError:
    data = pd.read_csv(src);

exd = pd.read_csv(src2);

exd_av = {'Slots Available':[]}
exd_av = pd.DataFrame(exd_av)
exd_av['Slots Available'] = exd.loc[exd['Taken']!=1,'Slots']

data['User ID'] = data['User ID'].astype(str)
data['Password'] = data['Password'].astype(str)

k = 1
index = 0
choice = ""
send_mail = 0

p=tk.Tk(screenName=None,baseName=None,className='Portal',useTk=1)

notify = Message(p,text = "")
notify.config(width=150)
notify.grid(row=2)

Pdvar = StringVar()

Label(p, text='User ID').grid(row=0)

Label(p, text='Password').grid(row=1)

E_UID = Entry(p)
E_UID.grid(row=0, column=1)

E_Pd = Entry(p,textvariable=Pdvar,show='*')
E_Pd.grid(row=1, column=1)

def hide_pd():
    global Pdvar
    E_Pd = Entry(p,show='*',text=Pdvar.get(),textvariable=Pdvar)
    E_Pd.grid(row=1, column=1)
    button = tk.Button(p,text = 'Show Password',width=40,command=show_pd)
    button.grid(row=1,column=2)

def show_pd():
    global Pdvar
    E_Pd = Entry(p,text=Pdvar.get(),textvariable=Pdvar)
    E_Pd.grid(row=1, column=1)
    button = tk.Button(p,text = 'Hide Password',width=40,command=hide_pd)
    button.grid(row=1,column=2)
    
button = tk.Button(p,text = 'Log-in', width=19,command=lambda:[log_in()])
button.bind('<Return>', lambda _: log_in())
button.grid(row=3,column=0)

button = tk.Button(p,text = 'Register', width=19,command=lambda:[register()])
button.bind('<Return>', lambda _: register())
button.grid(row=3,column=1)

button = tk.Button(p,text = 'Show Password',width=40,command=show_pd)
button.grid(row=1,column=2)

def slot_select():

    def select(variable):
        global choice
        choice = variable
        global exd_av
        global exd
        exd_av['Slots Available'] = exd.loc[exd['Taken']!=1,'Slots']
        exd_av['Slots Available'] = exd_av.loc[exd_av['Slots Available'] != variable]
        for i in range(exd.shape[0]):
            if(exd.loc[i,'Slots']== choice):
                exd.loc[i,'Taken'] = 1
                exd.loc[i,'Taken By'] = UID
        global k
        k = k + 1
        slot.destroy()
        slot_select()
    
    global exd_av
    global index
    global choice
    global send_mail
    slot = tk.Tk()
    
    variable = StringVar(slot)
    
    if(k == 1):
        Label(slot,text = 'Slot 1').grid(row = 0)
        OptionMenu(slot,variable,*exd_av['Slots Available'].dropna(),command = select).grid(row = 0,column = 1)
    
    if(k == 2):
        data.loc[index,'Slot 1'] = choice
        Label(slot,text = 'Slot 2').grid(row = 0)
        OptionMenu(slot,variable,*exd_av['Slots Available'].dropna(),command = select).grid(row = 1,column = 1)
        
    if(k == 3):
        data.loc[index,'Slot 2'] = choice
        Label(slot,text = 'Slot 3').grid(row = 0)
        OptionMenu(slot,variable,*exd_av['Slots Available'].dropna(),command = select).grid(row = 2,column = 1)
            
    if(k == 4):
        data.loc[index,'Slot 3'] = choice
        Label(slot,text = 'Slot 4').grid(row = 0)
        OptionMenu(slot,variable,*exd_av['Slots Available'].dropna(),command = select).grid(row = 3,column = 1)
        
    if(k == 5):
        data.loc[index,'Slot 4'] = choice
        Label(slot,text = 'Slot 5').grid(row = 0)
        OptionMenu(slot,variable,*exd_av['Slots Available'].dropna(),command = select).grid(row = 4,column = 1)

    elif(k>5):
        data.loc[index,'Slot 5'] = choice
        data.loc[index,'Complete'] = 1
        send_mail = 1
        save()
        slot.destroy()

    variable.set("Select")

UID = ""
        
        
def register():
    global notify
    global E_UID
    global E_Pd
    global send_mail
    if(len(E_UID.get().strip()) == 0 or len(E_Pd.get().strip())==0):
        notify.grid_forget()
        notify = Message(p,text = "FIELD CANNOT BE EMPTY")
        notify.config(width=150)
        notify.grid(row=2)
    else:
        notify.grid_forget()
        notify = Message(p,text = "")
        notify.config(width=150)
        notify.grid(row=2)
        UID = E_UID.get().strip()
        Pd = E_Pd.get().strip()
        global data
        uid_check = 0
        uid_status = 0
        for i in range(data.shape[0]):
            if(UID != data.loc[i,'User ID']):
                uid_check += 1
        if(uid_check == data.shape[0]):
            uid_status = 1
            data = data.append({'User ID':UID,'Password':Pd}, ignore_index=True)
        else:
            notify.grid_forget()
            notify = Message(p,text = "User ID taken...Try again.")
            notify.config(width=150)
            notify.grid(row=2)
           
           

        if(uid_status):
            send_mail = 0
            save()

def log_in():
    global notify
    global UID
    if(data.shape[0] == 0):
        notify.grid_forget()
        notify = Message(p,text = "No accounts available...please register first")
        notify.config(width=150)
        notify.grid(row=2)
    else:
        UID = E_UID.get()
        Pd = E_Pd.get()
        uid_check0 = 0
        global index
        global k
        for i in range(data.shape[0]):
            if(UID == data.loc[i,'User ID']):
                if(data.loc[i,'Complete'] == 1):
                    notify.grid_forget()
                    notify = Message(p,text = "User has made selection already..")
                    notify.config(width=150)
                    notify.grid(row=2)
                    
                    
                    break
                else:
                    if(Pd == data.loc[i,'Password']):
                        notify.grid_forget()
                        notify = Message(p,text = "Log-in Successful.")
                        notify.config(width=150)
                        notify.grid(row=2)
                        k = 1
                        index = i
                        slot_select()
                        break
                    else:
                        notify.grid_forget()
                        notify = Message(p,text = "Incorrect Password...")
                        notify.config(width=150)
                        notify.grid(row=2)
                        
                        
                        break
            else:
                uid_check0 = uid_check0 + 1
        if(uid_check0 == data.shape[0]):
            notify.grid_forget()
            notify = Message(p,text = "Incorrect User ID...")
            notify.config(width=150)
            notify.grid(row=2)


def save():
    s=tk.Tk(screenName=None,baseName=None,className='Save changes?',useTk=1)

    def save_it():

        global data
        global exd_av
        global exd
        global send_mail
        #sending email notification
        
        if(send_mail):
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText

            fromaddr = "inviduty@gmail.com"
            toaddrs = data.loc[data['Notified'] != 1, 'User ID']
            for toaddr in toaddrs:
                
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = toaddr
                msg['Subject'] = "EXAM DUTY VERIFICATION"

                body = "DEAR USER,"+"\n\n"+"YOU HAVE SELECTED SLOTS:\n\n1. "+data.loc[data['User ID'] == toaddr, 'Slot 1'].iloc[0]\
                +"\n2. "+data.loc[data['User ID'] == toaddr, 'Slot 2'].iloc[0]\
                +"\n3. "+data.loc[data['User ID'] == toaddr, 'Slot 3'].iloc[0]\
                +"\n4. "+data.loc[data['User ID'] == toaddr, 'Slot 4'].iloc[0]\
                +"\n5. "+data.loc[data['User ID'] == toaddr, 'Slot 5'].iloc[0]
                msg.attach(MIMEText(body, 'plain'))

                import smtplib
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login("inviduty@gmail.com", "") 
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)

                data.loc[data['User ID'] == toaddr,'Notified'] = 1


        with open(src, 'w') as f:
            data.to_csv(f, index = False)
        with open(src2, 'w') as f:
            exd.to_csv(f, index = False)
        s.destroy()   
    button = tk.Button(s,text = 'Yes', width=19,command=save_it).grid(row=0,column=0)
    button = tk.Button(s,text = 'No', width=19,command=s.destroy).grid(row=0,column=1)

    


p.mainloop()



