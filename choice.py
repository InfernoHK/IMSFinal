import os
from sys import stdout
from getkey import getkey, keys
from ansi.color import fg
from ansi import cursor
import random

global  inventory
global sales_velocity
global daycount
daycount = 1

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
    print("\nCurrent Inventory Status:")
    print("------------------------")
    for item in self.items:
        print(f"Name: {item.name}")
        print(f"Current Stock: {item.current_numbers}")
        print(f"Maximum Capacity: {item.max_capacity}")
        print(f"Selling Price: ${item.sell_price}")
        print(f"Cost Price: ${item.cost_price}")
        print("------------------------")

inventory = Inventory()

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
  
        
  choice = menu(["Storage","New Day","Changes","Finances"])
  if choice == 1:
    Storage()
        
  elif choice == 2: 
    NewDay()
            
  elif choice == 3:
      
    Changes()
          
  elif choice == 4:
    Finances()
            
def Storage():
  global inventory  # Make sure inventory is accessible
    
  choice = menu(["Add Item","Delete Item", "View Inventory","Exit"])
  if choice == 1:
      name = input("Enter item name: ")
      current_numbers = int(input(f"Enter current numbers for {name}: "))
      max_capacity = int(input(f"Enter max capacity for {name}: "))
      sell_price = float(input(f"Enter selling price for {name}: "))
      cost_price = float(input(f"Enter cost price for {name}: "))
      inventory.add_item(name, current_numbers, max_capacity, sell_price, cost_price)  # Use instance method
      Storage()

  elif choice == 2:
    name = input("Enter the name of the item to delete: ")
    inventory.delete_item(name)
    Storage()

  elif choice == 3:
    inventory.view_inventory()
    Storage()
  elif choice == 4:
    main_menu()


def NewDay():
    daycount =+ 1

    print("Starting new day...")
    simulate_sales()
    main_menu()


def simulate_sales():
    for item in inventory.items:
        # Generate random number of items sold between 0 and current stock
        items_sold = random.randint(0, item.current_numbers)
        item.current_numbers -= items_sold
        print(f"Sold {items_sold} units of {item.name}")
        print(f"Remaining stock: {item.current_numbers}")
        sales_velocity.append(itmes_sold)

def changes():
    LEAD_TIME = 7  # days
    if daycount > 5:  # days
    
      for item in inventory.items:
          # Calculate sales velocity (average daily sales)
          sales_velocity = (item.max_capacity - item.current_numbers) / daycount
          
          # Calculate reorder point using lead time
          reorder_point = sales_velocity * LEAD_TIME
          
          # Calculate suggested order quantity
          safety_stock = sales_velocity * 2  # Buffer stock for 2 days
          suggested_order = (reorder_point + safety_stock) - item.current_numbers
          
          print(f"\nAnalysis for {item.name}:")
          print(f"Sales Velocity: {sales_velocity:.2f} units per day")
          print(f"Reorder Point: {reorder_point:.2f} units")
          if suggested_order > 0:
              print(f"Suggested Order: {suggested_order:.2f} units")
              print(f"Estimated Cost: ${suggested_order * item.cost_price:.2f}")
          else:
              print("Stock levels adequate - no order needed")
      else:
        print("Analysis not available yet. Please wait until day 5.")
