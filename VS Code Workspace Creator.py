import customtkinter as ctk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import tkinter as tk
import json
import os
import pathlib # handles file paths better cross platform

# --- appearance stuff ---
ctk.set_appearance_mode("System")  # system dark or light whatever u use
ctk.set_default_color_theme("blue") # blue green dark-blue pick one

# --- main app window ---
class WsMakerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- window setup ---
        self.title("VS Code WS Maker")
        self.minsize(650, 550) # smallest size allowed
        self.center_win(750, 600) # start in middle

        # --- data ---
        self.folders_list = [] # holds the paths u add

        # --- build the ui ---
        self.setup_ui()

    def center_win(self, w=750, h=600):
        """puts the window in screen center"""
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw / 2) - (w / 2)
        y = (sh / 2) - (h / 2)
        self.geometry(f'{w}x{h}+{int(x)}+{int(y)}') # set size and position

    def setup_ui(self):
        """makes all the buttons boxes etc"""

        # grid layout 2 rows main log area
        self.grid_rowconfigure(0, weight=3) # top part bigger
        self.grid_rowconfigure(1, weight=1) # log part smaller
        self.grid_columnconfigure(0, weight=1) # use full width

        # --- top part for folder list actions ---
        top_bit = ctk.CTkFrame(self, corner_radius=10)
        top_bit.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="nsew")
        top_bit.grid_columnconfigure(0, weight=1) # listbox col
        top_bit.grid_rowconfigure(2, weight=1) # listbox row needs space

        # --- buttons for the list ---
        list_btns = ctk.CTkFrame(top_bit, fg_color="transparent")
        list_btns.grid(row=0, column=0, columnspan=2, padx=10, pady=(10,0), sticky="ew")
        list_btns.grid_columnconfigure((0, 1, 2), weight=1) # space buttons out

        add_btn = ctk.CTkButton(list_btns, text="Add Folder to List", command=self.add_folder, corner_radius=8)
        add_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        rem_btn = ctk.CTkButton(list_btns, text="Remove Selected", command=self.rem_folder, corner_radius=8)
        rem_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        clr_btn = ctk.CTkButton(list_btns, text="Clear List", command=self.clr_list, corner_radius=8)
        clr_btn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # --- button for subfolder action ---
        sub_btn_area = ctk.CTkFrame(top_bit, fg_color="transparent")
        sub_btn_area.grid(row=1, column=0, columnspan=2, padx=10, pady=(0,5), sticky="ew")
        sub_btn_area.grid_columnconfigure(0, weight=1)

        sub_btn = ctk.CTkButton(
            sub_btn_area,
            text="Create in Subfolders...",
            command=self.go_process_subs, # new func for this
            corner_radius=8,
            # fg_color=ctk.ThemeManager.theme["CTkButton"]["hover_color"] # maybe diff color? nah keep it simple
        )
        sub_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # --- the list box area ---
        list_area = ctk.CTkFrame(top_bit, corner_radius=5)
        list_area.grid(row=2, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="nsew") # below buttons
        list_area.grid_rowconfigure(0, weight=1)
        list_area.grid_columnconfigure(0, weight=1)

        # using tk listbox cuz ctk doesnt have one yet
        self.folder_box = tk.Listbox(
            list_area,
            selectmode=tk.SINGLE, # only select one
            bg=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"]), # match theme
            fg=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"]), # match theme
            selectbackground=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"]), # match theme
            selectforeground=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["text_color"]), # match theme
            borderwidth=0,
            highlightthickness=0, # no ugly border
            exportselection=False,
            font=("Segoe UI", 11) # decent font
        )
        self.folder_box.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        # --- scrollbar for the list ---
        # tk scrollbar easier here
        scrollbar = tk.Scrollbar(list_area, orient="vertical", command=self.folder_box.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.folder_box.configure(yscrollcommand=scrollbar.set) # link scrollbar

        # --- bottom part for logs button ---
        bottom_bit = ctk.CTkFrame(self, corner_radius=10)
        bottom_bit.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="nsew")
        bottom_bit.grid_rowconfigure(0, weight=1) # log box row
        bottom_bit.grid_rowconfigure(1, weight=0) # button row
        bottom_bit.grid_columnconfigure(0, weight=1)

        # --- log text box ---
        self.log_box = ctk.CTkTextbox(
            bottom_bit,
            wrap=tk.WORD, # wrap text nicely
            state=tk.DISABLED, # read only
            corner_radius=5,
            font=("Segoe UI", 10)
        )
        self.log_box.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")

        # --- button to process the list ---
        go_btn = ctk.CTkButton(
            bottom_bit,
            text="Create Workspaces for Folders in List",
            command=self.go_process_list, # func for this button
            corner_radius=8,
            height=35 # bit bigger
        )
        go_btn.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")

    # --- button actions ---
    def add_folder(self):
        """opens dialog adds folder to list"""
        f_path_str = fd.askdirectory(parent=self, title="Select Folder to Add")
        if f_path_str: # check if user selected something
            f_path = pathlib.Path(f_path_str) # use pathlib its good
            if f_path not in self.folders_list:
                self.folders_list.append(f_path)
                self.refresh_listbox()
                self.log_it(f"[List] Added: {f_path}")
            else:
                self.log_it(f"[List] Already got: {f_path}") # dont add duplicates

    def rem_folder(self):
        """removes selected folder from list"""
        sel_indices = self.folder_box.curselection() # find whats selected
        if not sel_indices:
            self.log_it("[List] Nothin selected to remove")
            return

        sel_idx = sel_indices[0] # get the first selected index
        try:
            f_to_rem_str = self.folder_box.get(sel_idx) # get path string from listbox
            f_to_rem = pathlib.Path(f_to_rem_str) # make it a path object

            if f_to_rem in self.folders_list: # check our actual data list
                self.folders_list.remove(f_to_rem)
                self.refresh_listbox() # update the visual list
                self.log_it(f"[List] Removed: {f_to_rem}")
            else:
                # shouldnt happen if lists r synced but safety first
                self.log_it(f"[List] Error: Cant find {f_to_rem} in data")
                self.refresh_listbox() # refresh anyway

        except Exception as e:
             self.log_it(f"[List] Error removing folder: {e}") # catch other probs

    def clr_list(self):
        """removes all folders from list"""
        if not self.folders_list:
            self.log_it("[List] List empty already")
            return

        # ask user first dont wanna delete by accident
        if mb.askyesno("Confirm Clear", "U sure u wanna clear the list?", parent=self):
            self.folders_list.clear() # empty the data
            self.refresh_listbox() # empty the visual list
            self.log_it("[List] Cleared the list")

    def refresh_listbox(self):
        """updates listbox to show whats in folders_list"""
        self.folder_box.delete(0, tk.END) # clear visual list first
        sorted_folders = sorted(self.folders_list) # sort em looks nicer
        for f_path in sorted_folders:
            self.folder_box.insert(tk.END, str(f_path)) # add paths back as strings

    def log_it(self, msg):
        """adds message to the log box"""
        self.log_box.configure(state=tk.NORMAL) # gotta enable to write
        self.log_box.insert(tk.END, msg + "\n") # add the message
        self.log_box.configure(state=tk.DISABLED) # disable again read only
        self.log_box.see(tk.END) # scroll down automatic

    def make_one_ws(self, target_f_path):
        """
        makes one workspace file inside target folder
        returns true if ok false if error
        logs messages too
        """
        try:
            f_name = target_f_path.name # get folder name itself
            if not f_name: # handle weird cases like C:/
                f_name = f"workspace_{target_f_path.drive.rstrip(':').lower()}" # make generic name

            ws_name = f"{f_name}.code-workspace" # the file name
            ws_save_loc = target_f_path / ws_name # where to save it inside target

            # check if already exists maybe skip?
            if ws_save_loc.exists():
                self.log_it(f"SKIP: Already exists {ws_save_loc}")
                return True # count as success if its there

            # data for the json file simple stuff
            ws_data = {
                "folders": [{"path": "."}], # path is just current dir relative to file
                "settings": {} # empty settings block
            }

            # write the file
            with open(ws_save_loc, 'w', encoding='utf-8') as f:
                json.dump(ws_data, f, indent=4) # indent makes json readable

            self.log_it(f"GOOD: Made {ws_save_loc}")
            return True # success

        except PermissionError:
            err_msg = f"FAIL: No permission for {target_f_path}"
            self.log_it(err_msg)
            return False # fail
        except OSError as e:
            err_msg = f"FAIL: OS error for {target_f_path}: {e}"
            self.log_it(err_msg)
            return False # fail
        except Exception as e:
            err_msg = f"FAIL: Weird error for {target_f_path}: {e}"
            self.log_it(err_msg)
            return False # fail

    def go_process_list(self):
        """goes thru the list makes ws files"""
        if not self.folders_list:
            self.log_it("[List] List empty cant process")
            mb.showwarning("Empty List", "Add folders to list first dude", parent=self)
            return

        self.log_it("\n--- Makin Workspaces (from List) ---")
        ok_count = 0
        bad_count = 0

        folders_to_do = list(self.folders_list) # copy list just in case

        for f_path in folders_to_do:
            if self.make_one_ws(f_path): # call the helper func
                ok_count += 1
            else:
                bad_count += 1

        # --- final report ---
        summary = f"\n--- Done (List) ---\nSuccess: {ok_count} Failed: {bad_count}"
        self.log_it(summary)
        mb.showinfo(
            "Done (List)",
            f"Finished makin ws files from list.\n\nGood: {ok_count}\nBad: {bad_count}\n\nCheck log below",
            parent=self
        )

    def go_process_subs(self):
        """handles the create in subfolders button"""
        parent_f_str = fd.askdirectory(
            parent=self,
            title="Select Parent Folder (contains project folders)"
        )

        if not parent_f_str: # user cancelled
            self.log_it("[Subfolders] No parent folder picked")
            return

        parent_f = pathlib.Path(parent_f_str) # make it a path
        self.log_it(f"\n--- Makin Workspaces (in Subfolders of {parent_f}) ---")

        subs_found = [] # list to hold subfolders
        try:
            # iterate thru items in parent folder
            for item in parent_f.iterdir():
                if item.is_dir(): # check if its a directory
                    subs_found.append(item)
        except Exception as e:
            self.log_it(f"Error scanning parent {parent_f}: {e}")
            mb.showerror("Scan Error", f"Couldnt scan parent folder:\n{e}", parent=self)
            return

        if not subs_found:
            self.log_it(f"No subfolders found in {parent_f}")
            mb.showinfo("No Subfolders", f"Didnt find any folders inside:\n{parent_f}", parent=self)
            return

        self.log_it(f"Found {len(subs_found)} subfolders gonna process em")
        ok_count = 0
        bad_count = 0

        for sub_f_path in subs_found:
            self.log_it(f"[Subfolders] Doin: {sub_f_path}")
            if self.make_one_ws(sub_f_path): # use same helper func
                ok_count += 1
            else:
                bad_count += 1

        # --- final report ---
        summary = f"\n--- Done (Subfolders) ---\nFolders Found: {len(subs_found)} Success: {ok_count} Failed: {bad_count}"
        self.log_it(summary)
        mb.showinfo(
            "Done (Subfolders)",
            f"Finished makin ws files in subfolders.\n\nParent: {parent_f}\nFound: {len(subs_found)}\nGood: {ok_count}\nBad: {bad_count}\n\nCheck log below",
            parent=self
        )

# --- run the app ---
if __name__ == "__main__":
    app = WsMakerApp() # create the app window
    app.mainloop() # start the ui loop
