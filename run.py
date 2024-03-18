import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# APIs connected to enable interaction with spreadsheet.
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('sandwich_data')

def get_sales_data():
    """
    Collects sales figures input from the user.
    """
    # Continuous loop until broken.
    while True:
        print('Please enter sales data from the last market.')
        print('Data should be six numbers separated by commas.')
        print('Example: 10,20,30,40,50,60\n')

        data_str = input('Type your data here then press Enter:\n')

        # Converts user-provided string to a list of strings.
        sales_data = data_str.split(',')

        # Calls validate_data function with user-provided data as argument.
        # If data was successfully validated, breaks the loop.
        if validate_data(sales_data):
            break

    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if one or more strings cannot be converted to int,
    or if there are less or more than the expected 6 values.
    """
    # The try block potentially raises an error.
    try:
        # Checks all values can be used as integers.
        [int(value) for value in values]

        # Checks if exactly 6 values. If not, raises a customised error.
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values required. {len(values)} were provided.'
            )
        
    # The except block responds to any errors raised.
    except ValueError as e:
        print(f'Invalid data: {e}. Please try inputting again.\n')

        # Returns False if 'the data is valid' is a false statement.
        return False
    
    # Returns True if it is true that the data is valid.
    return True

def calculate_surplus(sales_row):
    """
    Compares day's sales with stock to calculate surplus of each sandwich type.
    A negative surplus indicates that extra sandwiches were made to meet demand.
    """
    print('Product surpluses are being calculated.\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]

    surplus = []
    for made, sold in zip(stock_row, sales_row):
        surplus.append(int(made) - sold)

    return surplus

def update_worksheet(new_data, worksheet):
    """
    Updates appropriate worksheet in Sheets, adding
    new row containing collected or calculated data.
    """
    print(f'The {worksheet} worksheet is being updated.\n')
    target_worksheet = SHEET.worksheet(worksheet)
    target_worksheet.append_row(new_data)
    print(f'The {worksheet} worksheet update was successful.\n')

def decide_stock_levels():
    """
    Based on the last 5 days of business, decides stock levels for the next day.
    Calculates averages of recent sales figures. Adds 10% to accommodate growth.
    """
    sales = SHEET.worksheet('sales')
    columns = []
    # Python's (0, 6) is Excel's (1, 7) because the 0th is shunned.
    for i in range(1, 7):
        # Making a list of lists based on sandwich type columns, NOT based on day rows.
        column = sales.col_values(i)
        # Append only last 5 rows / days of the sandwich type column. That is, from (row) index -5 to end.
        columns.append(column[-5:])

    print('Recommended stock levels are being calculated.\n')
    new_stock_row = []
    for column in columns:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_row.append(round(stock_num))
    print('Recommended stock levels were successfully calculated.\n')

    return new_stock_row

# Can take out the ignition to run only a particular function instead, presuming no parameters nor return yet.
def main():
    """
    Runs all program functions.
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')

    surplus_data = calculate_surplus(sales_data)
    update_worksheet(surplus_data, 'surplus')

    stock_data = decide_stock_levels()
    update_worksheet(stock_data, 'stock')

print("Welcome to The Sandwich Shop's product data analyser.")
print("Together, we can minimise food waste while remaining well-stocked.\n")

main()
