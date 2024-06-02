import sqlite3
import os


connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS Items (
               Item_no INT NOT NULL,
               Item_name TEXT NOT NULL,
               Price INT
        )
''')

connection.commit()

#insert data into the data base
def insert_items(item_number,item,price):
    cursor.execute("INSERT INTO Items (Item_no,Item_name, Price) VALUES (?, ?, ?)", (item_number,item, price))
    connection.commit()

#close the connection
def close_connection():
    cursor.close()
    connection.close()

def delete_record(delete_item):
    cursor.execute("DELETE FROM Items WHERE Item_no=?",(delete_item,))
    connection.commit()