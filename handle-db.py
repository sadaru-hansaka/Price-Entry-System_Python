import sqlite3


# connection = sqlite3.connect("Sandaru Hardware.db")
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS Items")
cursor.execute('''
        CREATE TABLE IF NOT EXISTS Items (
               Item_name TEXT NOT NULL,
               Price INT
        )
''')

connection.commit()

cursor.execute("PRAGMA table_info(Items)")
columns = cursor.fetchall()
for column in columns:
    print(column)

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

    elif choice == "2":
        search = input("Search by item name: ")
        cursor.execute("SELECT * FROM Items WHERE Item_name LIKE? OR Item_name LIKE ?",
                       ('%' + search + '%', '%' + search + '%'))
        result = cursor.fetchall()
        if result:
            for row in result:
                print(row)
        else:
            print("No matching items found.")

    elif choice == "3":
        print("Editing part")
    
    elif choice=="q":
        cursor.execute('DELETE  FROM Items')
        connection.commit()
        print("Database Cleared")
        break

    else:
        cursor.execute('SELECT * FROM Items')
        out = cursor.fetchall()
        for r in out:
            print(f"{r[0]} - Rs.{r[1]}")
        break

cursor.close()
connection.close()