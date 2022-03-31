import tkinter as tk
import json
from tkinter import messagebox
from utility import find_files
from datetime import datetime
import os
import time

# ---------------------------- function field ------------------------------- #

# ---------------------------- search File Function ------------------------------- #

# ---------------------------- Save Function------------------------------- #
def saveToJson():
    # This function is not included in the FindFilesWindow class for a good reason
    # That reason is to try and isolate code to one responsibility
    # The FindFilesWindow class is responsible for interacting with the user and checking whether input is valid
    # This function is responsible for performing the actual action itself and takes arguments it knows are already valid

    # date time properties needs to use the json.dumps to transfer to the json format(serialize)
    funcName = "find_files"
    fnameInput = fileEntry.get()
    fpathInput = pathEntry.get()
    searchResult = text.get('1.0', END)
    recordDate = json.dumps(datetime.now().strftime('%Y-%m-%d'))

    new_data = {
        funcName: {
            "fname": fnameInput,
            "pathname": fpathInput,
            "searchResult": searchResult,
            "recordDate": recordDate
        }
    }
    # Todo:  add a check for regex
    if len(fnameInput) == 0 or len(fpathInput) == 0 or len(searchResult) == 0:
        messagebox.showinfo(
            title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("json/searchFiles.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("json/searchFiles.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("json/searchFiles.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            #make sure the program runs more smoothly
            time.sleep(0.5)
            fileEntry.delete(0, END)
            pathEntry.delete(0, END)
            text.delete('1.0', END)


# ----------------------------Delete File Funtion------------------------------- #
def delete():
    try:
        os.remove("json/searchFiles.json")
    except FileNotFoundError:
        messagebox.showinfo(
            title="Oops", message="The File hasn't been created yet, nothing to delete")

# ----------------------------Date Query Function------------------------------- #


# ---------------------------- UI SETUP ------------------------------- #

class FindFilesWindow:
    def __init__(self, parent) -> None:
        self.frame = tk.Frame(parent, padx=35, pady=35)
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
        self.query_button = tk.Button(self.frame, text="Date Query", width=30)
        self.query_button.grid(row=6, column=1)


        # Text
        self.text = tk.Text(self.frame, height=5, width=30)
        self.text.grid(row=3, column=1)

    def searchFile(self) -> None:
        fnameInput = self.fileEntry.get()
        fpathInput = self.pathEntry.get()
        searchResult = find_files(fnameInput, fpathInput)
        self.text.insert(tk.END, f"{searchResult}")
    
    def save(self) -> None:
        


class MainWindow:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.childWindows = []
        self.childCommandInstances = []

        # Create a root object for the rest of the items
        self.frame = tk.Frame(parent)

        # Create buttons
        self.findFilesButton = tk.Button(
            self.frame,
            text='Find Files',
            command=self.gotoFindFiles)

    def makeCommandWindow(self) -> tk.Toplevel:
        newWindow = tk.Toplevel(self.parent)
        self.childWindows.append(newWindow)
        return newWindow

    def makeFindFiles(self) -> None:
        newParent = self.makeCommandWindow()
        newParent.title("FindFiles Function")
        self.childCommandInstances.append(FindFilesWindow(newParent))





if __name__ == "__main__":
    #Global Config
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()



