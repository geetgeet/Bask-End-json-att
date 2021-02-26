from tkinter import *
from tkinter import messagebox


window =Tk()
window.title("Log in verifier")
window.geometry("300x300")
lbl_user=Label(window, text="Username")
lbl_user.pack()
user_entry=Entry(window, textvariable="username")
user_entry.pack()
pass_label=Label(window, text="Password")
pass_label.pack()
pass_entry=Entry(window, textvariable="password", show="*")
pass_entry.pack()
def check():
    all_logs={"user":"1","Blue":"123", "Red":"12345", "Black": "54321","Godwin":"12345"}
    myuser=request.form['username']
    password=re
    if (myuser, password)in all_logs.items():
        messagebox.showinfo("INFO", "Correct Login")
        window.withdraw()
        import MalaisiaTask
        MalaisiaTask()



    else:
        messagebox.showinfo("INFO", "Incorrect Login")
        user_entry.delete(0, END)
        pass_entry.delete(0, END)





mybutton= Button(window, text="Login ", bg="yellow", command=check).pack()
window.mainloop()
