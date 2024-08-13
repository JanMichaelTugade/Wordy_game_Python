import tkinter as tk
from . import TopFivePlayers, TopFiveLongestWords
from . import Homepage

class Leaderboard:
    # add wordy_game to constructor if homepage is already working
    def __init__(self, wordy_game, username):
        self.wordy_game = wordy_game
        self.username = username
        self.root = tk.Tk()

        # to set the window's name to Wordy App
        self.root.title("Wordy App")
        self.root.configure(bg='#1c2833')

        # to set the size of the window
        self.window_width = 500
        self.window_height = 300
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x_position = int((self.screen_width - self.window_width) / 2)
        self.y_position = int((self.screen_height - self.window_height) / 2)
        self.root.geometry(
            "{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_position, self.y_position))

        # to set the root window to non-resizable
        self.root.resizable(False, False)

        # for Wordy Title label
        self.wordy_label = tk.Label(self.root, text="Leaderboard", font=('Arial', 25) , fg='#DEA54B', bg='#1c2833')
        self.wordy_label.pack(padx=50, pady=20)

        # for Top Five Player button
        self.top_players_button = tk.Button(self.root, text="Top 5 Players", font=('Arial', 15), fg='#0A090C', bg='#DEA54B', width=len("Top 5 Longest Words"),
                                            command=self.players_button)
        self.top_players_button.pack(padx=70, pady=18)

        # for Top Five Longest Words button
        self.top_longest_words_button = tk.Button(self.root, text="Top 5 Longest Words", font=('Arial', 15), fg='#0A090C', bg='#DEA54B', width=len("Top 5 Longest Words"), command=self.longest_words_button)
        self.top_longest_words_button.pack(padx=10, pady=5)

        self.back_button = tk.Button(self.root, text="Back", font=('Arial', 15), command=self.back_to_homepage, fg='#FFFFFF', bg='#E84855', width=len("Top 5 Longest Words"))
        self.back_button.pack(padx=10, pady=15)

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.root.mainloop()

    def players_button(self):
        self.root.withdraw()
        TopFivePlayers.TopFivePlayers(self.wordy_game, self.username)
        self.root.destroy()

    def longest_words_button(self):
        self.root.withdraw()
        TopFiveLongestWords.TopFiveLongestWords(self.wordy_game,self.username)
        self.root.destroy()

    def back_to_homepage(self):
        self.root.withdraw()
        Homepage.Homepage(self.wordy_game, self.username)
        self.root.destroy()

    def close_window(self):
        self.root.withdraw()
        self.wordy_game.logout(self.username)
        self.root.destroy()
