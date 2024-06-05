from tkinter import *
from tkinter import ttk
from tkinter import messagebox
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

def insert_items(item_number,item,price):
    cursor.execute("INSERT INTO Items (Item_no,Item_name, Price) VALUES (?, ?, ?)", (item_number,item, price))
    connection.commit()
    
#close the connection
def close_connection():
    cursor.close()
    connection.close()

def search(searchh):
        cursor.execute("SELECT * FROM Items WHERE Item_name LIKE ? OR Item_name LIKE ? or Item_no LIKE ?",
                      ('%' + searchh + '%', 'le%' + searchh + '%',searchh))
        result = cursor.fetchall()
        return result

     
def save_changes(old_itemno,updated_item,updated_price,new_itemno):
      cursor.execute("UPDATE Items SET Item_no=?,Item_name=?,Price=? WHERE Item_no=?",
                     (old_itemno,updated_item,updated_price,new_itemno))
      connection.commit()

def delete_record(delete_item):
    cursor.execute("DELETE FROM Items WHERE Item_no=?",(delete_item,))
    connection.commit()

window =Tk()
#-----------------------------------------------------------------------------create the window
window.configure(bg="#E1F0DA")
screen_width=window.winfo_screenwidth()
screen_height=window.winfo_screenheight()
window.geometry("1100x600")
window.title("Python Project")

#-----------------------------------------------------------------------------------------------------------
def refresh():
    # Update the item number label
    global next_item_no
    next_item_no = last_no() + 1
    update_item_no_label(next_item_no)
    
    # Clear the search results
    result_box.delete(0, END)
    search_entry.delete(0, END)

    # Clear the entry boxes
    update_box_item.delete(0, END)
    update_box_price.delete(0, END)
    
    price_entry.delete(0,END)
    item_entry.delete(0,END)
    search_entry.delete(0,END)
    
def search_items():
    searchh=search_entry.get()
    results=search(searchh)
    result_box.delete(0,END)
    if results:
      for row in results:
        items_text = f"{row[0]}  -   {row[1]}  -  {row[2]}" 
        result_box.insert(END,items_text)
    else:
      result_box.insert(END," No matching items found....")
    search_entry.delete(0,END)


#read the last record of the data base
def last_no():
    query = "SELECT Item_no FROM Items ORDER BY ROWID DESC LIMIT 1"
    cursor.execute(query)
    last_item_no = cursor.fetchone()
    if last_item_no is not None:
        return last_item_no[0]
    else:
        return 0
def count():
     item_no=last_no()+1
     return item_no   

item_no_label=Label(window,
                text="",
                font=('Arial',15),
               )
item_no_label.place(x=20,y=50) 

def update_item_no_label(item_number):
    item_number=count()
    item_no_label.config(text=f"Item Number: {item_number}")

next_item_no = last_no()+1
update_item_no_label(next_item_no)

def add_items():
    try:
        item_number=count()
        item=item_entry.get()
        price=price_entry.get()
        price=int(price)
        insert_items(item_number,item,price)
        price_entry.delete(0,END)
        item_entry.delete(0,END)
        search_items()
        update_item_no_label(item_number)
    except:
        messagebox.showerror(title="Error",
                            message="Error occurd Try again!")    

def print_selected(event):
        update_box_item.delete(0, END)
        update_box_price.delete(0, END)
        selected_index=result_box.curselection()
        for i in selected_index:
            global selected_item
            selected_item=result_box.get(i)
            selected_item=selected_item.split("  -  ",)
            update_box_item.insert(END,selected_item[1])
            update_box_price.insert(END,selected_item[2])


def save():
    try:
        old_itemno=selected_item[0]
        old_item=selected_item[1]
        old_price=selected_item[2]
        new_itemno=old_itemno

        updated_item=update_box_item.get()
        updated_price=update_box_price.get()
        updated_price=int(updated_price)

            
        save_changes(old_itemno,updated_item,updated_price,new_itemno)
        search_items()

        update_box_item.delete(0, END)
        update_box_price.delete(0, END)
    except:
        messagebox.showerror(title="Error",
                            message="Error occurd Try again!") 


def delete():
        try:
            delete_item=selected_item[0]
            delete_record(delete_item)
            search_items()
            update_box_item.delete(0, END)
            update_box_price.delete(0, END)
        except:
            messagebox.showerror(title="Error",
                            message="Error occurd Try again!") 

#----------------------------------------------------------------------------create the label
start_label=Label(window,
                  text="-Welcome to Python Project-",
                  font=("Comic Sans",9)
                )

start_label.pack()

#------------------------------------------------------------------------------add items & prices
item_label=Label(window,text="Item name",font=('Arial',15))
item_label.place(x=20,y=95)

item_entry=Entry(window,
                 font=('Arial',15),
                 highlightbackground="black", 
                 highlightcolor="gray",
                 width=30, 
                 highlightthickness=2)
item_entry.place(x=150,y=95)
#---------------------------------------------------------
price_label=Label(window,
                 text="Price",
                 font=('Arial',15))

price_label.place(x=20,y=130)

price_entry=Entry(window,
                 font=('Arial',15),
                 highlightbackground="black", 
                 highlightcolor="gray", 
                 highlightthickness=2)
price_entry.place(x=150,y=130)
#-----------------------------------------------------------------------------------
add_button=Button(window,
                  text="Add",
                  font=('Arial',15),
                  height=1,
                  width=15,
                  bg="#80BCBD",
                  command=add_items)

add_button.place(x=150,y=170)
#--------------------------------------------------------------------------------------

#---------------------------------search part------------------
search_label=Label(window,
                   text="Search here",
                   font=('Arial',15),
                   )
search_label.place(x=20,y=280)

search_entry=Entry(window,
                   font=('Arial',15),
                   highlightbackground="black", 
                   highlightcolor="gray", 
                   highlightthickness=2,
                   width=25
                   )

search_entry.place(x=170,y=280)

search_button=Button(window,
                     text="Search",
                     font=('Arial',15),
                     height=1,
                     width=15,
                     command=search_items
                     )
search_button.place(x=150,y=320)


result_box=Listbox(window,
                   font=('Arial',15),
                   width=35,
                   height=22,
                   borderwidth=10,
                   bd=6, relief="flat", highlightbackground="black", highlightthickness=2
                   )

result_box.place(x=620, y=35, bordermode='outside')

#-------------------------------------------------------------------------------

update_box_item=Entry(window,
                font=('Arial',15),
                highlightbackground="black", 
                highlightcolor="gray", 
                highlightthickness=3,
                width=30)

update_box_item.place(x=40,y=400)

update_box_price=Entry(window,
                font=('Arial',15),
                highlightbackground="black", 
                highlightcolor="gray", 
                highlightthickness=3,
                width=15)

update_box_price.place(x=385,y=400)

save_button=Button(window,
                  text="Save Changes",
                  font=("Arial",15),
                  height=1,
                  width=15,
                  command=save
                  )

save_button.place(x=150,y=450)

delete_button=Button(window,
                     text="Delete Record",
                    font=("Arial",15),
                    height=1,
                    width=15,
                    bg="red",
                    fg="white",
                    command=delete
                     )
delete_button.place(x=150,y=520)

refresh_button = Button(window,
                        text="↻",
                        font=("Calibari", 20,"bold"),
                        command=refresh,
                        bd=0,
                        highlightthickness=0,
                        bg="#E1F0DA")
refresh_button.place(x=1040, y=10)

result_box.bind("<Button-1>",print_selected)

window.mainloop()
close_connection()