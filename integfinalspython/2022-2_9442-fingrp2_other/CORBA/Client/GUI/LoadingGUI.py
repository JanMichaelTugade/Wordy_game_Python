import sys
import tkinter as tk
import threading
import time
from . import GameGUI


class LoadingGUI:
    def __init__(self, wordy_game, username, room_name, round_number):
        self.wordy_game = wordy_game
        self.username = username
        self.room_name = room_name
        self.round_number = round_number
        # Set up the GUI components
        self.root = tk.Tk()
        self.root.title("Wordy")
        self.countdown = 5

        # Set the size and location of the GUI
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        self.root.configure(bg='#1c2833')

        # to set the size of the window
        self.window_width = 600
        self.window_height = 450
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x_position = int((self.screen_width - self.window_width) / 2)
        self.y_position = int((self.screen_height - self.window_height) / 2)
        self.root.geometry(
            "{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_position, self.y_position))

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.wordyLabel = tk.Label(self.root, text="Game starts in ", font=('Arial', 40), fg='#DEA54B', bg='#1c2833')
        self.wordyLabel.pack(pady=80, padx=0)

        self.timer = tk.Label(self.root, text=self.countdown, font=('Arial', 50), fg='#DEA54B', bg='#1c2833')
        self.timer.pack(pady=0, padx=0)

        # Start the countdown in a separate thread
        countdown_thread = threading.Thread(target=self.run_countdown)
        countdown_thread.start()

        # Start the timer

        self.root.mainloop()

    def run_countdown(self):
        while self.countdown > 0:
            time.sleep(1)
            self.countdown -= 1
            self.timer.config(text=str(self.countdown))

        self.root.withdraw()
        random = self.wordy_game.getRandomLetters(self.round_number)
        self.round_number += 1
        GameGUI.GameGUI(self.wordy_game, random, self.username, self.room_name, self.round_number)
        self.root.destroy()

    def close_window(self):
        self.wordy_game.logout(self.username)
        self.wordy_game.leaveWaitingRoom(self.username)
        self.root.destroy()


