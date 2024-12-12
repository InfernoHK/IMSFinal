import os
from sys import stdout
from getkey import getkey, keys
from ansi.color import fg
from ansi import cursor
import random
global automation
automation = False
global inventory
global sales_velocity
global money
money = 10000  # Starting money, you can adjust this initial amount
day_counter = 0
global total_purchases
total_purchases = 0





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

def automatic_orders():
  global automation
  automation = input("Turn on automatic orders? (y/n): ")
  if automation == "y":
    automation = True
    print("Automatic orders turned on")
   
    main_menu()


  else:
    automation = False
    print("Automatic orders turned off")
    main_menu()
   

def main_menu():
  
  
        
  choice = menu(["Storage","New Day","Changes","Finances","Automatic Orders","Exit"])
  if choice == 1:
    Storage()
        
  elif choice == 2: 
    NewDay()
            
  elif choice == 3:
      
    Changes()
          
  elif choice == 4:
    Finances()

  elif choice == 5:
    automatic_orders()

  elif choice == 6:
    exit()
            
def Storage():
  
  global inventory  # Make sure inventory is accessible
    
  choice = menu(["Add Item","Delete Item", "View Inventory","Purchase Inventory","Exit"])
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
    purchase_stock()

  elif choice == 5:
    main_menu()
    os.system('clear')


def show_analysis():
    global money
    global reorder_point
    LEAD_TIME = 7
    if day_counter >= 5:
        for item in inventory.items:
            sales_velocity = (item.max_capacity - item.current_numbers)/day_counter
            reorder_point = sales_velocity * LEAD_TIME
            safety_stock = sales_velocity * 2
            
            suggested_order = min(
                (reorder_point + safety_stock) - item.current_numbers,
                item.max_capacity - item.current_numbers
            )
            
            print(f"\nAnalysis for {item.name}:")
            print(f"Sales Velocity: {sales_velocity:.2f} units per day")
            print(f"Reorder Point: {reorder_point:.2f} units")
            if suggested_order > 0:
                print(f"Suggested Order: {suggested_order:.2f} units")
                total_cost = suggested_order * item.cost_price
                print(f"Estimated Cost: ${total_cost:.2f}")
                print(f"Current Balance: ${money:.2f}")
                print(f"Balance after purchase will be: ${money - total_cost:.2f}")
                
                accept = input("\nWould you like to accept this order? (y/n): ")
                if accept.lower() == 'y':
                    money -= total_cost
                    item.current_numbers += suggested_order
                    total_purchases += total_cost
                    print(f"\nOrder accepted! Purchased {suggested_order:.0f} units of {item.name}")
                    print(f"New stock level: {item.current_numbers}")
                    print(f"Current balance: ${money:.2f}")
            else:
                print("Stock levels adequate - no order needed")
    else:
        print("Analysis not available yet. Please wait until day 5.")
    
    input("\nPress Enter to continue...")
    main_menu()

def NewDay():
    os.system('clear')
    

    print("Starting new day...")
    simulate_sales()
    if automation == True:
       global money, pending_orders, total_purchases
    
       if day_counter >= 5:
          for item in inventory.items:
              sales_velocity = (item.max_capacity - item.current_numbers)/day_counter
              reorder_point = sales_velocity * 7  # LEAD_TIME
              safety_stock = sales_velocity * 2
            
              if item.current_numbers <= reorder_point:
                    suggested_order = min(
                    (reorder_point + safety_stock) - item.current_numbers,
                    item.max_capacity - item.current_numbers
                    )
                    suggested_order = round(suggested_order)
                
                    if suggested_order > 0:
                      total_cost = suggested_order * item.cost_price
                      if money >= total_cost:
                          money -= total_cost
                          item.current_numbers += suggested_order
                          total_purchases += total_cost
                          print(f"\nAuto-reorder triggered for {item.name}")
                          print(f"Ordered {suggested_order:.0f} units")
                          print(f"Delivery expected in 7 days")

                      else:
                          print(f"\nInsufficient funds to reorder {item.name}")
  
    main_menu()
    
def Changes():
    os.system('clear')
    show_analysis()

def simulate_sales():
    global day_counter
    LEAD_TIME = 7

    day_counter += 1
    for item in inventory.items:
        # Generate random number of items sold between 0 and current stock
        items_sold = random.randint(0, int(item.current_numbers/2))
        item.current_numbers -= items_sold
        print(f"Sold {items_sold} units of {item.name}")
        print(f"Remaining stock: {item.current_numbers}")
        
        # Calculate reorder point based on sales velocity
        if day_counter >= 5:
            sales_velocity = (item.max_capacity - item.current_numbers)/day_counter
            reorder_point = sales_velocity * LEAD_TIME
            
            # Check if current stock is below reorder point
            if item.current_numbers <= reorder_point:
                print(f"WARNING: {item.name} stock ({item.current_numbers:.0f}) is below reorder point ({reorder_point:.0f})")
                print(f"Consider restocking soon!")
        print("------------------------")


def purchase_stock():
    global money
    os.system('clear')
    print("\nPurchase Stock")
    print("------------------------")
    print(f"Current Balance: ${money:.2f}")
    
    inventory.view_inventory()
    
    name = input("\nEnter item name to purchase stock: ")
    
    for item in inventory.items:
        if item.name == name:
            available_space = item.max_capacity - item.current_numbers
            if available_space <= 0:
                print(f"\nStorage is full for {item.name}!")
                input("\nPress Enter to continue...")
                Storage()
                return
                
            print(f"\nAvailable space: {available_space}")
            while True:
                try:
                    amount = int(input(f"Enter amount to purchase (max {available_space}): "))
                    if amount <= available_space and amount > 0:
                        total_cost = amount * item.cost_price
                        print(f"\nTotal cost: ${total_cost:.2f}")
                        print(f"Balance after purchase will be: ${money - total_cost:.2f}")
                        confirm = input("Confirm purchase? (y/n): ")
                        
                        if confirm.lower() == 'y':
                            money -= total_cost
                            item.current_numbers += amount
                            total_purchases += total_cost
                          
                            print(f"\nSuccessfully purchased {amount} units of {item.name}")
                            print(f"New stock level: {item.current_numbers}")
                            print(f"Current balance: ${money:.2f}")
                        break
                    else:
                        print("Invalid amount. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
            
            input("\nPress Enter to continue...")
            Storage()
            return
    
    print(f"Item '{name}' not found.")
    input("\nPress Enter to continue...")
    Storage()


def Finances():
    os.system('clear')
    print("\nFinancial Overview")
    print("------------------------")
    
    total_spending = 0
    gross_income = 0
    current_inventory_value = 0
    
    for item in inventory.items:
        # Calculate spending (initial stock + any purchases)
        initial_stock_cost = item.max_capacity * item.cost_price
        total_spending += initial_stock_cost
        
        # Calculate gross income from sales
        items_sold = item.max_capacity - item.current_numbers
        gross_income += items_sold * item.sell_price
        
        # Calculate current inventory value
        current_inventory_value += item.current_numbers * item.cost_price
    
    # Calculate net profit
    total_spending += total_purchases
    net_profit = gross_income - total_spending
    
    print(f"Current Balance: ${money:.2f}")
    print(f"Total Spending: ${total_spending:.2f}")
    print(f"Gross Income: ${gross_income:.2f}")
    print(f"Net Profit: ${net_profit:.2f}")
    print(f"Current Inventory Value: ${current_inventory_value:.2f}")
    print("------------------------")
    
    input("\nPress Enter to return to main menu...")
    main_menu()


  
    