import sqlite3


# connection = sqlite3.connect("Sandaru Hardware.db")
connection = sqlite3.connect("database.db")
cursor = connection.cursor()


cursor.execute('''
        CREATE TABLE IF NOT EXISTS Items (
               Item_name TEXT NOT NULL,
               Price INT
        )
''')

connection.commit()

while True:
    choice = input("""
    for enter data press 1 - for search data press 2 - for edit data press 3       
   :""")

    if choice == "1":
        item = input("Enter item name: ")
        price = input("Enter price: ")

        cursor.execute("INSERT INTO Items (Item_name, Price) VALUES (?, ?)", (item, price))
        connection.commit()
        print("Data inserted successfully!")