import sqlite3
import os
import csv
from Employee import Employee

class Employees:

    def getFile(self, fileName):
        folder = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(folder, fileName)
        return file
    
    def getFromCsv(self):
        file = self.getFile("Employees.csv")
        try:
            with open(file) as csvfile: 
                employees = csv.reader(csvfile, delimiter= ";")
                list = []
                for row in employees:
                    employee = Employee() 
                    employee.id = None # SQLite will use rowId
                    employee.firstName = row[0]
                    employee.lastName = row[1]
                    employee.role = row[2]
                    employee.loginName = row[3]
                    list.append(employee)
        except FileNotFoundError:
            print("CSV file not found")

        list.sort(key = lambda employee: (employee.role)) # keeping objects in one list at first allows sorting if desired
        print("Employees fetched from csv") 
        return list

    def getFromDb(self):
        connection = sqlite3.connect(self.getFile("biker.db")) # opens connection at each button press
        cursor = connection.cursor()

        self.createTable(cursor)
        list = [] # returns an empty list if the following checks fail:
 
        if self.databaseExists(cursor): 
            self.insertIntoEmployees(connection, cursor)
            list = self.populateToEmployees(cursor) # if succeeded, list filled with employee objects

        connection.commit()
        connection.close()

        return list

    def createTable(self, cursor):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees(  
        id INTEGER PRIMARY KEY,
        first_name TEXT (30) NOT NULL, 
        last_name TEXT (30) NOT NULL, 
        role TEXT (30) NOT NULL, 
        loginname TEXT (30) NOT NULL UNIQUE)
        """)

    def databaseExists(self, cursor): # check if database created/exists
        cursor.execute("""SELECT count(name) FROM sqlite_master WHERE type='table' AND name='employees'""")
        first = cursor.fetchone()[0]
        if first == 1:
            print("Table created or exists")
            return True
        else: 
            print("Table does not exist")

    def insertIntoEmployees(self, connection, cursor):
        try:
            cursor.execute("SELECT max(rowid) from employees") # check if CSV already imported by checking row count
            count = cursor.fetchone()[0]
            if count == None:  
                query = """INSERT INTO employees (id, first_name, last_name, role, loginname) VALUES (?, ?, ?, ?, ?);"""
                employees = self.getFromCsv()
                for empl in employees:
                    employee = [empl. id, empl.firstName, empl.lastName, empl.role, empl.loginName]
                    cursor.execute(query, employee)
                print("Employees imported to database")
            else: print(f"{count} rows detected, nothing imported to database")
        except: 
            print("Error occurred, import to database failed")
            connection.rollback()

    def populateToEmployees(self, cursor):
        list = []
        try:
            cursor.execute("""SELECT * FROM employees;""")
            rows = cursor.fetchall()

            for row in rows:
                print(f"Accessed row {row[0]}: {row[2]}")
                employee = Employee()
                employee.id = row[0]
                employee.firstName = row[1]
                employee.lastName = row[2]
                employee.role = row[3]
                employee.loginName = row[4]
                list.append(employee)
        except: print("Error occurred, unable to populate to employee objects")

        return list
