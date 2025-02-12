from tkinter import *
from tkinter import messagebox
import sqlite3

f = ('Times', 14)

con = sqlite3.connect('userdata.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS record(
                    name text, 
                    email text, 
                    contact number, 
                    gender text, 
                    password text
                )
            ''')
con.commit()

            

ws = Tk()
ws.title('PythonGuides')
ws.geometry('940x500')
ws.config(bg='#CCCCCC')


def insert_record():
    check_counter=0
    warn = ""
    if register_name.get() == "":
       warn = "Name can't be empty"
    else:
        check_counter += 1
    # if register_name.get() == int(register_name.get()):==============Пока что в разработке
    #    warn = "the name must consist of letters"=====================Пока что в разработке
    # else:============================================================Пока что в разработке
    #     check_counter += 1  =========================================Пока что в разработке
    if register_email.get() == "":
        warn = "Email can't be empty"
    else:
        check_counter += 1
    # if cur.execute(f'''SELECT COUNT({register_mobile.get()} from record)''') > 1: =========Пока что в разработке
    #     warn = 'this number has already been registered'===================================Пока что в разработке
    # else:==================================================================================Пока что в разработке
    #     check_counter += 1=================================================================Пока что в разработке
    if register_mobile.get() == "":
       warn = "Contact can't be empty"
    else:
        check_counter += 1
    if len(register_mobile.get()) < 11:
       warn = "Cheating is bad, enter your real number"
    else:
        check_counter += 1
    if len(register_pwd.get()) < 6:
       warn = "our team believes that your password is too small, it should be changed :)"
    else:
        check_counter += 1
    if  var.get() == "":
        warn = "Select Gender"
    else:
        check_counter += 1
    if register_pwd.get() == "":
        warn = "Password can't be empty"
    else:
        check_counter += 1

    if pwd_again.get() == "":
        warn = "Re-enter password can't be empty"
    else:
        check_counter += 1

    if register_pwd.get() != pwd_again.get():
        warn = "Passwords didn't match"
    else:
        check_counter += 1
    if check_counter == 9:        
        try:
            con = sqlite3.connect('userdata.db')
            cur = con.cursor()
            cur.execute("INSERT INTO record VALUES (:name, :email, :contact, :gender, :password)", {
                            'name': register_name.get(),
                            'email': register_email.get(),
                            'contact': register_mobile.get(),
                            'gender': var.get(),
                            'password': register_pwd.get()

            })
            con.commit()
            messagebox.showinfo('confirmation', 'Record Saved')

        except Exception as ep:
            messagebox.showerror('', ep) 
    else:
        messagebox.showerror('Error', warn)

def login_response():
    utel = utel_tf.get()
    uname = email_tf.get()
    upwd = pwd_tf.get()
    check_counter=0
    try:
        con = sqlite3.connect('userdata.db')
        c = con.cursor()
        for row in c.execute(f"Select * from record where contact = {utel}"):
            tel = str(row[2])
            pwd = row[4]
    except Exception as ep:
        messagebox.showerror('', ep)    
    if utel == "":
       warn = "Phone number can't be empty"
    else:
        check_counter += 1
    if upwd == "":
        warn = "Password can't be empty"
    else:
        check_counter += 1
    if check_counter == 2:
        if (utel == tel and upwd == pwd):
            messagebox.showinfo('Login Status', 'Logged in Successfully!')
        
        else:
            messagebox.showerror('Login Status', 'invalid username or password')
    else:
        messagebox.showerror('', warn)
    print(type(tel), type(utel))
    print(type(pwd), type(upwd))
    
var = StringVar()
var.set('male')
variable = StringVar()
left_frame = Frame(
    ws, 
    bd=2, 
    bg='#CCCCCC',   
    relief=SOLID, 
    padx=10, 
    pady=10
    )


Label(
    left_frame, 
    text="Enter Phone number", 
    bg='#CCCCCC',
    font=f).grid(row=0, column=0, sticky=W, pady=10)


Label(
    left_frame, 
    text="Enter Password", 
    bg='#CCCCCC',
    font=f
    ).grid(row=1, column=0, pady=10)


email_tf = Entry(
    left_frame, 
    font=f
    )
utel_tf = Entry(
    left_frame, 
    font=f
    )
tel_tf = Entry(
    left_frame, 
    font=f
    )
pwd_tf = Entry(
    left_frame, 
    font=f,
    show='*'
    )
login_btn = Button(
    left_frame, 
    width=15, 
    text='Login', 
    font=f, 
    relief=SOLID,
    cursor='hand2',
    command=login_response
    )
right_frame = Frame(
    ws, 
    bd=2, 
    bg='#CCCCCC',
    relief=SOLID, 
    padx=10, 
    pady=10
    )


Label(
    right_frame, 
    text="Enter Name", 
    bg='#CCCCCC',
    font=f
    ).grid(row=0, column=0, sticky=W, pady=10)


Label(
    right_frame, 
    text="Enter Email", 
    bg='#CCCCCC',
    font=f
    ).grid(row=1, column=0, sticky=W, pady=10)


Label(
    right_frame, 
    text="Contact Number", 
    bg='#CCCCCC',
    font=f
    ).grid(row=2, column=0, sticky=W, pady=10)


Label(
    right_frame, 
    text="Select Gender", 
    bg='#CCCCCC',
    font=f
    ).grid(row=3, column=0, sticky=W, pady=10)



Label(
    right_frame, 
    text="Enter Password", 
    bg='#CCCCCC',
    font=f
    ).grid(row=5, column=0, sticky=W, pady=10)


Label(
    right_frame, 
    text="Re-Enter Password", 
    bg='#CCCCCC',
    font=f
    ).grid(row=6, column=0, sticky=W, pady=10)


gender_frame = LabelFrame(
    right_frame,
    bg='#CCCCCC',
    padx=10, 
    pady=10,
    )


register_name = Entry(
    right_frame, 
    font=f
    )

register_email = Entry(
    right_frame, 
    font=f
    )

register_mobile = Entry(
    right_frame, 
    font=f
    )


male_rb = Radiobutton(
    gender_frame, 
    text='Male',
    bg='#CCCCCC',
    variable=var,
    value='male',
    font=('Times', 10),    

)

female_rb = Radiobutton(
    gender_frame,
    text='Female',
    bg='#CCCCCC',
    variable=var,
    value='female',
    font=('Times', 10),
  
)

others_rb = Radiobutton(
    gender_frame,
    text='Others',
    bg='#CCCCCC',
    variable=var,
    value='others',
    font=('Times', 10)
   
)

register_pwd = Entry(
    right_frame, 
    font=f,
    show='*'
)
pwd_again = Entry(
    right_frame, 
    font=f,
    show='*'
)

register_btn = Button(
    right_frame, 
    width=15, 
    text='Register', 
    font=f, 
    relief=SOLID,
    cursor='hand2',
    command=insert_record
)


utel_tf.grid(row=0, column=1, pady=10, padx=20)
pwd_tf.grid(row=1, column=1, pady=10, padx=20)
login_btn.grid(row=2, column=1, pady=10, padx=20)
left_frame.place(x=50, y=50)
register_name.grid(row=0, column=1, pady=10, padx=20)
register_email.grid(row=1, column=1, pady=10, padx=20) 
register_mobile.grid(row=2, column=1, pady=10, padx=20)
register_pwd.grid(row=5, column=1, pady=10, padx=20)
pwd_again.grid(row=6, column=1, pady=10, padx=20)
register_btn.grid(row=7, column=1, pady=10, padx=20)
right_frame.place(x=500, y=50)

gender_frame.grid(row=3, column=1, pady=10, padx=20)
male_rb.pack(expand=True, side=LEFT)
female_rb.pack(expand=True, side=LEFT)
others_rb.pack(expand=True, side=LEFT)

ws.mainloop()
