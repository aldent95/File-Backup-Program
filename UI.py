#!/usr/bin/python
#Allows compatibility with any version of Python by checking for both versions of Tkinter
try:
    from Tkinter import *
except ImportError:
    from tkinter import *
from backup import Main_Backup
import tkFileDialog
import ConfigParser


class UI(Tk):
    def initialize(self):
        #Handles setting up most of the GUI
        w = 500;#Window width
        h = 500;#Window height
        sw = self.winfo_screenwidth();#Gets screen width
        sh = self.winfo_screenheight();#Gets screen height
        x=(sw-w)/2;#Calculates the x position for the left side of the window that allows it to be placed in the center of the screen
        y =(sh-h)/2;#Calculates the y position for the top of the window that allows it to be placed in the center of the screen
        self.update();#Forces and update on the window
        self.geometry('%dx%d+%d+%d' % (w,h,x,y));#Sets the windows width, height and position
        self.minsize(int(w),int(h/2));#Sets the minimum size of the window
        
        self.columnconfigure(0,weight=1);#Configure all used columns to automaticly resize
        self.columnconfigure(1,weight=1);
        self.columnconfigure(2,weight=1);
        self.columnconfigure(3,weight=1);
        self.columnconfigure(4,weight=1);
        self.rowconfigure(1,weight=1);#Configures the row uesd for the text area to automaticly resize
        
        self.title("Dent & Heath File Backup System");#Sets the title
        self.grid();#Sets the layout to use grid
        
        Label(self,padx=2,text="Enter backup year").grid(row=0,column=0,sticky='E'+'W');#Setup and place the entry label
        self.entry = Entry(self);#Setup the entry box
        self.entry.grid(column=1,row=0,sticky='E'+'W');#Place the entry box


        self.configureOutput()
        self.setupButtons();
    def loadSettings(self):
        config = ConfigParser.ConfigParser()
        config.read('Settings.ini')
        self.arguments['inputDirectory'] = config.get('settings','inputLocation')
        if config.get('settings', 'override') == 'True':
            self.arguments['overrideArg'] = True
        else:
            self.arguments['overrideArg'] = False
    def configureOutput(self):
        self.output = Text(self);#Setup the text area
        self.output.grid(column=0,row=1,sticky='E'+'W'+'N'+'S',columnspan=5);#Place the text area, spanning 4 columns
        #self.output.insert('end',"Output\n");#Add some testing text to the text area
        self.output.configure(state='disabled');#Disable the text area
    def setupButtons(self):
        #Handles creating and setting up all the buttons
        outputSelect= Button(self, text="Select backup location", command=self.selectOutput)
        outputSelect.grid(column=2,row=0,sticky='E'+'W')
        copyButton= Button(self, text="Copy", command=self.copy)
        copyButton.grid(column=3,row=0,sticky='E'+'W')
        deleteButton= Button(self, text="Delete", command=self.delete)
        deleteButton.grid(column=4,row=0,sticky='E'+'W')
    def selectOutput(self):
        directory = tkFileDialog.askdirectory()
        self.arguments['outputDirectory'] = str(directory)
    def copy(self):
        try:
            self.arguments['year'] = int(self.entry.get())
        except ValueError:
            self.arguments['year'] = ""
        self.arguments['deleteArg'] = False
        if self.validCheck():
            Main_Backup(self.arguments)
            self.output.configure(state='normal')
            self.output.delete(1.0,'end')
            self.output.insert('end', "Copy Complete")
            self.output.configure(state='disabled')
        
    def delete(self):
        try:
            self.arguments['year'] = int(self.entry.get())
        except ValueError:
            self.arguments['year'] = ""
        self.arguments['deleteArg'] = True
        if self.validCheck():
            Main_Backup(self.arguments)
            self.output.configure(state='normal')
            self.output.delete(1.0,'end')
            self.output.insert('end', "Delete complete")
            self.output.configure(state='disabled')
    def validCheck(self):
        self.output.configure(state='normal')
        self.output.delete(1.0,'end')
        passed = True
        if self.arguments['year'] == "":
            self.output.insert('end', "Please select a year\n")
            passed = False
        if self.arguments['outputDirectory'] == "":
            self.output.insert('end', "Please select an output location\n")
            passed = False
        if self.arguments['inputDirectory'] == "":
            self.output.insert('end', "Please check Settings.ini as the input location has failed to load\n")
            passed = False
        if self.arguments['deleteArg'] == "":
            self.output.insert('end', "Please contact dev, something has gone VERY wrong\n")
            passed = False
        if self.arguments['overrideArg'] == "":
            self.output.insert('end', "Please contact dev, something has gone VERY wrong\n")
            passed = False
        self.output.configure(state='disabled')
        return passed
    def __init__(self):
    #Handles the initial call to create a GUI
       parent = '';
       Tk.__init__(self,parent);#Parent constructor
       self.arguments = {'inputDirectory':'', 'outputDirectory':'', 'year':'', 'deleteArg':'', 'overrideArg':False}
       self.loadSettings()
       self.parent = parent;#Store the parent
       self.initialize();#Initilize the GUI
       self.mainloop();#Start the main loop

if __name__ == "__main__":
    import sys
    main = UI();
