import tkinter as tk
import tkinter.messagebox
from . import ClientLogin


class RegisterWindow:
    def __init__(self, wordy_game):
        self.wordy_game = wordy_game
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.go_to_login)

        self.root.geometry("500x450")
        self.root.configure(bg='#1c2833')

        self.root.title("Wordy Register")

        self.window_width = 500
        self.window_height = 430
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x_position = int((self.screen_width - self.window_width) / 2)
        self.y_position = int((self.screen_height - self.window_height) / 2)
        self.root.geometry(
            "{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_position, self.y_position))

        self.root.resizable(False, False)

        self.wordyLabel = tk.Label(self.root, text="R E G I S T E R", font=('Arial', 25) ,fg='#FCA311', bg='#1c2833')
        self.wordyLabel.pack(padx=20, pady=20)

        # create labels
        self.lbl_username = tk.Label(self.root, text="Username", font=('Arial', 15),  fg='#DBCBD8', bg='#1c2833')
        self.lbl_username.pack(padx=5, pady=15)

        self.entry_username = tk.Entry(self.root, font=('Arial', 16))
        self.entry_username.pack()

        self.lbl_password = tk.Label(self.root, text="Password", font=('Arial', 15), fg='#DBCBD8', bg='#1c2833')
        self.lbl_password.pack(padx=5, pady=15)

        self.entry_password = tk.Entry(self.root, show="*", font=('Arial', 16), )
        self.entry_password.pack()

        self.btn_register = tk.Button(self.root, text="Register", font=('Arial', 15), command=self.register, fg='#0A090C', bg='#DEA54B', width=len("Back to Login"))
        self.btn_register.pack(padx=40, pady=25)

        self.btn_login = tk.Button(self.root, text="Back to Login", font=('Arial', 15), command=self.go_to_login, fg='#0A090C', bg='#DEA54B',width=len("Back to Login"))
        self.btn_login.pack(padx=5, pady=0)

        self.root.mainloop()

    def register(self, result=None):
        username = self.entry_username.get()
        password = self.entry_password.get()
        bool(result)
        result = self.wordy_game.register(username, password)
        if result:
            tkinter.messagebox.showinfo("Congratulations!", "Registered Successfully!")
            self.root.destroy()
            ClientLogin.ClientLogin(self.wordy_game)
        else:
            tkinter.messagebox.showerror("Error", "Please enter a valid username and password")
    def go_to_login(self):
        self.root.destroy()
        ClientLogin.ClientLogin(self.wordy_game)

