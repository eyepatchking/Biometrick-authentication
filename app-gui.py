from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, PhotoImage
import os

names = set()


class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        # BUG FIX 1: nameslist.txt mavjud bo'lmasa yaratish
        if os.path.exists("nameslist.txt"):
            with open("nameslist.txt", "r") as f:
                x = f.read().strip()
                if x:
                    for i in x.split(" "):
                        if i:
                            names.add(i)
        else:
            open("nameslist.txt", "w").close()

        # BUG FIX 2: classifiers papkasi mavjud bo'lmasa yaratish
        os.makedirs("./data/classifiers", exist_ok=True)

        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Face Recognizer")
        self.resizable(False, False)
        self.geometry("500x250")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        # BUG FIX 3: num_of_images atributi boshlang'ich qiymat olishi kerak
        self.num_of_images = 0

        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            with open("nameslist.txt", "w") as f:
                for i in names:
                    f.write(i + " ")
            self.destroy()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # BUG FIX 4: homepagepic.png mavjud bo'lmasa xato bermaslik
        try:
            render = PhotoImage(file='homepagepic.png')
            img = tk.Label(self, image=render)
            img.image = render
            img.grid(row=0, column=1, rowspan=4, sticky="nsew")
        except Exception:
            pass

        label = tk.Label(self, text="        Home Page        ",
                         font=self.controller.title_font, fg="#263942")
        label.grid(row=0, sticky="ew")
        button1 = tk.Button(self, text="   Sign up  ", fg="#ffffff", bg="#263942",
                            command=lambda: self.controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="   Check a User  ", fg="#ffffff", bg="#263942",
                            command=lambda: self.controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff",
                            command=self.on_closing)
        button1.grid(row=1, column=0, ipady=3, ipadx=7)
        button2.grid(row=2, column=0, ipady=3, ipadx=2)
        button3.grid(row=3, column=0, ipady=3, ipadx=32)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            with open("nameslist.txt", "w") as f:
                for i in names:
                    f.write(i + " ")
            self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Enter the name", fg="#263942",
                 font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942",
                                    command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg="#263942",
                                   command=self.start_training)
        self.buttonclear = tk.Button(self, text="Clear", command=self.clear,
                                     fg="#ffffff", bg="#263942")
        self.buttoncanc.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)
        self.buttonclear.grid(row=1, ipadx=5, ipady=4, column=2, pady=10)

    def start_training(self):
        global names
        name = self.user_name.get().strip()
        if name == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif name in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(name) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")

    def clear(self):
        self.user_name.delete(0, 'end')


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        tk.Label(self, text="Select your username", fg="#263942",
                 font='Helvetica 12 bold').grid(row=0, column=0, padx=10, pady=10)
        self.menuvar = tk.StringVar(self)
        # BUG FIX 5: names bo'sh bo'lsa OptionMenu xato beradi
        name_list = list(names) if names else ["(no users)"]
        self.menuvar.set(name_list[0])
        self.dropdown = tk.OptionMenu(self, self.menuvar, *name_list)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttoncanc = tk.Button(self, text="Cancel",
                                    command=lambda: controller.show_frame("StartPage"),
                                    bg="#ffffff", fg="#263942")
        self.buttonclear = tk.Button(self, text="Clear", command=self.clear,
                                     fg="#ffffff", bg="#263942")
        self.buttonext = tk.Button(self, text="Next", command=self.next_foo,
                                   fg="#ffffff", bg="#263942")
        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)
        self.buttonclear.grid(row=1, ipadx=5, ipady=4, column=2, pady=10)

    def next_foo(self):
        selected = self.menuvar.get()
        # BUG FIX 6: dropdown'dan to'g'ri qiymat olish
        if selected in ('None', '(no users)', ''):
            messagebox.showerror("ERROR", "Please select a valid user!")
            return
        # BUG FIX 7: classifier fayli mavjudligini tekshirish
        classifier_path = f"./data/classifiers/{selected}_classifier.xml"
        if not os.path.exists(classifier_path):
            messagebox.showerror("ERROR",
                f"No trained model found for '{selected}'.\nPlease sign up and train the model first.")
            return
        self.controller.active_name = selected
        self.controller.show_frame("PageFour")

    def clear(self):
        self.menuvar.set('')

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name,
                                               command=tk._setit(self.menuvar, name))


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numimglabel = tk.Label(self, text="Number of images captured = 0",
                                    font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff",
                                       bg="#263942", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff",
                                     bg="#263942", command=self.trainmodel)
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    def capimg(self):
        self.numimglabel.config(text="Captured Images = 0")
        messagebox.showinfo("INSTRUCTIONS", "We will capture 300 pictures of your face.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=f"Number of images captured = {x}")

    def trainmodel(self):
        # BUG FIX 8: num_of_images atributiga xavfsiz kirish
        if getattr(self.controller, 'num_of_images', 0) < 300:
            messagebox.showerror("ERROR", "Not enough data! Capture at least 300 images.")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
        self.controller.show_frame("PageFour")


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold')
        label.grid(row=0, column=0, sticky="ew")
        button1 = tk.Button(self, text="Face Recognition", command=self.openwebcam,
                            fg="#ffffff", bg="#263942")
        button4 = tk.Button(self, text="Go to Home Page",
                            command=lambda: self.controller.show_frame("StartPage"),
                            bg="#ffffff", fg="#263942")
        button1.grid(row=1, column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=1, column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        # BUG FIX 9: active_name None bo'lsa xato chiqarish
        if not self.controller.active_name:
            messagebox.showerror("ERROR", "No user selected!")
            return
        main_app(self.controller.active_name)


app = MainUI()
# BUG FIX 10: icon.ico mavjud bo'lmasa crash bo'lmaslik
try:
    app.iconphoto(True, tk.PhotoImage(file='icon.ico'))
except Exception:
    pass
app.mainloop()
