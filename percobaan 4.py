import tkinter as tk
from tkinter import messagebox
import sqlite3
import bcrypt

app = tk.Tk()
app.title('Login')
app.geometry('1166x718')  
app.config(bg='#001220')

font1 = ('Helvetica', 25, 'bold')
font2 = ('Arial', 17, 'bold')
font3 = ('Arial', 13, 'bold')
font4 = ('Arial', 17, 'bold', 'underline')

conn = sqlite3.connect('nama_database.db')
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
def save_courses():
    name = name_entry.get()
    nim = nim_entry.get()
    courses = [entry.get() for entry in course_entries]

    if name and nim and all(courses):
        cursor.execute('INSERT INTO users (name, nim, course1, course2, course3, course4, course5, course6, course7, course8, course9, course10, course11) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (name, nim, *courses))
        conn.commit()
        messagebox.showinfo('Success', 'Courses have been saved.')
        show_login_frame()
    else:
        messagebox.showerror('Error', 'Please fill in all fields.')

def show_course_input_frame():
    global name_entry, nim_entry, course_entries  # Global variable declaration

    frame1.destroy()
    frame2 = tk.Frame(app, bg='#001220', width=700, height=600)  # Adjusted width and height
    frame2.place(x=0, y=0)

    # Labels and entry fields for name and NIM
    name_label = tk.Label(frame2, font=font3, text='Name:', bg='#001220', fg='#fff')
    name_label.place(x=20, y=20)
    name_entry = tk.Entry(frame2, font=font2, fg='#FFFFFF', bg='#121111', insertbackground='#fff', width=30)
    name_entry.place(x=120, y=20)

    nim_label = tk.Label(frame2, font=font3, text='NIM:', bg='#001220', fg='#fff')
    nim_label.place(x=20, y=70)
    nim_entry = tk.Entry(frame2, font=font2, fg='#FFFFFF', bg='#121111', insertbackground='#fff', width=30)
    nim_entry.place(x=120, y=70)

    # Labels and entry fields for courses
    course_labels = ['Course 1:', 'Course 2:', 'Course 3:', 'Course 4:', 'Course 5:', 'Course 6:', 'Course 7:', 'Course 8:', 'Course 9:', 'Course 10:', 'Course 11:']
    y_position = 120
    course_entries = []
    for i, label in enumerate(course_labels):
        course_label = tk.Label(frame2, font=font3, text=label, bg='#001220', fg='#fff')
        course_label.place(x=20, y=y_position)
        
        entry = tk.Entry(frame2, font=font2, fg='#FFFFFF', bg='#121111', insertbackground='#fff', width=30)
        entry.place(x=120, y=y_position)
        course_entries.append(entry)
        y_position += 40

    # Save button
    save_button = tk.Button(frame2, command=save_courses, font=font2, text='Save', fg='#fff', bg='#00965d', activebackground='#006e44', width=12)
    save_button.place(x=320, y=y_position)

def login():
    username = username_login_entry.get()
    password = password_login_entry.get()
    if username != '' and password != '':
        cursor.execute('SELECT password FROM users WHERE username=?', (username,))
        result = cursor.fetchone()
        if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
            messagebox.showinfo('Success', 'Login Berhasil.')
            show_course_input_frame()  # Panggil fungsi setelah login berhasil
        else:
            messagebox.showerror('Error', 'Password atau Username Invalid')
    else:
        messagebox.showerror('Error', 'Enter all data.')

def show_login_frame():
    frame1.destroy()
    frame2 = tk.Frame(app, bg='#001220', width=500, height=360)  
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

# Penempatan widget pada frame1, pastikan Anda telah mengatur posisi dengan benar:
frame1 = tk.Frame(app, bg='#001220', width=500, height=360)
frame1.place(x=0, y=0)

username_label = tk.Label(frame1, font=font3, text='Username:', bg='#001220', fg='#fff')
username_label.place(x=50, y=80)  # Menyesuaikan posisi x dan y
username_entry = tk.Entry(frame1, font=font2, fg='#FFFFFF', bg='#121111', insertbackground='#fff')
username_entry.place(x=180, y=80)  # Menyesuaikan posisi x dan y

password_label = tk.Label(frame1, font=font3, text='Password:', bg='#001220', fg='#fff')
password_label.place(x=50, y=130)  # Menyesuaikan posisi x dan y

password_entry = tk.Entry(frame1, font=font2, show='*', fg='#FFFFFF', bg='#121111', insertbackground='#fff')
password_entry.place(x=180, y=130)  # Menyesuaikan posisi x dan y

signup_button = tk.Button(frame1, command=signup, font=font2, text='Sign up', fg='#fff', bg='#00965d', activebackground='#006e44', width=12)
signup_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)  # Geser ke tengah

login_label = tk.Label(frame1, font=font3, text='Apakah sudah memiliki akun?', bg='#001220', fg='#fff')
login_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER) # Geser ke tengah

login_button = tk.Button(frame1, command=show_login_frame, font=font4, text='Login', fg='#00bf77', bg='#001220', activebackground='#001220', width=8)
login_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER) # Geser ke tengah

app.mainloop()