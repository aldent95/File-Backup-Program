#!/usr/bin/python
try:
    from Tkinter import *
except ImportError:
    from tkinter import *
import tkFileDialog
import ConfigParser

class SettingsMenu(Toplevel):
    def hide(self):  # Hides the window
        self.withdraw()
    def __init__(self, parent, config):
        Toplevel.__init__(self, parent)
        self.config=config
        self.setup() 
        self.protocol("WM_DELETE_WINDOW", self.hide)  # Changes the close button to just hide the window
        self.withdraw()
    def setup(self):
        self.inputDir = self.config.get('settings', 'inputLocation')
        self.override = self.config.get('settings', 'override')
        print self.override
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        w = 400  # Sets up the window position on the screen
        h = 150
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2

        Label(self,padx=2,text='Copy Input Location').grid(row=0,column=0,sticky='E'+'W')
        Label(self,padx=2,text='Make sure the input location is set to the root directory of the original files').grid(row=1,column=0,sticky='EW')
        Label(self,padx=2,text='Override existing files').grid(row=2,column=0,sticky='E'+'W')
        
        self.inputEntry = Entry(self)
        self.inputEntry.grid(row=0,column=1,sticky='E'+'W')
        self.inputEntry.insert(END, self.inputDir)
        self.inputEntry.config(state='readonly')

        self.overrideEntry = Entry(self)
        self.overrideEntry.grid(row=2,column=1,sticky='E'+'W')
        self.overrideEntry.insert(END, self.override)
        self.overrideEntry.config(state='readonly')

        inputSelect = Button(self, text='Change', command=self.changeInput)
        inputSelect.grid(row=0,column=2,sticky='E'+'W')

        overrideChange = Button(self, text='Switch', command=self.changeOverride)
        overrideChange.grid(row=2,column=2,sticky='E'+'W')

        save = Button(self, text = 'Save', command=self.save)
        save.grid(row=3,column=0,sticky='W')

        cancel = Button(self,text='Cancel', command=self.close)
        cancel.grid(row=3,column=2,sticky='E')
        
        
        self.update()
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.resizable(width=0, height=0)
        self.grid()
        self.title("Settings Menu")

    def changeInput(self, content=""):
        if content == "":
            content = str(tkFileDialog.askdirectory())
        self.inputEntry.config(state='normal')
        self.inputEntry.delete(0,END)
        self.inputEntry.insert(END, content)
        self.config.set('settings','inputLocation', content)
        self.inputEntry.config(state='readonly')
    def getInput(self):
        return self.config.get('settings', 'inputLocation')
    def getOverride(self):
        return self.config.get('settings', 'override')
    def changeOverride(self, c=""):
        content = ""
        if c == "":
            content = self.overrideEntry.get()
        if content == 'True':
            content = True
        else:
            content = False
        content = not content
        self.overrideEntry.config(state='normal')
        self.overrideEntry.delete(0,END)
        self.overrideEntry.insert(END, str(content))
        self.config.set('settings','override', content)
        self.overrideEntry.config(state='readonly')

    def save(self):
        self.config.write(open('Settings.ini', 'w+'))
        self.hide()
    def close(self):
        self.config.set('settings', 'inputLocation', self.inputDir)
        self.config.set('settings', 'override', self.override)
        self.changeInput(self.inputDir)
        self.changeOverride(self.override)
        self.hide()


