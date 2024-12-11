
# Example usage
def main():
    inventory = Inventory()
    
    # Menu for user interaction
    while True:
        print("\n1. Add item")
        print("2. Delete item")
        print("3. View inventory")
        print("4. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            name = input("Enter item name: ")
            max_capacity = int(input(f"Enter max capacity for {name}: "))
            sell_price = float(input(f"Enter selling price for {name}: "))
            cost_price = float(input(f"Enter cost price for {name}: "))
            inventory.add_item(name, max_capacity, sell_price, cost_price)
        
        elif choice == "2":
            name = input("Enter the name of the item to delete: ")
            inventory.delete_item(name)
        
        elif choice == "3":
            inventory.view_inventory()
        
        elif choice == "4":
            print("Exiting program.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
