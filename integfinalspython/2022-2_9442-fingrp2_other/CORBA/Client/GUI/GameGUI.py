import random
import tkinter as tk
import threading
import time

from . import RankGUI, ResultGUI

class GameGUI:
    def __init__(self, wordy_game, random_letters, username, room_name, round_number):
        self.wordy_game = wordy_game
        self.random_letters = random_letters
        self.username = username
        self.room_name = room_name
        self.round_number = round_number
        first_letter_line = ""
        second_letter_line = ""

        user_id = wordy_game.getUserIDFromUsername(username)
        points = wordy_game.modifyPointsAchieved(user_id, room_name)

        self.user_id = user_id

        # Set up the GUI components
        self.root = tk.Tk()
        self.root.title("Wordy")
        self.countdown = 20

        # Set the size and location of the GUI
        self.root.geometry("800x650")
        self.root.resizable(False, False)
        self.root.wm_attributes("-topmost", 1)
        self.root.configure(bg='#1c2833')

        # to set the size of the window
        self.window_width = 800
        self.window_height = 650

        self.round_label = tk.Label(self.root, text="Round " + str(round_number), font=('Arial', 40), fg='#DEA54B', bg='#1c2833')
        self.round_label.pack(pady=20, padx=0)

        self.timer = tk.Label(self.root, text="Timer", font=('Arial', 30), fg='#DEA54B', bg='#1c2833')
        self.timer.pack(pady=30, padx=0)

        self.countdown_label = tk.Label(self.root, text=str(self.countdown), font=('Arial', 25), fg='#DBCBD8', bg='#1c2833')
        self.countdown_label.place(x=385, y=185)

        self.user_label = tk.Label(self.root, text=username, font=('Arial', 17), fg='#E8DAB2', bg='#1c2833')
        self.user_label.place(x=10, y=10)

        self.score_label = tk.Label(self.root, text="Score: " + str(points), font=('Arial', 17),  fg='#DEA54B', bg='#1c2833')
        self.score_label.place(x=self.window_width - 105, y=10)

        self.word_label = tk.Label(self.root, text=first_letter_line + "\n" + second_letter_line,
                                   font=('Orbitron', 40, 'bold'), justify='center', fg='#CE796B', bg='#1c2833' )
        self.word_label.pack(pady=50, padx=0)
        self.shuffle_letters(self.random_letters)

        self.validation = tk.Label(self.root, text="", font=('Arial', 17), bg='#1c2833')
        self.validation.place(relx=0.5, rely=0.85, anchor="center")

        # Create answer entry and bind it to events
        self.answer_entry = tk.Entry(self.root, font=('Arial', 30), justify='center',fg='#1c2833', bg='#DEA54B')
        self.answer_entry.pack(pady=30, padx=0)
        self.answer_entry.bind('<Return>', self.validate_answer)
        self.answer_entry.bind("<KeyRelease>", lambda e: self.on_answer_changed(e))

        self.shuffle_button = tk.Button(self.root, text="SHUFFLE", font=('Arial', 11), command=self.click_shuffle, fg='#FFFFFC', bg='#8B9556')
        self.shuffle_button.place(x=548, y=440)

        # Start the countdown in a separate thread
        self.stop_countdown = False
        countdown_thread = threading.Thread(target=self.run_countdown)
        countdown_thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

        # Run the Tkinter event loop
        self.root.mainloop()

    def on_answer_changed(self, event):
        # Convert the entered text to uppercase and remove any digits
        text = self.answer_entry.get().upper()
        text = ''.join([i for i in text if not i.isdigit()])
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.insert(0, text)

    def run_countdown(self):
        while self.countdown > 0 and not self.stop_countdown:
            time.sleep(1)
            self.countdown -= 1
            self.countdown_label.config(text=str(self.countdown))

        self.root.withdraw()
        self.wordy_game.modifyPointsAchieved(self.user_id, self.room_name)
        time.sleep(3)
        flag = self.wordy_game.checkPointsAchieved(self.room_name)
        self.wordy_game.setLongestWordToNull(self.room_name)
        if not flag:
            RankGUI.RankGUI(self.wordy_game, self.round_number, self.username, self.room_name)
            self.root.destroy()
        elif self.wordy_game.modifyPointsAchieved(self.user_id, self.room_name) == 3 or self.wordy_game.checkPointsAchieved(self.room_name):
            self.wordy_game.updateMatchesWon(self.user_id)
            ResultGUI.ResultGUI(self.wordy_game, self.user_id, self.round_number, self.username, self.room_name)
            self.root.destroy()
        elif not self.wordy_game.modifyPointsAchieved(self.user_id, self.room_name) == 3 or self.wordy_game.checkPointsAchieved(self.room_name):
            ResultGUI.ResultGUI(self.wordy_game, self.user_id, self.round_number, self.username, self.room_name)
            self.root.destroy()

    def click_shuffle(self):
        self.shuffle_letters(self.random_letters)

    def shuffle_letters(self, randomLetters):
        letters_array = list(randomLetters)

        # THE FISHER-YALES SHUFFLE ALGORITHM
        for i in range(len(letters_array) - 1, 0, -1):
            index = random.randint(0, i)
            temp = letters_array[index]
            letters_array[index] = letters_array[i]
            letters_array[i] = temp

        first_letter_line = ''.join(letters_array[:10]).strip()
        second_letter_line = ''.join(letters_array[10:]).strip()

        first_letter_line = ' '.join(list(first_letter_line))
        second_letter_line = ' '.join(list(second_letter_line))

        self.word_label.config(text=first_letter_line + "\n" + second_letter_line)

    def validate_answer(self, event=None):
        data = self.wordy_game.getWordsData()
        answer = self.answer_entry.get().strip()

        if answer:
            if self.wordy_game.validateInput(self.random_letters, answer, data):
                self.validation.config(text="ANSWER IS VALID", fg="green")
                if len(answer) >= self.wordy_game.getLongestWordLength(self.user_id):
                    self.wordy_game.updateLongestWordFormed(self.user_id, answer, self.room_name)
                    if self.wordy_game.checkExistingUserID(self.user_id):
                        self.wordy_game.compareWordFormedToLongestWord(self.user_id, answer)
                    else:
                        self.wordy_game.insertIntoLeaderboardTable(self.user_id, answer, 0)
            else:
                self.validation.config(text="INVALID WORD FORMED", fg="red")
        else:
            self.validation.config(text="", fg="black")

        self.answer_entry.delete(0, tk.END)
        self.root.update()

    def close_window(self):
        self.wordy_game.logout(self.username)
        self.wordy_game.leaveWaitingRoom(self.username)
        self.root.destroy()