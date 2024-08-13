import sys
from omniORB import CORBA
import CosNaming
import WordyApp
import tkinter as tk
from GUI import ClientLogin

class WelcomeGUI:
    def __init__(self):
        self.root = tk.Tk()

        # to set the window's name to Wordy App
        self.root.title("Wordy App")

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

        # Set the background color to dark blue
        self.root.configure(bg='#1c2833')

        # for Wordy Title label
        self.wordy_label = tk.Label(self.root, text="W o r d y", font=('Arial', 25), fg='#F0EBD8', bg='#1c2833')
        self.wordy_label.pack(padx=20, pady=20)

        # for ip label
        self.ip_label = tk.Label(self.root, text="Ip Address", font=('Arial', 15), fg='#DBCBD8', bg='#1c2833')
        self.ip_label.pack(padx=5, pady=15)

        # for ip textfield
        self.ip_entry = tk.Entry(self.root, font=('Arial', 16))
        self.ip_entry.pack()

        # for port label
        self.port_label = tk.Label(self.root, text="Port Number", font=('Arial', 15), fg='#DBCBD8', bg='#1c2833')
        self.port_label.pack(padx=5, pady=15)

        # for port textfield
        self.port_entry = tk.Entry(self.root, font=('Arial', 16))
        self.port_entry.pack()

        # for ip button
        self.ip_button = tk.Button(self.root, text="Connect", font=('Arial', 15), command=self.click_connect, fg='#0A090C', bg='#DEA54B', width=len("Connect to LA"))
        self.ip_button.pack(padx=20, pady=20)

        # for LAN button
        self.lan_button = tk.Button(self.root, text="Connect to LAN", font=('Arial', 15), command=self.click_local, fg='#0A090C', bg='#DEA54B')
        self.lan_button.pack(padx=5, pady=0)

        self.root.mainloop()

    def click_connect(self):
        ip_address = self.ip_entry.get()
        port_number = self.port_entry.get()

        # Get ip and port number
        corbaloc_string = "corbaloc::" + ip_address + ":" + port_number + "/NameService"

        # Initialize the ORB
        orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

        # Obtain a reference to the Naming Service
        obj = orb.string_to_object(corbaloc_string)
        namingContext = obj._narrow(CosNaming.NamingContext)

        # Construct the name to resolve
        name = [CosNaming.NameComponent("WordyGame", "")]

        try:
            # Resolve the name to a reference to the WordyGame object
            obj = namingContext.resolve(name)
            wordy_game = obj._narrow(WordyApp.WordyGame)

            # Use the WordyGame object
            if wordy_game is not None:
                self.root.withdraw()
                ClientLogin.ClientLogin(wordy_game)
                self.root.destroy()
            else:
                print("ERROR: Unable to obtain reference to WordyGame object")

        except (CosNaming.NamingContext.NotFound, ValueError) as ex:
            print("ERROR: Failed to resolve name: %s" % ex)

        # Shutdown the ORB
        orb.shutdown(True)

    def click_local(self):
        port_number = self.port_entry.get()

        # Get ip and port number
        corbaloc_string = "corbaloc::localhost:" + port_number + "/NameService"

        # Initialize the ORB
        orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

        # Obtain a reference to the Naming Service
        obj = orb.string_to_object(corbaloc_string)
        naming_context = obj._narrow(CosNaming.NamingContext)

        # Construct the name to resolve
        name = [CosNaming.NameComponent("WordyGame", "")]

        try:
            # Resolve the name to a reference to the WordyGame object
            obj = naming_context.resolve(name)
            wordy_game = obj._narrow(WordyApp.WordyGame)

            # Use the WordyGame object
            if wordy_game is not None:
                self.root.withdraw()
                ClientLogin.ClientLogin(wordy_game)
                self.root.destroy()
            else:
                print("ERROR: Unable to obtain reference to WordyGame object")

        except (CosNaming.NamingContext.NotFound, ValueError) as ex:
            print("ERROR: Failed to resolve name: %s" % ex)

        # Shutdown the ORB
        orb.shutdown(True)
