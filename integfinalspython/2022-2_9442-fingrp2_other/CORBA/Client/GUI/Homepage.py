import tkinter as tk
from tkinter import messagebox

from . import Leaderboard, WaitingRoom, ClientLogin

class Homepage:

    #  add to constructor wordy_game, username once used
    def __init__(self, wordy_game, username):
        self.wordy_game = wordy_game
        self.username = username
        self.root = tk.Tk()

        # to set the window's name to Wordy App
        self.root.title("Wordy App")
        self.root.configure(bg='#1c2833')

        # to set the size of the window
        self.window_width = 500
        self.window_height = 500
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x_position = int((self.screen_width - self.window_width) / 2)
        self.y_position = int((self.screen_height - self.window_height) / 2)
        self.root.geometry(
            "{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_position, self.y_position))

        # to set the root window to non-resizable
        self.root.resizable(False, False)

        # for Wordy Title label
        self.wordy_label = tk.Label(self.root, text="    W o r d y    G a m e   ", font=('Arial', 25), fg='#FCA311', bg='#1c2833')
        self.wordy_label.pack(padx=20, pady=20)

        # for username label
        # add username
        self.username_label = tk.Label(self.root, text="Hello, " + username + "!  ٩(◕‿◕)۶ ", font=('Arial', 20), fg='#EFF8E2', bg='#1c2833')
        self.username_label.pack(padx=5, pady=15)

        # for start button
        self.start_button = tk.Button(self.root, text="Start", font=('Arial', 18), command=self.click_start, fg='#0A090C', bg='#849324', width=len("Leaderboard"))
        self.start_button.pack(padx=30, pady=10)

        # for join button
        self.join_button = tk.Button(self.root, text="Join", font=('Arial', 18), command=self.click_join, fg='#0A090C', bg='#DEA54B', width=len("Leaderboard"))
        self.join_button.pack(padx=30, pady=10)

        # for leaderboard button
        self.leaderboard_button = tk.Button(self.root, text="Leaderboard", font=('Arial', 18), command=self.click_leaderboard, fg='#0A090C', bg='#DEA54B', width=len("Leaderboard"))
        self.leaderboard_button.pack(padx=30, pady=10)

        # for logout button
        self.logout_button = tk.Button(self.root, text="Logout", font=('Arial', 18), command=self.click_logout, fg='#FFFFFF', bg='#E84855', width=len("Leaderboard"))
        self.logout_button.pack(padx=30, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.root.mainloop()

    def click_start(self):
        self.root.withdraw()
        joined = self.wordy_game.checkWaitingRoomStatus()
        if joined[0] == "Waiting room in session":
            messagebox.showinfo("Notification",
                                "Waiting room is already in session! Please join the current waiting room or wait to "
                                "make a new one")
            self.root.deiconify()
        else:
            self.wordy_game.startNewWaitingRoom()
            self.wordy_game.joinWaitingRoom(self.username)
            WaitingRoom.WaitingRoom(self.wordy_game, self.username)
            self.root.destroy()

    def click_join(self):
        self.root.withdraw()
        joined = self.wordy_game.checkWaitingRoomStatus()
        if joined[0] == "No waiting room in session":
            messagebox.showinfo("Notification", "No waiting room is currently in session!")
            self.root.deiconify()
        elif joined[0] == "Waiting room in session":
            if self.wordy_game.joinWaitingRoom(self.username):
                WaitingRoom.WaitingRoom(self.wordy_game, self.username)
                self.root.destroy()
            else:
                messagebox.showinfo("Notification", "Error joining waiting room!")

    def click_leaderboard(self):
        self.root.withdraw()
        Leaderboard.Leaderboard(self.wordy_game, self.username)
        self.root.destroy()

    def click_logout(self):
        self.root.withdraw()
        self.wordy_game.logout(self.username)
        ClientLogin.ClientLogin(self.wordy_game)
        self.root.destroy()

    def close_window(self):
        self.root.withdraw()
        self.wordy_game.logout(self.username)
        self.root.destroy()
