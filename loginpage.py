
from tkinter import *
from PIL import ImageTk #for jpg
from tkinter import messagebox

def login():
    if usernameentry.get()=='' or pwdentry.get()=='':
        messagebox.showerror('Error','Fields cannot be Empty')
    elif usernameentry.get()=='Vee' and pwdentry.get()=='1234':
        messagebox.showinfo('Success','Welcome')
        window.destroy()
        import mainpage
    else:
        messagebox.showerror('Error','Invalid Login Credentials')

window=Tk()

window.geometry('1125x750+0+0')
window.title('Login Page')

window.resizable(False,False)

bgimg=ImageTk.PhotoImage(file='static/loginpage_bg.jpeg')
bglabel=Label(window,image=bgimg)
bglabel.place(x=0,y=0)

loginframe=Frame(window,bg='#d4c9c0')
loginframe.place(x=400,y=30)

logoimg=ImageTk.PhotoImage(file='static/loginpagelogo.jpg')
logolabel=Label(loginframe,image=logoimg)
logolabel.grid(row=0,column=0,columnspan=2,pady=10)

usernamelabel=Label(loginframe,text='Username',font=('papyrus',20), bg='#d4c9c0')
usernamelabel.grid(row=1,column=0,pady=10,padx=10)

usernameentry=Entry(loginframe,font=('papyrus',20),bg='#d4c9c0')
usernameentry.grid(row=1,column=1,pady=10,padx=10)

pwdlabel=Label(loginframe,text='Password',font=('papyrus',20), bg='#d4c9c0')
pwdlabel.grid(row=2,column=0,pady=10,padx=10)

pwdentry=Entry(loginframe,show='*',font=('papyrus',20),bg='#d4c9c0')
pwdentry.grid(row=2,column=1,pady=10,padx=10)

loginbutton=Button(loginframe,text='Login',font=('papyrus',20),bg='#c6b39e',
                   activebackground='#c6b39e',activeforeground='black',cursor='hand2',command=login)
loginbutton.grid(row=3,column=0,columnspan=2,pady=10,padx=10)

window.mainloop()


