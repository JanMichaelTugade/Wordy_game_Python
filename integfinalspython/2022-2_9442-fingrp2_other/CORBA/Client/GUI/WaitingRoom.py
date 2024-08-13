import threading
import time
import tkinter as tk
from tkinter import CENTER, messagebox

from . import Homepage, LoadingGUI
class WaitingRoom:

    def __init__(self, wordy_game, username):
        super().__init__()

        self.wordy_game = wordy_game
        self.username = username
        self.root = tk.Tk()
        self.root.title("Wordy Start ")
        self.countdown = 10

        self.root.configure(bg='#1c2833')

        self.window_width = 500
        self.window_height = 430
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x_position = int((self.screen_width - self.window_width) / 2)
        self.y_position = int((self.screen_height - self.window_height) / 2)
        self.root.geometry(
            "{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_position, self.y_position))

        self.frame = tk.Frame(self.root, width=700, height=350, bg='#1c2833')
        self.frame.pack(expand=True)

        self.title_label = tk.Label(self.frame, text="Wordy Game", font=("Arial", 30), fg='#DEA54B', bg='#1c2833')
        self.title_label.grid(row=0, column=0, pady=40)

        players = self.wordy_game.getPlayerList()
        self.playerListLabel = tk.Label(self.frame, text="The players are: " + str(players), font=('Arial', 15), fg='#DBCBD8', bg='#1c2833')
        self.playerListLabel.grid(row=1, column=0, pady=20)

        status = self.wordy_game.checkWaitingRoomStatus()
        self.timer = tk.Label(self.frame, text=status[1], font=('Arial', 20), fg='#DBCBD8', bg='#1c2833')
        self.timer.grid(row=3, column=0, pady=20)

        self.main_button = tk.Button(self.frame, text="Back to Main Menu", fg='#0A090C', bg='#DEA54B', font=("Arial", 15),
                                     command=self.back_to_main)
        self.main_button.grid(row=4, column=0, pady=20)

        # Start the countdown in a separate thread
        self.stop_countdown = False
        self.countdown_thread = threading.Thread(target=self.run_countdown)
        self.countdown_thread.start()

        self.root.mainloop()

    def update(self):
        players = self.wordy_game.getPlayerList()
        self.playerListLabel.config(text="The players are: " + str(players))

        status = self.wordy_game.checkWaitingRoomStatus()
        self.timer.config(text=status[1])

    import threading

    def start_game(self):
        self.root.withdraw()
        status = self.wordy_game.checkWaitingRoomStatus()
        if status[0] == "Waiting room invalid":
            messagebox.showerror("Waiting Room Failed",
                                 "The waiting room does not have enough players! Returning to main menu.")
            self.wordy_game.leaveWaitingRoom(self.username)
            Homepage.Homepage(self.wordy_game, self.username)
        elif status[0] == "Waiting room ready":
            LoadingGUI.LoadingGUI(self.wordy_game, self.username, status[2], 0)
        self.root.destroy()

    def run_countdown(self):
        while self.countdown > 1 and not self.stop_countdown:
            self.update()
            self.countdown -= 1
            time.sleep(1)
        self.start_game()

    def back_to_main(self):
        self.root.withdraw()
        self.stop_countdown = True
        self.wordy_game.leaveWaitingRoom(self.username)
        Homepage.Homepage(self.wordy_game, self.username)
        self.root.destroy()

    def close_window(self):
        self.root.withdraw()
        self.wordy_game.logout(self.username)
        self.root.destroy()
