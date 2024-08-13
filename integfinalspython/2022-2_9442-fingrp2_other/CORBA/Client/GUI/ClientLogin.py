
import tkinter as tk
import tkinter.messagebox

from . import ClientRegister, Homepage


class ClientLogin:

    def __init__(self, wordy_game):

        self.wordy_game = wordy_game
        self.root = tk.Tk()

        # to set the window's name to Wordy App
        self.root.title("Wordy App")

        self.root.configure(bg='#1c2833')

        # to set the size of the window
        self.window_width = 500
        self.window_height = 430
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x_position = int((self.screen_width - self.window_width) / 2)
        self.y_position = int((self.screen_height - self.window_height) / 2)
        self.root.geometry(
            "{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_position, self.y_position))

        # to set the root window to non-resizable
        self.root.resizable(False, False)

        # for Wordy Title label
        self.wordy_label = tk.Label(self.root, text="W o r d y", font=('Arial', 25), fg='#DEA54B', bg='#1c2833')
        self.wordy_label.pack(padx=20, pady=20)

        # for username label
        self.username_label = tk.Label(self.root, text="Username", font=('Arial', 15), fg='#DBCBD8', bg='#1c2833')
        self.username_label.pack(padx=5, pady=15)

        # for username textfield
        self.username_entry = tk.Entry(self.root, font=('Arial', 16))
        self.username_entry.pack()

        # for password label
        self.password_label = tk.Label(self.root, text="Password", font=('Arial', 15), fg='#DBCBD8', bg='#1c2833')
        self.password_label.pack(padx=5, pady=15)

        # for password textfield
        self.password_entry = tk.Entry(self.root, font=('Arial', 16), show="*")
        self.password_entry.pack()

        # for login button
        self.login_button = tk.Button(self.root, text="Login", font=('Arial', 15), command=self.click_login, fg='#0A090C', bg='#DEA54B', width=len("Register"))
        self.login_button.pack(padx=30, pady=18)

        # for register button
        self.register_button = tk.Button(self.root, text="Register", font=('Arial', 15), command=self.click_register, fg='#0A090C', bg='#DEA54B', width=len("Register"))
        self.register_button.pack(padx=10, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.root.mainloop()

    def click_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        result = self.wordy_game.login(username, password, "")

        if result == "User is already logged in!" or result == "Invalid username or password!":
            tkinter.messagebox.showinfo("Error", result)
        else:
            tkinter.messagebox.showinfo("Success", result)
            self.root.withdraw()
            # create the homepage window and pass the username and wordy_game object
            Homepage.Homepage(self.wordy_game, username)
            self.root.destroy()

    def click_register(self):
        self.root.destroy()
        ClientRegister.RegisterWindow(self.wordy_game)

    def close_window(self):
        self.wordy_game.logout(self.username_entry.get())
        self.root.destroy()


