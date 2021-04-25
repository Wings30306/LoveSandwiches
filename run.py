# python code goes here
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

""" SETTINGS """
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")


def get_sales_data():
    """
    Get sales figures input from user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers, separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("Data is valid")
            break
    return sales_data


def validate_data(values):
    """
    Inside the try, convert all string values into integers.
    Raise ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values
    """
    print(values)
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_sales_worksheet(data):
    """
    Update sales worksheet, add a new row with the list data provided
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully!\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stuck and calculate the surplus for each item type

    The surplus is defined as the the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[len(stock) - 1]
    surplus_row = [int(stock_num) - sales_num for stock_num, sales_num in zip(
        stock_row, sales_row)]
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(surplus_row)
    return surplus_row


def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")
    # column = sales.col_values(3)
    # print(column)
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        stock = round((sum(int_column)/5)*1.1)
        new_stock_data.append(stock)

    stock_worksheet = SHEET.worksheet("stock")
    stock_worksheet.append_row(new_stock_data)
    return new_stock_data


def main():
    """
    Run all program functions
    """
    print("Welcome to Love Sandwiches Data Automation")
    data = get_sales_data()
    sales_data = [int(value) for value in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)
    sales_data = get_last_5_entries_sales()
    calculate_stock_data(sales_data)


main()
