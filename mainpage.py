from tkinter import *;
from PIL import ImageTk
import ttkthemes
from tkinter import ttk,messagebox,filedialog
import time
import pymysql
import pandas

#functions
def windowtemplate(title,button,command):
    global idEntry,nameEntry,mobileEntry,emailEntry,addressEntry,genderEntry,dobEntry,win
    win = Toplevel()
    win.config(bg='#89defb')
    win.geometry('490x520+350+80')
    win.title(title)
    win.resizable(False, False)
    win.grab_set()
    idlabel = Label(win, text='Id', bg='#89defb', font=('papyrus', 15))
    idlabel.grid(row=0, column=0, sticky=W, padx=10)
    idEntry = Entry(win, font=('papyrus', 12), bd=2, width=35)  # ,state=DISABLED)
    idEntry.grid(row=0, column=1, padx=20, pady=20)

    namelabel = Label(win, text='Name', bg='#89defb', font=('papyrus', 15))
    namelabel.grid(row=1, column=0, sticky=W, padx=10, pady=10)
    nameEntry = Entry(win, font=('papyrus', 12), bd=2, width=35)
    nameEntry.grid(row=1, column=1, padx=20, pady=20)

    mobilelabel = Label(win, text='Mobile No.', bg='#89defb', font=('papyrus', 15))
    mobilelabel.grid(row=2, column=0, sticky=W, padx=10, pady=10)
    mobileEntry = Entry(win, font=('papyrus', 12), bd=2, width=35)
    mobileEntry.grid(row=2, column=1, padx=20, pady=20)

    emaillabel = Label(win, text='Email Id', bg='#89defb', font=('papyrus', 15))
    emaillabel.grid(row=3, column=0, sticky=W, padx=10, pady=10)
    emailEntry = Entry(win, font=('papyrus', 12), bd=2, width=35)
    emailEntry.grid(row=3, column=1, padx=20, pady=20)

    addresslabel = Label(win, text='Address', bg='#89defb', font=('papyrus', 15))
    addresslabel.grid(row=4, column=0, sticky=W, padx=10, pady=10)
    addressEntry = Entry(win, font=('papyrus', 12), bd=2, width=35)
    addressEntry.grid(row=4, column=1, padx=20, pady=20)

    genderlabel = Label(win, text='Gender', bg='#89defb', font=('papyrus', 15))
    genderlabel.grid(row=5, column=0, sticky=W, padx=10, pady=10)
    genderEntry = Entry(win, font=('papyrus', 12), bd=2, width=35)
    genderEntry.grid(row=5, column=1, padx=20, pady=20)

    doblabel = Label(win, text='D.O.B', bg='#89defb', font=('papyrus', 15))
    doblabel.grid(row=6, column=0, sticky=W, padx=10, pady=10)
    dobEntry = Entry(win, font=('papyrus', 12), bd=2, width=35)
    dobEntry.grid(row=6, column=1, padx=20, pady=20)

    button = Button(win, text=button, \
                          font=('papyrus', 15), bg="#d0f2fc", activebackground='#d0f2fc',
                    activeforeground='black',
                          cursor='hand2', command=command)
    button.grid(row=7, columnspan=2)

    if title=="Update Student":
        try:
            indexing = studenttable.focus()  # unique index given to focused para
            content = studenttable.item(indexing)
            # item is a dictionary {'text':'','image':'','values':[all values from id to time]}
            data = content['values']
            idEntry.insert(0, data[0])
            nameEntry.insert(0, data[1])
            mobileEntry.insert(0, data[2])
            emailEntry.insert(0, data[3])
            addressEntry.insert(0, data[4])
            genderEntry.insert(0, data[5])
            dobEntry.insert(0, data[6])
        except:
            messagebox.showerror('Error', 'Select Data To be Updated')


def add_data():
    if idEntry.get()=='' or nameEntry.get()=='' or dobEntry.get()=='' or genderEntry.get()=='' or \
            addressEntry.get()=='' or mobileEntry.get()=='' or emailEntry.get()=='':
        messagebox.showerror('Error','Fields Cannot Be Empty',parent=win)
    else:
        try:
            query = 'insert into student values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(idEntry.get(),nameEntry.get(),mobileEntry.get(),emailEntry.get(),
                             addressEntry.get(),genderEntry.get(),dobEntry.get(),date,currenttime))
            con.commit()
            result=messagebox.askyesno('Confirmation','Student details added successfully,\n '
                                                      'Do you want to add more Students?')

            if result:
                idEntry.delete(0,END)
                addressEntry.delete(0, END)
                mobileEntry.delete(0, END)
                emailEntry.delete(0, END)
                dobEntry.delete(0, END)
                nameEntry.delete(0, END)
                genderEntry.delete(0, END)
            else:
                win.destroy()
        except:
            messagebox.showerror('Error', 'Id already exists', parent=win)
            return

        query='select * from student'
        mycursor.execute(query)
        fetched_data=mycursor.fetchall()
        studenttable.delete(*studenttable.get_children())
        for data in fetched_data:
            studenttable.insert('',END,values=data)#root, append data to end, values

def search_data():
    if idEntry.get()=='' and nameEntry.get()=='' and dobEntry.get()=='' and genderEntry.get()=='' \
            and addressEntry.get()=='' and mobileEntry.get()=='' and emailEntry.get()=='':
        messagebox.showerror('Error','Atleast One Field Should Be Filled',parent=win)
    else:
        query= 'select * from student where id=%s or name=%s or mobile=%s or address=%s or ' \
               'email=%s or gender=%s or dob=%s'
        mycursor.execute(query,(idEntry.get(),nameEntry.get(),mobileEntry.get(),addressEntry.get(),
                                emailEntry.get(),genderEntry.get(),dobEntry.get()))
        studenttable.delete(*studenttable.get_children())
        fetched_data=mycursor.fetchall()
        for data in fetched_data:
            studenttable.insert('',END,values=data)

def deletestudent():
    try:
        indexing=studenttable.focus() #unique index given to focused para
        content=studenttable.item(indexing)
        # item is a dictionary {'text':'','image':'','values':[all values from id to time]}
        id=content['values'][0]
        result = messagebox.askyesno('Confirm', 'Do you really want to delete this record?')
        if not result:
            return
        query='delete from student where id=%s'
        mycursor.execute(query,id)
        con.commit() #commit for crud operations
        messagebox.showinfo('Deleted',f'Id {id} is deleted successfully')
        showstudent()
    except:
        messagebox.showerror('Error','Select Data to be deleted')

def showstudent():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studenttable.delete(*studenttable.get_children())
    for data in fetched_data:
        studenttable.insert('', END, values=data)

def update_data():
        query='update student set name=%s,mobile=%s,email=%s,address=%s,gender=%s,' \
              'dob=%s,date=%s,time=%s where id=%s'
        mycursor.execute(query,(nameEntry.get(),mobileEntry.get(),emailEntry.get(),
                                addressEntry.get(),genderEntry.get(),dobEntry.get(),date,currenttime,idEntry.get()))
        con.commit()
        messagebox.showinfo('Success',f"Id {idEntry.get()} modified successfully",parent=win)
        win.destroy()
        showstudent()

def export_data():
    try:
        url = filedialog.asksaveasfilename(defaultextension='.csv')
        indexing = studenttable.get_children()
        newlist = []
        for index in indexing:
            content = studenttable.item(index)
            datalist = content['values']
            newlist.append(datalist)
        table=pandas.DataFrame(newlist,columns=['Id',"Name","Mobile",'Email','Address','Gender',
                                                'DOB','Added Date','Added Time'])
        table.to_csv(url,index=False)
        messagebox.showinfo('Success','Data is saved successfully')
    except:
        return

def exit():
    result=messagebox.askyesno('Confirm','Do you want to exit?')
    if result:
        root.destroy()

def connect_database():
    def connect():
        global mycursor,con
        try:
            con = pymysql.connect(host=hostEntry.get(), user=usernameEntry.get(), password=passwordEntry.get())
            mycursor=con.cursor()
            messagebox.showinfo('Success','Connection established Successfully',parent=connectWindow)
            #parent is window on which it appears
            try:
                query = 'create database studentmanagementsystem'
                mycursor.execute(query)
                query = 'use studentmanagementsystem'
                mycursor.execute(query)
                query = 'create table student(id int not null primary key, name varchar(50),mobile varchar(50),' \
                        'email varchar(30),address varchar(100),gender varchar(20),dob varchar(30),' \
                        'date varchar(50),time varchar(50))'
                mycursor.execute(query)
            except:
                query = 'use StudentManagementSystem'
                mycursor.execute(query)
            connectWindow.destroy()
            addstudentbutton.config(state=NORMAL)
            deletestudentbutton.config(state=NORMAL)
            updatestudentbutton.config(state=NORMAL)
            exportstudentbutton.config(state=NORMAL)
            showstudentbutton.config(state=NORMAL)
            searchstudentbutton.config(state=NORMAL)
        except:
            messagebox.showerror("Error","Invalid Credentials",parent=connectWindow) #title and content

    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+550+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0, 0)
    connectWindow.config(bg='#89defb')

    hostnameLabel = Label(connectWindow, text='Host Name', bg='#89defb', font=('papyrus', 15))
    hostnameLabel.grid(row=0, column=0, padx=10, pady=10)

    hostEntry = Entry(connectWindow, font=('papyrus', 12), bd=2, width=32)
    hostEntry.grid(row=0, column=1,  padx=20, pady=20)

    usernameLabel = Label(connectWindow, text='User Name',bg='#89defb', font=('papyrus', 15))
    usernameLabel.grid(row=1, column=0, padx=10, pady=10)

    usernameEntry = Entry(connectWindow, font=('papyrus', 12), bd=2, width=32)
    usernameEntry.grid(row=1, column=1,  padx=20, pady=20)

    passwordLabel = Label(connectWindow, text='Password', bg='#89defb', font=('papyrus', 15))
    passwordLabel.grid(row=2, column=0,padx=10, pady=10)

    passwordEntry = Entry(connectWindow,show='*', font=('papyrus', 12), bd=2, width=32)
    passwordEntry.grid(row=2, column=1, padx=20, pady=20)

    button = Button(connectWindow, text='Connect', \
                    font=('papyrus', 15), bg="#d0f2fc", activebackground='#d0f2fc', activeforeground='black',
                    cursor='hand2', command=connect)
    button.grid(row=3, columnspan=2)


count=0
text=''
def slider():
    global text,count
    if count==len(s):
        text=''
        count=0
    text=text+s[count]
    smslabel.config(text=text)
    count+=1

    smslabel.after(100, slider)

def clock():
    global date,currenttime
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimelabel.config(text=f'   Date: {date}\nTime: {currenttime}')
    datetimelabel.after(1000,clock)#call every second

#gui
root=ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('adapta')

root.geometry('1125x800+0+0')
root.title('Student Management System')
root.resizable(False,False)

bgimg=ImageTk.PhotoImage(file='static/mainpagebg.jpg')
bglabel=Label(root,image=bgimg)
bglabel.place(x=0,y=0)

datetimelabel=Label(root,font=('papyrus',15),bg="#89defb")
root.wm_attributes('-transparentcolor','grey')
datetimelabel.place(x=5,y=5)

clock()

s='Student Management System'
smslabel=Label(root,text=s,font=('arial',25,'italic'),bg="#d0f2fc")
smslabel.place(x=400,y=0)
slider()

connectbutton=Button(root,text='Connect To Database',font=('papyrus',15),bg="#d0f2fc",\
                     activebackground='#d0f2fc',activeforeground='black',cursor='hand2',command=connect_database)
connectbutton.place(x=900,y=10)

leftframe=Frame(root,bg="#d0f2fc")
leftframe.place(x=20,y=80)

logoimg=PhotoImage(file='static/mainpagestudentm.png')
logolabel=Label(leftframe,image=logoimg,bg='#d0f2fc')
logolabel.grid(row=0,column=0)

logoimg2=PhotoImage(file='static/mainpagestudentg.png')
logolabel=Label(leftframe,image=logoimg2,bg='#d0f2fc')
logolabel.grid(row=0,column=1)

addstudentbutton=Button(leftframe,width=25,text='Add Student',font=('papyrus',15),bg="#97e3fd",
                        activebackground='#d0f2fc',activeforeground='black',cursor='hand2',state=DISABLED,
                        command=lambda :windowtemplate('Add Student','Add',add_data))
addstudentbutton.grid(row=1,column=0,pady=20,columnspan=2)

searchstudentbutton=Button(leftframe,width=25,text='Search Student',font=('papyrus',15),bg="#97e3fd",
                           activebackground='#d0f2fc',activeforeground='black',cursor='hand2',state=DISABLED,
                           command=lambda :windowtemplate('Search Student','Search',search_data))
searchstudentbutton.grid(row=2,column=0,pady=20,columnspan=2)

deletestudentbutton=Button(leftframe,width=25,text='Delete Student',font=('papyrus',15),bg="#97e3fd",
                           activebackground='#d0f2fc',activeforeground='black',cursor='hand2',state=DISABLED,
                           command=deletestudent)
deletestudentbutton.grid(row=3,column=0,pady=20,columnspan=2)

updatestudentbutton=Button(leftframe,width=25,text='Update Student',font=('papyrus',15),bg="#97e3fd",
                           activebackground='#d0f2fc',activeforeground='black',cursor='hand2',state=DISABLED,
                           command=lambda :windowtemplate('Update Student','Update',update_data))
updatestudentbutton.grid(row=4,column=0,pady=20,columnspan=2)

showstudentbutton=Button(leftframe,width=25,text='Show Students',font=('papyrus',15),bg="#97e3fd",
                         activebackground='#d0f2fc',activeforeground='black',cursor='hand2',state=DISABLED,command=showstudent)
showstudentbutton.grid(row=5,column=0,pady=20,columnspan=2)

exportstudentbutton=Button(leftframe,width=25,text='Export Student',font=('papyrus',15),bg="#97e3fd",
                           activebackground='#d0f2fc',activeforeground='black',cursor='hand2',state=DISABLED,command=export_data)
exportstudentbutton.grid(row=6,column=0,pady=20,columnspan=2)

exitbutton=Button(leftframe,width=25,text='Exit Student',font=('papyrus',15),bg="#97e3fd",
                  activebackground='#d0f2fc',activeforeground='black',cursor='hand2',command=exit)
exitbutton.grid(row=7,column=0,pady=20,columnspan=2)

rightframe=Frame(root,bg='#d0f2fc')
rightframe.place(x=350,y=80,width=760,height=690)

scrollx=Scrollbar(rightframe,orient=HORIZONTAL)
scrolly=Scrollbar(rightframe,orient=VERTICAL)

style=ttk.Style()
#style.theme_use(adapta)
style.configure("Treeview",font=('Papyrus',12),background='#d0f2fc',foreground='black',rowheight=25,fieldbackground='#d0f2fc')
style.configure("Treeview.Heading",font=('Papyrus',14,'bold'))

studenttable=ttk.Treeview(rightframe,columns=('Id','Name','Mobile No.','Email Id','Address','Gender','D.O.B','Added Date','Added Time'),
                          xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)

scrollx.config(command=studenttable.xview)
scrolly.config(command=studenttable.yview)

scrollx.pack(side=BOTTOM,fill=X)
scrolly.pack(side=RIGHT,fill=Y)

studenttable.pack(fill=BOTH,expand=1)

studenttable.heading('Id',text='Id')
studenttable.heading('Name',text='Name')
studenttable.heading('Mobile No.',text='Mobile No.')
studenttable.heading('Email Id',text='Email Id')
studenttable.heading('Address',text='Address')
studenttable.heading('Gender',text='Gender')
studenttable.heading('D.O.B',text='D.O.B')
studenttable.heading('Added Date',text='Added Date')
studenttable.heading('Added Time',text='Added Time')

studenttable.config(show='headings')

studenttable.column('Id',width=50,anchor=CENTER)
studenttable.column('Name',width=200,anchor=CENTER)
studenttable.column('Mobile No.',width=200,anchor=CENTER)
studenttable.column('Email Id',width=400,anchor=CENTER)
studenttable.column('Address',width=300,anchor=CENTER)
studenttable.column('Gender',width=200,anchor=CENTER)
studenttable.column('D.O.B',width=200,anchor=CENTER)
studenttable.column('Added Date',width=200,anchor=CENTER)
studenttable.column('Added Time',width=200,anchor=CENTER)


root.mainloop()