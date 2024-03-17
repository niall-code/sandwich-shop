import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('sandwich_data')

def get_sales_data():
    """
    Gets sale figures input from the user
    """
    print('Please enter sales data from the last market.')
    print('Data should be six numbers separated by commas.')
    print('Example: 10,20,30,40,50,60\n')

    data_str = input('Type your data here then press Enter: ')

    # Convert user-provided string to a list of strings
    sales_data = data_str.split(',')

    validate_data(sales_data)

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if one or more strings cannot be converted to int,
    or if there are less or more than the expected 6 values.
    """
    try:
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values required. {len(values)} were provided.'
            )
    except ValueError as e:
        print(f'Invalid data: {e}. Please try inputting again.\n')

get_sales_data()
