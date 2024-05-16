import tkinter as tk
from tkinter import messagebox
import bcrypt
import json
import os
from PIL import Image, ImageTk

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Login')
        self.root.geometry('1166x718')
        self.root.config(bg='#001220')
        
        self.font1 = ('Helvetica', 25, 'bold')
        self.font2 = ('Arial', 17, 'bold')
        self.font3 = ('Arial', 13, 'bold')
        self.font4 = ('Arial', 17, 'bold', 'underline')

        self.current_user = None  # To store the logged-in username

        # Load the image and save reference
        self.image_path = "C:\\Users\\hp\\Desktop\\login system\\Untitled design.png"
        self.photo = None
        self.load_image()

        self.show_signup_frame()

    def get_data_file_path(self):
        base_dir = os.path.dirname(__file__)
        return os.path.join(base_dir, "data.json")

    def save_data(self, data):
        with open(self.get_data_file_path(), "w") as file:
            json.dump(data, file)

    def load_data(self):
        try:
            data_file_path = self.get_data_file_path()
            if not os.path.exists(data_file_path) or os.stat(data_file_path).st_size == 0:
                with open(data_file_path, "w") as file:
                    json.dump({}, file)
                return {}
            with open(data_file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def load_image(self):
        image = Image.open(self.image_path)
        image = image.resize((500, 718))  # Sesuaikan ukuran gambar
        self.photo = ImageTk.PhotoImage(image)

    def add_image_to_frame(self, frame):
        image_label = tk.Label(frame, image=self.photo, bg='#001220')
        image_label.place(relx=0.8, rely=0.5, anchor=tk.CENTER)

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        data = self.load_data()
        if username != '' and password != '':
            if username in data:
                messagebox.showerror('Error', 'Username Telah Digunakan. Coba Username Lain.')
            else:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                data[username] = {"password": hashed_password.decode('utf-8'), "courses": []}
                self.save_data(data)
                messagebox.showinfo('Success', 'Akun Berhasil Dibuat')
                self.show_login_frame()
        else:
            messagebox.showerror('Error', 'Enter all data.')

    def save_courses(self):
        name = self.name_entry.get()
        nim = self.nim_entry.get()
        courses = [entry.get() for entry in self.course_entries]

        data = self.load_data()
        if name and nim and self.current_user and all(courses):
            if self.current_user in data:
                data[self.current_user]["name"] = name
                data[self.current_user]["nim"] = nim
                data[self.current_user]["courses"] = courses
                self.save_data(data)
                messagebox.showinfo('Success', 'Courses have been saved.')
                self.show_login_frame()
            else:
                messagebox.showerror('Error', 'Invalid username.')
        else:
            messagebox.showerror('Error', 'Please fill in all fields.')

    def login(self):
        username = self.username_login_entry.get()
        password = self.password_login_entry.get()
        data = self.load_data()
        if username != '' and password != '':
            if username in data and bcrypt.checkpw(password.encode('utf-8'), data[username]['password'].encode('utf-8')):
                messagebox.showinfo('Success', 'Login Berhasil.')
                self.current_user = username  # Store the logged-in username
                self.show_course_input_frame()
            else:
                messagebox.showerror('Error', 'Password atau Username Invalid')
        else:
            messagebox.showerror('Error', 'Enter all data.')

    def show_signup_frame(self):
        self.clear_frame()
        frame1 = tk.Frame(self.root, bg='#001220', width=583, height=718)
        frame1.place(x=0, y=0)

        signup_label = tk.Label(frame1, font=self.font1, text='Sign Up Akun Mahasiswa', bg='#001220', fg='#fff')
        signup_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        username_label = tk.Label(frame1, font=self.font3, text='Username:', bg='#001220', fg='#fff')
        username_label.place(relx=0.1, rely=0.3, anchor=tk.W)

        self.username_entry = tk.Entry(frame1, font=self.font2, fg='#FFFFFF', bg='#121111', insertbackground='#fff')
        self.username_entry.place(relx=0.3, rely=0.3, anchor=tk.W)

        password_label = tk.Label(frame1, font=self.font3, text='Password:', bg='#001220', fg='#fff')
        password_label.place(relx=0.1, rely=0.45, anchor=tk.W)

        self.password_entry = tk.Entry(frame1, font=self.font2, show='*', fg='#FFFFFF', bg='#121111', insertbackground='#fff')
        self.password_entry.place(relx=0.3, rely=0.45, anchor=tk.W)

        signup_button = tk.Button(frame1, command=self.signup, font=self.font2, text='Sign up', fg='#fff', bg='#00965d', activebackground='#006e44', width=12)
        signup_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        login_label = tk.Label(frame1, font=self.font3, text='Apakah sudah memiliki akun?', bg='#001220', fg='#fff')
        login_label.place(relx=0.5, rely=0.70, anchor=tk.CENTER)

        login_button = tk.Button(frame1, command=self.show_login_frame, font=self.font4, text='Login', fg='#fff', bg='#00965d', activebackground='#001220', width=8)
        login_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
        
        self.add_image_to_frame(self.root)  # Menampilkan gambar di frame signup

    def show_login_frame(self):
        self.clear_frame()
        frame2 = tk.Frame(self.root, bg='#001220', width=583, height=718)
        frame2.place(x=0, y=0)

        login_label2 = tk.Label(frame2, font=self.font1, text='Log in', bg='#001220', fg='#fff')
        login_label2.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        username_label2 = tk.Label(frame2, font=self.font3, text='Username:', bg='#001220', fg='#fff')  # Perbaikan penulisan
        username_label2.place(relx=0.1, rely=0.3, anchor=tk.W)

        password_label2 = tk.Label(frame2, font=self.font3, text='Password:', bg='#001220', fg='#fff')
        password_label2.place(relx=0.1, rely=0.45, anchor=tk.W)

        self.username_login_entry = tk.Entry(frame2, font=self.font2, fg='#fff', bg='#121111', insertbackground='#fff')
        self.username_login_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.password_login_entry = tk.Entry(frame2, font=self.font2, show='*', fg='#fff', bg='#121111', insertbackground='#fff')
        self.password_login_entry.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        login_button2 = tk.Button(frame2, command=self.login, font=self.font2, text='Login', fg='#fff', bg='#00965d', activebackground='#006e44', width=12)
        login_button2.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.add_image_to_frame(self.root)  # Menampilkan gambar di frame login

    def show_course_input_frame(self):
        self.clear_frame()
        frame3 = tk.Frame(self.root, bg='#001220', width=700, height=600)
        frame3.place(x=233, y=59)

        name_label = tk.Label(frame3, font=self.font3, text='Name:', bg='#001220', fg='#fff')
        name_label.place(x=20, y=20)
        self.name_entry = tk.Entry(frame3, font=self.font2, fg='#FFFFFF', bg='#121111', insertbackground='#fff', width=30)
        self.name_entry.place(x=120, y=20)

        nim_label = tk.Label(frame3, font=self.font3, text='NIM:', bg='#001220', fg='#fff')
        nim_label.place(x=20, y=70)
        self.nim_entry = tk.Entry(frame3, font=self.font2, fg='#FFFFFF', bg='#121111', insertbackground='#fff', width=30)
        self.nim_entry.place(x=120, y=70)

        course_labels = ['Course 1:', 'Course 2:', 'Course 3:', 'Course 4:', 'Course 5:', 'Course 6:', 'Course 7:', 'Course 8:', 'Course 9:', 'Course 10:', 'Course 11:', 'Course 12:', 'Course 13:', 'Course 14:', 'Course 15:']
        self.course_entries = []

        for i, course_label in enumerate(course_labels):
            label = tk.Label(frame3, font=self.font3, text=course_label, bg='#001220', fg='#fff')
            label.place(x=20, y=120 + i * 30)
            entry = tk.Entry(frame3, font=self.font2, fg='#FFFFFF', bg='#121111', insertbackground='#fff', width=30)
            entry.place(x=120, y=120 + i * 30)
            self.course_entries.append(entry)

        save_button = tk.Button(frame3, command=self.save_courses, font=self.font2, text='Save', fg='#fff', bg='#00965d', activebackground='#006e44', width=12)
        save_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        
        self.add_image_to_frame(self.root)  # Menampilkan gambar di frame input course

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
