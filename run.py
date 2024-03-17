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

        data_str = input('Type your data here then press Enter: ')

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

def update_sales_worksheet(new_data):
    """
    Updates sales worksheet in Sheets,
    adding new row containing collected data.
    """
    print('Sales worksheet is being updated.\n')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(new_data)
    print('Sales worksheet update was successful.\n')

# Functions called to take user input and update appropriate worksheet.
data = get_sales_data()
sales_data = [int(num) for num in data] # Type conversion.
update_sales_worksheet(sales_data)
