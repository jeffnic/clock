__author__ = 'jeff'


from tkinter import *
import os
import time
from datadb import *

class Clock:
    def __init__(self, id):
        hr12 = ('%I:%M:%S')
        hr24 = ('%H:%M:%S')
        self.__hr12 = hr12
        self.__hr24 = hr24
        self.__id = id

        self.root = Tk()
        self.root.title("Clock ID # " + str(self.__id))
        self.root.resizable(width=False, height=False)
        self.frame = Frame(self.root, padx = 7, pady = 7, border = 4, relief = 'raised' )
        self.frame.grid(row = 1, column = 1)
        self.setHr = IntVar()
        self.label = Label(self.frame, text="", font=('Comic Sans',40, "bold"))
        self.root.iconbitmap("logo.ico")
        hrbuttn12 = Radiobutton(self.frame, text = "12 Hour", variable = self.setHr, command = self.setFormat, value = 12).grid(row = 2, column = 1)
        hrbuttn24 = Radiobutton(self.frame, text = "24 Hour", variable = self.setHr, command = self.setFormat, value = 24).grid(row = 2, column = 2)
        closeButton = Button(self.frame, text = "Exit", command = self.close, bg = "#FFFFC2", relief = "ridge", highlightcolor = "green", padx = 11, pady = 0, borderwidth = 4).grid(row = 2, column = 3)

        #insert stuff here
        dbConnection = DataDB()
        self.__dbConnection = dbConnection
        try:
            dbConnection.open("clockdb.db")
            defValue = self.__dbConnection.read(self.getID())
            if defValue == self.__hr12:
                print("Restoring clock #%s to 12 hr format" % self.__id)
                self.setHr.set(12)
                # self.setFormat()

            elif defValue == self.__hr24:
                print("Restoring clock #%s to 24 hr format" % self.__id)
                self.setHr.set(24)
                # self.setFormat()

            else:
                print("No config found, setting default to 24 hr format")
                self.setHr.set(24)
                self.__dbConnection.insert(self.__id,self.__hr24)

        except Exception as e:
            print("No configuration found, setting default to 24 hr format")
            self.setHr.set(24)
            print(e)

        self.label.grid(row = 1, column = 1, columnspan = 3)
        self.tick()
        self.root.mainloop()


    def setDefault(self):
        defValue = self.__dbConnection.read(self.getID())
        try:
            if defValue == self.__hr24:
                self.setHr.set(24)


            elif defValue == self.__hr12:
                self.setHr.set(12)
        except:
            self.setHr.set(24)

        # print(defValue)

    def close(self):
        print("Thank you for using Clock!\n")
        print("These are your currently configured clocks")
        self.__dbConnection.currentConfig()
        # self.setFormat()
        self.root.destroy()


    def getFormat(self):
        hr12 = ('%I:%M:%S')
        hr24 = ('%H:%M:%S')

        if self.setHr.get()==12:
            return hr12

        else:
            return hr24

    def setFormat(self):

        if self.setHr.get()==12:
            hrformat = ('%I:%M:%S')
            print("Configuring 12 hour default setting for clock #%s " % self.__id)
            self.__dbConnection.open("clockdb.db")
            self.__dbConnection.insert(self.getID(),hrformat)

        elif self.setHr.get()==24:
            hrformat = ('%H:%M:%S')
            print("Configuring 24 hour default setting for clock #%s " % self.__id)
            self.__dbConnection.open("clockdb.db")
            self.__dbConnection.insert(self.getID(),hrformat)


    def tick(self):
        time1 = ''
        time2 = time.strftime(self.getFormat())
        if time2 != time1:
            time1 = time2
            self.label.config(text = time2)
        self.root.after(200,self.tick)


    def getID(self):
        return self.__id


if __name__ == "__main__":
    print("Please launch using 'main.py")