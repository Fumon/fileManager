import tkinter as tk
import json
from tkinter import messagebox
from utility import find_files
from datetime import datetime, timezone
import os

# ---------------------------- function field ------------------------------- #

# ---------------------------- search File Function ------------------------------- #

# ---------------------------- Save Function------------------------------- #
def saveToJson(fname: str, pathname: str, searchResult: list[str]) -> None:
    # This function is not included in the FindFilesWindow class for a good reason
    # That reason is to try and isolate code to one responsibility
    # The FindFilesWindow class is responsible for interacting with the user and checking whether input is valid
    # This function is responsible for performing the actual action itself and takes arguments it knows are already valid

    with open("json/searchFiles.json", "a+") as data_file:
        fileLength = data_file.tell()

        if fileLength:
            # There's data in the file. Read it
            data_file.seek(0)
            data = json.load(data_file)
            # Reset to start to prepare for write
            data_file.seek(0)
            data_file.truncate()
        else:
            data = {}
    
        # Updating old data with new data
        data[datetime.now(timezone.utc).isoformat()] = {
                "fname": fname,
                "pathname":  pathname,
                "searchResult":  searchResult
            }
        json.dump(data, data_file, indent=4)

# ----------------------------Delete File Funtion------------------------------- #
def delete():
    try:
        os.remove("json/searchFiles.json")
    except FileNotFoundError:
        messagebox.showinfo(
            title="Oops", message="The File hasn't been created yet, nothing to delete")

# ------------------------- UI Utility Classes ------------------------ #

class SpawnsChildWindows:
    childWindows: list[tk.Toplevel]

    def __init__(self, parent) -> None:
        self.parent = parent
        self.childWindows = []
    
    def makeCommandWindow(self) -> tk.Toplevel:
        newWindow = tk.Toplevel(self.parent)
        self.childWindows.append(newWindow)
        return newWindow

# ---------------------------- UI SETUP ------------------------------- #

class DateQueryWindow:
    def __init__(self, parent) -> None:
        self.frame = tk.Frame(parent, padx=40, pady=50)
        self.frame.pack(side="top")

        self.dateLabel = tk.Label(self.frame, text="Date:")
        self.dateLabel.grid(row=1, column=0)
        self.dateEntry = tk.Entry(self.frame, width=30)
        self.dateEntry.grid(row=1, column=1)

        self.resultLabel = tk.Label(self.frame, text="Result:")
        self.resultLabel.grid(row=2, column=0)
        self.resultText = tk.Text(self.frame, height=5, width=30)
        self.resultText.grid(row=2, column=1)

        self.queryButton = tk.Button(self.frame, text="Query")
        self.queryButton.grid(row=3, column=0)

    def doQuery(self) -> None:
        # Input Validation
        inputDate = self.dateEntry.get()
        datetime


class FindFilesWindow(SpawnsChildWindows):
    currentSearchResult: list[str]

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.childWindows

        self.frame = tk.Frame(parent, padx=35, pady=35)
        self.frame.pack(side="top")
        # Create interface

        # Labels
        self.fileLabel = tk.Label(self.frame, text="File:")
        self.fileLabel.grid(row=1, column=0)
        self.pathLabel = tk.Label(self.frame, text="Path:")
        self.pathLabel.grid(row=2, column=0)
        self.textLabel = tk.Label(self.frame, text="Result:")
        self.textLabel.grid(row=3, column=0)

        # Entries
        # fileEntry
        self.fileEntry = tk.Entry(self.frame, width=40)
        self.fileEntry.grid(row=1, column=1)
        self.fileEntry.focus()
        # path Entry
        self.pathEntry = tk.Entry(self.frame, width=40)
        self.pathEntry.grid(row=2, column=1)
        self.pathEntry.focus()

        # Buttons
        self.search_button = tk.Button(self.frame, text="Search", width=9, command=self.searchFile)
        #the first parameter for padx is left, the second parameter for pady is the right
        self.search_button.grid(row=2, column=2,padx=(3,0))

        #the tuple for pady, the first parameter for top, second parameter for buttom
        self.add_button = tk.Button(self.frame, text="Save", width=30, command=self.save)
        self.add_button.grid(row=4, column=1,pady=(5,5))

        self.delete_button = tk.Button(self.frame, text="Delete", width=30, command=self.delete)
        self.delete_button.grid(row=5, column=1,pady=(0,5))

        # Todo This jumps to a new UI window to execute the Query function, there would be some command for switching the UI
        self.query_button = tk.Button(self.frame, text="Date Query", width=30, command=self.makeDateQuery)
        self.query_button.grid(row=6, column=1)


        # Text
        self.currentSearchResult = None
        self.text = tk.Text(self.frame, height=5, width=30)
        self.text.grid(row=3, column=1)

        # Set to none to indicate there is no date query active
        self.dateQueryCommand = None

    def searchFile(self) -> None:
        fnameInput = self.fileEntry.get()
        fpathInput = self.pathEntry.get()
        self.currentSearchResult = find_files(fnameInput, fpathInput)
        self.text.insert(tk.END, self.currentSearchResult)
    
    def save(self) -> None:
        # DO INPUT VALIDATION HERE
        if self.currentSearchResult is None:
            messagebox.showinfo(title="Oops", message="Need to search before saving")
            # Exit early
            return
        
        fnameInput = self.fileEntry.get()
        fpathInput = self.pathEntry.get()

        saveToJson(fnameInput, fpathInput, self.currentSearchResult)

        # Clear the inputs
        self.fileEntry.delete(0, tk.END)
        self.pathEntry.delete(0, tk.END)
        self.text.delete("1.0", tk.END)
        self.currentSearchResult = None
    
    def delete(self) -> None:
        pass

    def makeDateQuery(self) -> None:
        if self.dateQueryCommand is None:
            newWindow = self.makeCommandWindow()
            newWindow.title("Date Query")
            self.dateQueryCommand = DateQueryWindow(newWindow)

class MainUI(SpawnsChildWindows):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.childCommandInstances = []

        # Create a root object for the rest of the items
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both")

        # Create buttons
        self.findFilesButton = tk.Button(
            self.frame,
            text='Find Files',
            command=self.makeFindFiles)
        self.findFilesButton.pack(fill="both")

    def makeFindFiles(self) -> None:
        newParent = self.makeCommandWindow()
        newParent.title("FindFiles Function")
        self.childCommandInstances.append(FindFilesWindow(newParent))

if __name__ == "__main__":
    #Global Config
    mainWindow = tk.Tk()
    window = MainUI(mainWindow)
    mainWindow.mainloop()
