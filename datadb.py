__author__ = 'jeff'

import sqlite3
import os
from datetime import time, date, datetime
import time

class DataDB:

    def __init__(self):
        self.__wasOpened = False
        hr12 = ('%I:%M:%S')
        hr24 = ('%H:%M:%S')
        self.__hr12 = hr12
        self.__hr24 = hr24
        # self.__now = time.strftime("%c")


    def open(self, path):
        self.__path = path
        self.__conn = sqlite3.connect(self.__path)
        self.__cur = self.__conn.cursor()
        if os.path.getsize(self.__path) == 0:
            self.create()

        try:
            self.__conn = sqlite3.connect(self.__path)
            self.__cur = self.__conn.cursor()
        except:
            print("Database file not found, creating...")
            self.create()
            self.__conn = sqlite3.connect(self.__path)
            self.__cur = self.__conn.cursor()

        self.__wasOpened = True


    def create(self):
        print("creating database table 'clockdb'")
        createTable = """CREATE TABLE clockdb(ID INTEGER primary key, hrformat VARCHAR, updated_at TIME)"""
        self.__cur.execute(createTable)
        self.__conn.commit()


    def insert(self, id, hrformat):
        now = time.strftime("%c")
        try:
            r = (id, hrformat, now)
            self.__cur.execute('INSERT INTO clockdb VALUES (?,?,?)', r)
            self.__conn.commit()
        # except Exception as e:
        #     print(str(e))
        except:
            self.update(id,hrformat)


    def update(self, id, hrformat):
        now = time.strftime("%c")
        v = (hrformat, id)
        n = (now, id)
        self.__cur.execute('UPDATE clockdb SET hrformat = ? WHERE ID = ?', v )
        self.__cur.execute('UPDATE clockdb SET updated_at = ? WHERE ID = ?', n)
        self.__conn.commit()


    def read(self, id):
        t = (id,)
        # print("Currently configured clocks")
        # for row in self.__cur.execute('SELECT * FROM clockdb'):
        #     print(row)

        for row in self.__cur.execute('SELECT * FROM clockdb WHERE ID = ?', t):
            # print("Current default setting for clock # %s is %s" % (row[0], row[1]))
            return row[1]

        # value = self.__cur.execute('SELECT * FROM clockdb WHERE ID = ?', t)
        # print(value)
        # self.close(id)


    def currentConfig(self):
        # print("Currently configured clocks")
        for row in self.__cur.execute('SELECT * FROM clockdb'):
            # print(row)
            if row[1] == self.__hr24:
                # print("Clock #%s - 24 hour format" % row[0])
                print("Clock #%s --> 24 hour format, last updated %s "% (row[0], str(row[2])))
            elif row[1] == self.__hr12:
                # print("Clock #%s - 12 hour format" % row[0], )
                # print("Last updated at: %s "% str(row[2]))
                print("Clock #%s --> 12 hour format, last updated %s "% (row[0], str(row[2])))

    def close(self,id):
        if self.__wasOpened:
            self.read(id)
            self.__cur.close()
            self.__conn.close()

if __name__ == "__main__":
    print("Please launch using 'main.py")