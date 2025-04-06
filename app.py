import tkinter as tk
import tkinter.messagebox
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class MyApp(ctk.CTk):
    flp_directory: str
    changelog_directory: str

    def __init__(self):
        super().__init__()

        # Window Setup        
        self.title("FL Studio Live")
        self.geometry("600x600")      
        self.resizable(False, False)  

        # Grid Configuration
       
        # Use a single row: row=0
        # Two columns: col=0 (70% width), col=1 (30% width)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Left Frame (browser area)
        self.left_frame = ctk.CTkFrame(self, corner_radius=0)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Let the left frame expand
        self.left_frame.grid_columnconfigure(0, weight=1)

        # -------------------- Title Label --------------------
        self.title_label = ctk.CTkLabel(self.left_frame, 
                                        text="FL Studio Live",
                                        font=
                                        ctk.CTkFont(family="Arial", size=50, weight="bold"),
                                        text_color="#ff944d")
        self.title_label.grid(row=0, column=0, padx=20, pady=(0, 40))

        # -------------------- Selecting FLP File --------------------     
        self.flp_entry = ctk.CTkEntry(# Entry: FLP Path
            self.left_frame,
            placeholder_text="FLP file path..."
        )
        self.flp_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.flp_button = ctk.CTkButton(# Button: Browse for FLP
            self.left_frame, 
            text="Select FLP file",
            command=self.browse_flp
        )
        self.flp_button.grid(row=0, column=0, padx=10, pady=(100, 10), sticky="w")

        # -------------------- Selecting Changelog Directory --------------------
        self.save_entry = ctk.CTkEntry(# Entry: Save Path
            self.left_frame,
            placeholder_text="Save directory path..."
        )
        self.save_entry.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        self.save_button = ctk.CTkButton(# Button: Browse for Save Directory
            self.left_frame, 
            text="Select Save Directory",
            command=self.browse_save
        )
        self.save_button.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        # -------------------- Start Session Button -------------------- 
        """
        1 - There will be 2 buttons: 1 (Start Session): You are hosting the session; 2 (Join Session): You are joining a session
            - If you click "Start Session", you will be given a code (hash of your ip address) to give to the other client to connect to.
            - If you click "Join Session", you will be prompted to enter the hash ip code to connect to the server
        """


        # -------------------- Toggle Updates On/Off Button --------------------


    # --------------------------------------------
    #  Placeholder command methods
    # --------------------------------------------
    def browse_flp(self):
        """       
        1 - Open file explorer to allow user to select flp
        2 - Display directory of the file in the entry box below the button
        3 - Store the directory of the flp file in the class as an attribute
        """
        filepath = tk.filedialog.askopenfilename(title="Select .flp file", filetypes=[("FL Studio project file", "*.flp"), ("All Files", "*.*")])

        if filepath: 
            # populate flp path entry field
            self.flp_entry.delete(0, "end")
            self.flp_entry.insert(0, filepath)

            # store filepath in class attribute
            self.flp_directory = filepath        

    def browse_save(self):
        """
        1 - Open file explorer to allow user to select where the program data (i.e., the changelogs) will go
        2 - Display directory of the file in the entry box below the button
        3 - Store the directory of the flp file in the class as an attribute
        """
        directory = tk.filedialog.askdirectory(title="Select Data Directory")

        if directory:
            # populate data path entry field
            self.save_entry.delete(0, "end")
            self.save_entry.insert(0, directory)

            # store directory in class attribute
            self.changelog_directory = directory
            print(self.changelog_directory)

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()

