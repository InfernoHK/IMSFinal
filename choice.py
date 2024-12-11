import os
from sys import stdout
from getkey import getkey, keys
from ansi.color import fg
from ansi import cursor
import random

global menu_sys_list 
menu_sys_list = []

class Item:
  def __init__(self, name, current_numbers, max_capacity, sell_price, cost_price):
    self.name = name
    self.current_numbers = current_numbers
    self.max_capacity = max_capacity
    self.sell_price = sell_price
    self.cost_price = cost_price

    
    def __str__(self):
      return f"Item: {self.name}, Current Numbers: {self.current_numbers}, Max Capacity: {self.max_capacity}, Sell Price: ${self.sell_price}, Cost Price: ${self.cost_price}"

class Inventory:
  def __init__(self):
    self.items = []
  
  def add_item(self, name, current_numbers, max_capacity, sell_price, cost_price):
    # Check if item already exists, to prevent duplicates (optional)
    for item in self.items:
      if item.name == name:
        print(f"Item '{name}' already exists.")
        return
    new_item = Item(name, current_numbers, max_capacity, sell_price, cost_price)
    self.items.append(new_item)
    print("Added item: ", new_item.name)

  def delete_item(self, name):
    # Find the item and delete it
    for item in self.items:
      if item.name == name:
        self.items.remove(item)
        print(f"Deleted item: {name}")
        return
    print(f"Item '{name}' not found.")
  
  def view_inventory(self):
    if not self.items:
      print("Inventory is empty.")
    else:
      for item in self.items:
        print(item)



def menu(choices):


  global pos
  pointer = fg.boldblue('>')
  for choice in choices:
    print(choice)
  print(cursor.hide()+cursor.up()*(len(choices))+pointer, end='    ')
  stdout.flush()

  pos = 1
  while 1:
    key = getkey()
    text = f'{""} {choices[pos-1]}'
    if (key == '\x1b[A' or key == 'w') and pos > 1:
      pos -= 1
      print(f'\r{text}\r' + cursor.up() + pointer + \
            fg.bold(f'{""} {choices[pos-1]}'), end = '      ')
    elif (key == '\x1b[B' or key == 's') and pos < len(choices):
      pos += 1
      print(f'\r{text}\r' + cursor.down() + pointer + \
            fg.bold(f'{""} {choices[pos-1]}'), end = '    ')
    elif key == '\n':
      print(cursor.down()*(len(choices)-pos)+cursor.show())
      return pos
    elif key.isdecimal():
      number = int(key)
      if 0 < number <= len(choices):
        print(cursor.down()*(len(choices)-pos)+cursor.show())
        return number
    stdout.flush()
def main_menu():
  
    if menu_sys_list == []:
        
        choice = menu(["Storage","New Day","Changes","Finances"])
        if choice == 1:
            Storage()
            
        elif choice == 2:
            
            NewDay()
            
        elif choice == 3:
            
            Changes()
            
        elif choice == 4:
            menu_sys_list.append("Exit")
            Finances()
                 
def Storage():
  inventory = Inventory()
  choice = menu(["Add Item","Delete Item", "View Inventory","Exit"])
  if choice == 1:
    name = input("Enter item name: ")
    current_numbers = int(input(f"Enter current numbers for {name}: "))
    max_capacity = int(input(f"Enter max capacity for {name}: "))
    sell_price = float(input(f"Enter selling price for {name}: "))
    cost_price = float(input(f"Enter cost price for {name}: "))
    inventory.add_item(name, current_numbers, max_capacity, sell_price, cost_price)

  elif choice == 2:
    name = input("Enter the name of the item to delete: ")
    inventory.delete_item(name)

  elif choice == 3:
    inventory.view_inventory()

  elif choice == 4:
    main_menu()
    


   