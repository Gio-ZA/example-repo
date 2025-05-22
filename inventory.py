"""
This program manages a shoe inventory system. It allows the user to:

- Read shoe data from an inventory file.
- Add new shoes to the inventory.
- View all available shoes.
- Restock shoes with the lowest quantity.
- Search for shoes by code.
- Calculate the total value of each shoe type.
- Identify the shoe with the highest quantity available for sale.

The shoe data is stored in a text file called 'inventory.txt'.
"""
import re
from tabulate import tabulate


class Shoe:
    """
    Represents a shoe item in the inventory.

    Attributes:
        country (str): The country where the shoe is sourced.
        code (str): The unique product code for the shoe.
        product (str): The brand or name of the shoe.
        cost (int): The price of a single pair of the shoe.
        quantity (int): The number of shoe pairs available in stock.

    Methods:
        get_cost(): Returns the cost of the shoe.
        get_quantity(): Returns the quantity in stock.
        __str__(): Returns a string representation of the shoe's
        attributes.
    """
    def __init__(self, country, code, product, cost: int, quantity: int):
        """
        Initializes a Shoe object with its details.

        Args:
            country (str): The country where the shoe is sourced.
            code (str): The unique code identifying the shoe.
            product (str): The brand or name of the shoe.
            cost (int): The cost per pair of shoes.
            quantity (int): The quantity of shoes in stock.
        """
        self.country = country
        self.code = code
        self.product = product
        self.cost = int(cost)
        self.quantity = int(quantity)

    def get_cost(self):
        """
        Returns the cost of the shoe.

        Returns:
            int: The price of a single pair of the shoe.
        """
        return self.cost

    def get_quantity(self):
        """
        Returns the quantity of shoes available in stock.

        Returns:
            int: The number of shoe pairs available.
        """
        return self.quantity

    def __str__(self):
        """
        Returns a string representation of the shoe's details.

        Returns:
            str: A human-readable string representation of the shoe's
            details.
        """
        return (
            f"Country: {self.country} | Code: {self.code} | "
            f"Product: {self.product} | Cost: R{self.cost:,.2f} | "
            f"Quantity: {self.quantity}"
        )


# List to store instances of the Shoe class.
shoe_list: list[Shoe] = []


def read_shoes_data():
    """
    Reads shoe data from the 'inventory.txt' file and populates the shoe
    list.

    This function assumes that the file exists and that the first line
    is a header.
    Each line in the file represents a shoe and is expected to contain:
        - country
        - product code
        - product name
        - cost
        - quantity

    Returns:
        None
    """
    try:
        with open("inventory.txt", "r") as file:
            # Skip over header.
            next(file)

            for line in file:
                line_split_up = line.strip().split(",")
                country = line_split_up[0]
                code = line_split_up[1]
                product = line_split_up[2]
                cost = int(line_split_up[3])
                quantity = int(line_split_up[4])
                shoe_list.append(Shoe(country, code, product, cost, quantity))

    except FileNotFoundError:
        print("The file 'inventory.txt' was not found.")


def cancel_capture(user_input):
    """
    Checks if the user wants to cancel the current input operation.

    If the user enters 'x' (in any case), a cancellation message is
    printed and the function returns True to indicate the process
    should stop.

    Args:
        user_input (str): The input entered by the user.

    Returns:
        bool: True if the user entered 'x' to cancel, otherwise False.
    """
    if user_input.lower() == "x":
        print("Capture cancelled.")
        return True
    return False


def capture_shoes():
    """
    Prompts the user to input details for a new shoe and adds it to the
    shoe list.

    The user will be prompted to provide:
        - Country the shoe is from
        - Shoe code
        - Product name (brand of the shoe)
        - Price per pair of shoes
        - Quantity of shoes in stock

    Returns:
        None
    """
    print("\nEnter 'x' at any time to cancel.\n")

    # Validate required text fields
    # Country:
    while True:
        country = input("Enter the country the shoe is from: ").strip().title()

        if cancel_capture(country):
            return

        if not country or not country.replace(" ", "").isalpha():
            print("Invalid country. Please enter only letters and spaces.")
        else:
            break

    # Code
    while True:
        code = input("Enter the shoe code (e.g., SKU12345): ").strip().upper()

        if cancel_capture(code):
            return

        if not re.fullmatch(r"SKU\d+", code):
            print("Invalid code format. Code must start with 'SKU'" +
                  "followed by numbers (e.g., SKU12345).")
        else:
            break

    # Product
    while True:
        product = input("Enter what brand shoe it is: ").strip().title()

        if cancel_capture(product):
            return

        if not product or not product.replace(" ", "").isalpha():
            print("Invalid product. Please enter only letters and spaces.")
        else:
            break

    # Cost
    while True:
        cost_input = input("Enter the price for one pair: ").strip()

        if cancel_capture(cost_input):
            return

        try:
            cost = int(cost_input)
            if cost < 0:
                print("Error: Cost cannot be negative")
            else:
                break

        except ValueError:
            print("Error: Please enter a valid integer for cost")

    # Quantity
    while True:
        quantity_input = input("Enter the amount of pairs: ").strip()

        if cancel_capture(quantity_input):
            return

        try:
            quantity = int(quantity_input)
            if quantity < 0:
                print("Error: Quantity cannot be negative.")
            else:
                break
        except ValueError:
            print("Error: Please enter a valid integer for quantity.")

    # Create and store shoe if all inputs are valid
    shoe_list.append(Shoe(country, code, product, cost, quantity))
    print("Shoe successfully captured.")


def view_all():
    """
    Displays all shoes in the inventory list.

    This function prints the details (country, code, product, cost, and
    quantity) of each shoe in the list in table format.

    Returns:
        None
    """
    table_data = []
    for shoe in shoe_list:
        table_data.append([
            shoe.country,
            shoe.code,
            shoe.product,
            f"R{shoe.cost:,.2f}",
            shoe.quantity
        ])

    headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def re_stock():
    """
    Finds the shoe with the lowest stock in the inventory and offers to
    restock it.

    If the user agrees to restock, the function prompts for the restock
    amount and updates the quantity of the shoe in both the list and the
    'inventory.txt' file.

    Returns:
        None
    """
    shoe_list_ascending = sorted(shoe_list, key=Shoe.get_quantity)
    lowest_stock_shoe = shoe_list_ascending[0]

    print("\nThe following shoe has the lowest stock: ")
    print(lowest_stock_shoe)

    request_restock = input(
        "Would you like to restock the above shoe?(Y/N) "
    ).strip().upper()

    if request_restock == "Y":
        while True:
            restock_input = input(
                "Enter the amount you want to restock with(or 'x' to cancel): "
            )

            if restock_input.lower() == "x":
                print("Restock cancelled.")
                return

            try:
                restock_amount = int(restock_input)
                if restock_amount < 0:
                    print("Error: Restock amount cannot be negative.")
                else:
                    break
            except ValueError:
                print("Error: Please enter a valid integer.")

        lowest_stock_shoe.quantity += restock_amount
        print(f"Updated quantity: {lowest_stock_shoe.quantity}")

        # Update the quantity of the matching shoe in the original
        # shoe_list
        for i, shoe in enumerate(shoe_list):
            if shoe.code == lowest_stock_shoe.code:
                shoe_list[i] = lowest_stock_shoe
                break

        # Add/replace updated shoe to file
        with open("inventory.txt", "w") as file:
            file.write("Country,Code,Product,Cost,Quantity\n")

            for shoe in shoe_list:
                file.write(f"{shoe.country},{shoe.code},{shoe.product},"
                           f"{shoe.cost},{shoe.quantity}\n")

        print("Inventory file updated successfully")

    else:
        print("Restock cancelled")


def search_shoe():
    """
    Prompts the user for a shoe code and searches for the shoe in the
    inventory.

    If a shoe with the given code is found, its details are displayed.
    Otherwise, an error message is shown.

    Returns:
        None
    """
    shoe_code_input = input(
        "Enter the shoe code for the shoe you are looking for: "
    ).strip().upper()
    found = False
    for shoe in shoe_list:
        if shoe_code_input == shoe.code:
            print("Shoe found!")
            print(shoe)
            found = True
            break

    if not found:
        print("Invalid code or shoe not found")


def value_per_item():
    """
    Calculates and prints the total value of each shoe in the inventory.

    The total value is calculated by multiplying the cost by the
    quantity for each shoe, and then displaying the result.

    Returns:
        None
    """
    for shoe in shoe_list:
        value = shoe.cost * shoe.quantity
        print(f"Total value for: {shoe.code} = R{value:,.2f}")


def highest_qty():
    """
    Displays the shoe with the highest quantity in stock.

    The function sorts the shoe list in descending order based on
    quantity and prints the shoe with the highest stock.

    Returns:
        None
    """
    shoe_list_descending = sorted(shoe_list, key=Shoe.get_quantity,
                                  reverse=True)
    print(f"The following item is on sale:\n{shoe_list_descending[0]}")


# Populate shoe_list, list
read_shoes_data()

# Display the main menu and handle user input for inventory management
while True:
    try:
        menu_input = int(
            input(
                """\nWould you like to:
        1. View all shoes
        2. Capture a shoe
        3. Restock shoes
        4. Search for a shoe
        5. Show total value of all shoes
        6. Show for sale item
        7. Quit

        Enter selection: """
            )
        )
        # Handle user input
        if menu_input == 1:
            view_all()
        elif menu_input == 2:
            capture_shoes()
        elif menu_input == 3:
            re_stock()
        elif menu_input == 4:
            search_shoe()
        elif menu_input == 5:
            value_per_item()
        elif menu_input == 6:
            highest_qty()
        elif menu_input == 7:
            print("Goodbye!")
            break
        else:
            print("Invalid input given. Select a valid number")
    except ValueError:
        print("Invalid input. Select a valid number")

# Checked up on the re.fullmatch function to validate the code input.
# Source: https://docs.python.org/3/library/re.html#re.fullmatch

# Created cancel_capture() that was not requested by the task just to
# make capture_shoe() a bit easier to read.
