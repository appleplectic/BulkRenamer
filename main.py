import csv
import os
import ctypes
import tempfile
import pathlib
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import sv_ttk
import pandas as pd
import darkdetect


class BulkRenamerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Bulk Renamer")

        self.csv_label = ttk.Label(self.root, text="Select Spreadsheet File:")
        self.csv_label.grid(row=0, column=0, padx=10, pady=10)
        self.csv_path = ttk.Entry(self.root, width=50)
        self.csv_path.grid(row=0, column=1, padx=10, pady=10)
        self.csv_button = ttk.Button(self.root, text="Browse", command=self.browse_csv)
        self.csv_button.grid(row=0, column=2, padx=10, pady=10)

        self.folder_label = ttk.Label(self.root, text="Select Folder:")
        self.folder_label.grid(row=1, column=0, padx=10, pady=10)
        self.folder_path = ttk.Entry(self.root, width=50)
        self.folder_path.grid(row=1, column=1, padx=10, pady=10)
        self.folder_button = ttk.Button(self.root, text="Browse", command=self.browse_folder)
        self.folder_button.grid(row=1, column=2, padx=10, pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=2, column=0, columnspan=3, pady=10)

        self.rename_button = ttk.Button(self.button_frame, text="Rename Files", command=self.rename_files)
        self.rename_button.grid(row=0, column=0, padx=10)

        self.undo_button = ttk.Button(self.button_frame, text="Undo", command=self.undo_rename)
        self.undo_button.grid(row=0, column=1, padx=10)

        self.rename_history = []
        self.tempfolder = tempfile.TemporaryDirectory()

    def __del__(self):
        self.tempfolder.cleanup()

    def browse_csv(self):
        path = filedialog.askopenfilename(filetypes=[("Spreadsheet files", ["*.csv", "*.xls", "*.xlsx"])])
        if path and os.path.isfile(path):
            self.csv_path.delete(0, tk.END)
            self.csv_path.insert(0, path)
        else:
            messagebox.showerror("Error", "Please select a valid spreadsheet file.")

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path and os.path.isdir(path):
            self.folder_path.delete(0, tk.END)
            self.folder_path.insert(0, path)
        else:
            messagebox.showerror("Error", "Please select a valid folder.")

    def rename_files(self):
        csv_file = self.csv_path.get()
        folder = self.folder_path.get()

        if ((not csv_file) or (not folder)) or (not os.path.isfile(csv_file)) or (not os.path.isdir(folder)):
            messagebox.showerror("Error", "Please enter valid folder and spreadsheet paths.")
            return

        if csv_file.lower().endswith("xls") or csv_file.lower().endswith("xlsx"):
            df = pd.read_excel(csv_file, header=None, dtype=str)
            filepath = pathlib.Path(self.tempfolder.name) / "temp.csv"
            df.to_csv(filepath, index=False, header=False)
            csv_file = filepath
            print(csv_file)

        try:
            renames = 0
            already_exists = 0
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                files = os.listdir(folder)

                for row in reader:
                    if len(row) < 2:
                        continue

                    old_name, new_name = row[0], row[1]
                    if not old_name or not new_name:
                        continue

                    for file in files:
                        no_ext, ext = os.path.splitext(file)
                        if os.path.isfile(os.path.join(folder, file)) and old_name in no_ext:
                            old_path = os.path.join(folder, file)
                            new_path = os.path.join(folder, no_ext.replace(old_name, new_name) + ext)

                            if os.path.exists(new_path):
                                already_exists += 1

                            os.rename(old_path, new_path)
                            self.rename_history.append((new_path, old_path))
                            renames += 1

            messagebox.showinfo("Success", f"{renames} files renamed successfully, {already_exists} files skipped because destination exists.")

        except ValueError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def undo_rename(self):
        if not self.rename_history:
            messagebox.showinfo("Undo", "No renames to undo.")
            return

        try:
            while self.rename_history:
                new_path, old_path = self.rename_history.pop()
                if os.path.exists(new_path):
                    os.rename(new_path, old_path)

            messagebox.showinfo("Undo", "Renames undone successfully.")
            self.rename_history = []

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during undo: {e}")


def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


if __name__ == "__main__":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    root = tk.Tk()
    root.iconbitmap(resource_path("rename.ico"))
    app = BulkRenamerApp(root)
    sv_ttk.set_theme(darkdetect.theme())
    root.mainloop()
