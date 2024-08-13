import tkinter as tk
import threading
import time
from . import Homepage

class ResultGUI:
    def __init__(self, wordy_game, user_id, round_number, username, room_name):
        self.wordy_game = wordy_game
        self.round_number = round_number
        self.username = username
        self.room_name = room_name
        # Set up the GUI components
        self.root = tk.Tk()
        self.root.title("Wordy")
        self.countdown = 5

        # Set the size and location of the GUI
        self.root.geometry("800x650")
        self.root.resizable(False, False)

        # Set the background color to dark blue
        self.root.configure(bg='#1c2833')

        players = self.wordy_game.getPlayersInGameSession(room_name)
        # Create the "Game Over" label
        if self.wordy_game.modifyPointsAchieved(user_id, room_name) == 3:
            self.gameoverLabel = tk.Label(self.root, text="You Win!", font=('Arial', 40, 'bold'), fg='Lavender',
                                          bg='#1c2833')
        elif len(players) < 2:
            self.gameoverLabel = tk.Label(self.root, text="You Win!", font=('Arial', 40, 'bold'), fg='Lavender',
                                          bg='#1c2833')
        else:
            self.gameoverLabel = tk.Label(self.root, text="You Lose!", font=('Arial', 40, 'bold'), fg='Lavender',
                                          bg='#1c2833')
        self.gameoverLabel.pack(pady=20, padx=0)

        self.appLabel = tk.Label(self.root, text="W O R D Y", font=('Arial', 20), fg='tan', bg='#1c2833')
        self.appLabel.place(x=328, y=90)

        self.nextLabel = tk.Label(self.root, text="Thank you for playing ", font=('Arial', 12), fg='white', bg='#1c2833')
        self.nextLabel.place(x=309, y=595)

        self.countdownLabel = tk.Label(self.root, text=str(self.countdown), font=('Arial', 14, 'bold'), fg='white', bg='#1c2833')
        self.countdownLabel.place(x=458, y=593)

        # Create the panel to display the players and their scores
        panel_width = 400
        panel_height = 440
        panel_x = (800 - panel_width) / 2
        panel_y = (650 - panel_height) / 2

        panel = tk.Frame(self.root, width=panel_width, height=panel_height, bd=1, relief=tk.RIDGE, bg='Beige')
        panel.place(x=200, y=140)

        # Create the labels to display the players and their scores
        player_labels = []
        score_labels = []
        for i in range(len(players)):
            player = players[i]
            player_label = tk.Label(panel, text=player, font=('Arial', 14), fg='black', bg='Beige')
            if player == self.username:
                player_label.config(fg='#CE796B')  # Set the color to yellow for the logged-in player
            player_label.place(x=20, y=20 + 40 * i)

            # Get the player's score using their username
            player_score = self.wordy_game.displayScores(self.wordy_game.getUserIDFromUsername(player))
            score_label = tk.Label(panel, text=player_score, font=('Arial', 14), fg='black', bg='Beige')
            if player == self.username:
                score_label.config(fg='#CE796B')  # Set the color to yellow for the logged-in player's score
            score_label.place(x=320, y=20 + 40 * i)

            score_labels.append(score_label)
            player_labels.append(player_label)

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

        # Start the countdown in a separate thread
        countdown_thread = threading.Thread(target=self.run_countdown)
        countdown_thread.start()

        # Run the Tkinter event loop
        self.root.mainloop()

    def run_countdown(self):
        while self.countdown > 0:
            time.sleep(1)
            self.countdown -= 1
            self.countdownLabel.config(text=str(self.countdown))
        self.countdownLabel.place_forget()
        self.nextLabel.place_forget()
        main_menu_button = tk.Button(self.root, text="Main Menu", font=('Arial', 14), command=self.go_to_main_menu)
        main_menu_button.place(x=350, y=590)

    def go_to_main_menu(self):
        self.root.withdraw()
        self.wordy_game.leaveWaitingRoom(self.username)
        Homepage.Homepage(self.wordy_game, self.username)
        self.root.destroy()

    def close_window(self):
        self.wordy_game.logout(self.username)
        self.wordy_game.leaveWaitingRoom(self.username)
        self.root.destroy()