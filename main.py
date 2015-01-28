

# from datadb import *
from clock import *
import os

newConnection = DataDB()

class Launch:

    def main(self,id):
        # hr12 = ('%I:%M:%S')
        # hr24 = ('%H:%M:%S')

        c1 = Clock(id)


    def getId(self):
        try:
            id = int(input("Please enter an integer to create and track your clock:  "))
            self.main(id)
            assert type(id) == type(1), "id is not an integer: %r" % id
        except:
            print("Clock ID must be an integer, try again")
            self.getId()


    def firstRun(self):

        if os.path.isfile("hasrun.dat"):
            self.getId()
        else:
            print("""
            First run hints:

            * Change the clock settings (12hr or 24hr).
            * The program keeps settings in a database so they'll persist
            * Feel free to make as many clocks as you like!

            """)
            open("hasrun.dat","w").close()
            self.getId()

launcher = Launch()
launcher.firstRun()