
from tkinter.font import BOLD, Font
from Employees import Employees
from tkinter import *
from tkinter import ttk
import os
import tkinter.messagebox
from PIL import ImageTk, Image
import datetime

class Biker:
    def __init__(self, root):
        root.title("Biker Haaglanden")
        root.geometry("1090x600+100+75")
        root.minsize(width = 1085, height = 600)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack()

        self.mainFrame = ttk.Frame(self.notebook, relief = RAISED)
        self.notebook.add(self.mainFrame, text = "Start")

        self.employeeFrame = ttk.Frame(self.notebook, padding = 20, relief = RAISED)
        self.notebook.add(self.employeeFrame, text = "Medewerkers")

        # additional notebook tabs and corresponding buttons for extra access to the tabs:
        titles = ["Klanten", "Fietsen", "Accessoires"]
        
        for i, title in enumerate(titles):
            frame = ttk.Frame(root)
            self.notebook.add(frame, text = title)
            ttk.Label(self.mainFrame, text = title).grid(row = 2 + i, column = 1, sticky = W)
            button = ttk.Button(self.mainFrame, text = "🔍",  width = 2, command = lambda frame = frame: self.notebook.select(tab_id = frame))
            button.grid(row = 2 + i, column = 3, sticky = W, padx = 20)
            
        font = "Verdana"
        width = 30

        # widgets for mainFrame
        folder = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(folder, "bicycle.jpg") # https://freepngimg.com/png/3756-bicycle-png-image
        image = Image.open(file)
        resizedImg = image.resize((int(image.width * 0.5), int(image.height * 0.5)))
        tkImg = ImageTk.PhotoImage(resizedImg)
        
        self.imageLabel = Label(self.mainFrame, relief = RAISED, borderwidth = 3)
        self.imageLabel.img = tkImg
        self.imageLabel.config(image = self.imageLabel.img)
        self.imageLabel.grid(row = 1, rowspan = 4, column = 0, padx = 25, pady = 25)

        ttk.Label(self.mainFrame, text = "Biker Hoofdmenu", font = (font, 16, BOLD), foreground = "dark red").grid(row = 0, column = 1, sticky = W, pady = 20)
        ttk.Label(self.mainFrame, text = "Medewerkers").grid(row = 1, column = 1, sticky = W)

        self.button = ttk.Button(self.mainFrame, text = "Haal gegevens op", command = lambda: self.fetch())
        self.button.grid(row = 1, column = 2, sticky = W, padx = 10)

        self.toon = ttk.Button(self.mainFrame, text = "🔍", command = lambda: self.notebook.select(tab_id = self.employeeFrame), width = 2)
        self.toon.grid(row = 1, column = 3, sticky = W, padx = 20)

        ttk.Label(self.mainFrame, text = "Laatst opgehaald:").grid(row = 1, column = 4, sticky = W)
        self.dateLabel = ttk.Label(self.mainFrame, text = "n.v.t.".rjust(20))
        self.dateLabel.grid(row = 1, column = 5, sticky = W)
        
        # widgets for employeeFrame
        self.employees = Employees()
        self.storedEmployees = [] # storing reference, in order to fetch only when requested
        
        ttk.Label(self.employeeFrame, text = "Zoek medewerkers:").grid(row = 0, column = 0, sticky = E, padx = 20, pady = 10)

        self.searchEntry = ttk.Entry(self.employeeFrame, foreground = "black")
        self.searchEntry.insert(0, "Zoek op naam of rol")
        self.searchEntry.grid(row = 0, column = 1, sticky = W)

        ttk.Button(self.employeeFrame, text = "Zoek", command = lambda: self.search()).grid(row = 0, column = 2, sticky = W)
        ttk.Button(self.employeeFrame, text = "Reset", command = lambda: self.reset()).grid(row = 0, column = 2, sticky = E)

        labels = ["Achternaam", "Voornaam", "Rol", "Loginnaam"]

        self.texts = [] # storing text widgets in a list to be able to modify text widgets later on 
        for i, text in enumerate(labels):
            ttk.Label(self.employeeFrame, text = text, font = (font, 12, BOLD)).grid(row = 1, column = i, sticky = W) 
            text = Text(self.employeeFrame, width = width, font = (font, 12)) 
            text.config(background = "seashell", relief = SUNKEN, borderwidth = 1, state = DISABLED)
            text.grid(row = 2, column = i)
            self.texts.append(text)

        # bindings
        self.texts[0].bind_class("Text", '<MouseWheel>', self.scroll) # "scroll" bound to first text widget
        self.searchEntry.bind("<Button-1>", self.clear)
        self.searchEntry.bind("<Return>", self.search)

    # methods
    def lists(self, employees): # makes lists from given employees for use in text widgets, id's not used in interface
        firstNames, lastNames, roles, loginNames = [], [], [], []
        
        for employee in employees:
            firstNames.append(employee.firstName)
            lastNames.append(employee.lastName)
            roles.append(employee.role)
            loginNames.append(employee.loginName)

        formattedLists = ["\n".join(lastNames), "\n".join(firstNames), "\n".join(roles), "\n".join(loginNames)] 
        return formattedLists

    def getTexts(self): # configure text widgets
        for i, text in enumerate(self.texts):
            text.config(state = NORMAL)
            text.delete(0.0, END)
            text.insert(END, self.lists(self.storedEmployees)[i]) # fetch or access stored list, depending on method (fetch or reset)
            text.config(foreground = "black", state = DISABLED)

    def fetch(self): # fetch all data and fill in text widgets / applies to the first two notebook tabs
        self.storedEmployees = self.employees.getFromDb()
        self.getTexts()
        self.button.config(text = "Haal opnieuw op")
        if self.storedEmployees != []: 
            self.dateLabel.config(text = datetime.datetime.now().isoformat(sep = " ", timespec = "seconds"))
            self.showMessage("Medewerkers opgehaald")
        else: self.showError()

    def search(self, event = None): # show only data that matches search results
        if self.storedEmployees != []: 
            results = []
            for employee in self.storedEmployees:
                if self.searchEntry.get().lower() in employee.firstName.lower() or self.searchEntry.get().lower() in employee.lastName.lower() or self.searchEntry.get().lower() in employee.role.lower():
                    results.append(employee)
                    
            for i, text in enumerate(self.texts):
                text.config(state = NORMAL)
                text.delete(0.0, END)
                text.insert(END, self.lists(results)[i]) # makes text lists from search results
                text.config(state = DISABLED)
            
            if results == []: 
                self.showMessage("Geen gegevens gevonden")
                self.reset()  
        else: self.showWarning()

    def reset(self): # back to default lists
        self.getTexts()
        self.searchEntry.delete(0, END)
        self.searchEntry.insert(0, "Zoek op naam of rol")
        self.searchEntry.config(foreground = "gray")
        if self.storedEmployees == []: self.showWarning() 

    def clear(self, event): # clear search text entry
        self.searchEntry.delete(0, END)
        self.searchEntry.config(foreground = "black")

    def scroll(self, event): # to let all four text widgets to scroll (with mouse) synchronously / to prevent separate scrolling 
        for text in self.texts:
            text.yview_scroll(-1*(event.delta), "units") # may not work on Win?

    # alerts
    def showMessage(self, message):
        tkinter.messagebox.showinfo("Showinfo", message) 

    def showWarning(self, warning = "Haal medewerkers eerst op"):
        tkinter.messagebox.showwarning("Showwarning", warning)

    def showError(self, error = "Ophalen niet gelukt"):
        tkinter.messagebox.showerror("Showerror", error)

