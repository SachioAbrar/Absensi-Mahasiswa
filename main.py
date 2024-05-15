import tkinter as tk
from tkinter import messagebox
import sqlite3
import bcrypt
from PIL import Image, ImageTk


app = tk.Tk()
app.title('Login')
app.geometry('1166x718') 
app.config(bg='#001220')

screen_height = app.winfo_screenheight()
window_height = 718
window_y = (screen_height // 2) - (window_height // 2)

# Load the image
image_path = "C:\\Users\\hp\\Desktop\\login system\\Untitled design.png"  # Ubah dengan path gambar Anda
image = Image.open(image_path)
image = image.resize((500, 718))  # Sesuaikan ukuran gambar
photo = ImageTk.PhotoImage(image)

# Tampilkan gambar dalam label di samping frame utama
image_label = tk.Label(app, image=photo)
image_label.place(relx=0.8, rely=0.5, anchor=tk.CENTER)


font1 = ('Helvetica', 25, 'bold')
font2 = ('Arial', 17, 'bold')
font3 = ('Arial', 13, 'bold')
font4 = ('Arial', 17, 'bold', 'underline')

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT NOT NULL,
        password TEXT NOT NULL)''')

def signup():
    username = username_entry.get()
    password = password_entry.get()
    if username != '' and password != '':
        cursor.execute('SELECT username FROM users WHERE username=?', (username,))
        if cursor.fetchone() is not None:
            messagebox.showerror('Error', 'Username Telah Digunakan. Coba Username Lain.')
        else:
            encoded_password = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            messagebox.showinfo('Success', 'Akun Berhasil Dibuat')
    else:
        messagebox.showerror('Error', 'Enter all data.')


def login():
    username = username_login_entry.get()
    password = password_login_entry.get()
    if username != '' and password != '':
        cursor.execute('SELECT password FROM users WHERE username=?', (username,))
        result = cursor.fetchone()
        if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
            messagebox.showinfo('Success', 'Login Berhasil.')
        else:
            messagebox.showerror('Error', 'Password atau Username Invalid')
    else:
        messagebox.showerror('Error', 'Enter all data.')

def show_login_frame():
    frame1.destroy()
    frame2 = tk.Frame(app, bg='#001220', width=583, height=718) 
    frame2.place(x=0, y=0)

    login_label2 = tk.Label(frame2, font=font1, text='Log in', bg='#001220', fg='#fff')
    login_label2.place(relx=0.5, rely=0.1, anchor=tk.CENTER) 
    
    global username_login_entry, password_login_entry
    username_login_entry = tk.Entry(frame2, font=font2, show='', fg='#fff', bg='#121111', insertbackground='#fff')
    username_login_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)  

    password_login_entry = tk.Entry(frame2, font=font2, show='*', fg='#fff', bg='#121111', insertbackground='#fff')
    password_login_entry.place(relx=0.5, rely=0.45, anchor=tk.CENTER)  

    login_button2 = tk.Button(frame2, command=login, font=font2, text='Login', fg='#fff', bg='#00965d', activebackground='#006e44', width=12)
    login_button2.place(relx=0.5, rely=0.6, anchor=tk.CENTER)  
    

frame1 = tk.Frame(app, bg='#001220', width=583, height=718)  
frame1.place(x=0, y=0)

signup_label = tk.Label(frame1, font=font1, text='Sign Up Akun Mahasiswa', bg='#001220', fg='#fff')
signup_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)  

username_label = tk.Label(frame1, font=font3, text='Username:', bg='#001220', fg='#fff')
username_label.place(relx=0.1, rely=0.3, anchor=tk.W)  
username_entry = tk.Entry(frame1, font=font2, fg='#FFFFFF', bg='#121111', insertbackground='#fff')
username_entry.place(relx=0.3, rely=0.3, anchor=tk.W)  

password_label = tk.Label(frame1, font=font3, text='Password:', bg='#001220', fg='#fff')
password_label.place(relx=0.1, rely=0.45, anchor=tk.W)  

password_entry = tk.Entry(frame1, font=font2, show='*', fg='#FFFFFF', bg='#121111', insertbackground='#fff')
password_entry.place(relx=0.3, rely=0.45, anchor=tk.W)  



signup_button = tk.Button(frame1, command=signup, font=font2, text='Sign up', fg='#fff', bg='#00965d', activebackground='#006e44', width=12)
signup_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER) 

login_label = tk.Label(frame1, font=font3, text='Apakah sudah memiliki akun?', bg='#001220', fg='#fff')
login_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

login_button = tk.Button(frame1, command=show_login_frame, font=font4, text='Login', fg='#00bf77', bg='#001220', activebackground='#001220', width=8)
login_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER) 

app.mainloop()

