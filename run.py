import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("DT_survey_analytics")

survey = SHEET.worksheet("survey_results")
data = survey.get_all_values()

#print(data)

def get_user_input():
    """
    Requests user to indicate what function they want to
    perform via command:
    - "add" to add new survey data to existing spreadsheet
    - "read" to read a specific individual's responses
    - "analyse" to conduct general analysis over all survey data
    """

def get_survey_data():
    """
    Gets survey input for a given responder from the 
    user.
    """

def update_sheet(new_data_row):
    """
    Updates the survey spreadsheet with a list of new
    values, provided by the user.
    """

def read_user_data(name):
    """
    Reads a row of data from the spreadsheet based on 
    the employees name, which is passed by user.
    """

def validate_user_fucntion(function):
    """
    Checks that the initial function passed by user to 
    perform on data set is valid.
    """

def validate_data(values):
    """
    Checks that the user input intended to be submitted 
    to the spreadsheet is in a valid format.
    """

def main():
    """
    Run all program functions
    """
    print("Hello world")

print("Welcome to DT Survey Analytics.\n")
main()
