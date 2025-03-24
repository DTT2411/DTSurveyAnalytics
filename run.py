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

def get_user_function():
    """
    Requests user to indicate what function they want to
    perform via command:
    - 'add' adds new survey data to existing spreadsheet
    - 'list' returns a list of names of individual respondents
    - 'read' returns a specific individual's responses
    - 'analyse' returns general analysis over all survey data
    - 'exit' exits the program
    """
    while True:
        print("Please enter a command to perform on the survey\n")
        print("- 'add' to add new survey data to existing spreadsheet")
        print("- 'list' to see a list of names of individual respondents")
        print("- 'read' to read a specific individual's responses")
        print("- 'analyse' to conduct general analysis over all survey data\n")
        user_command = input("Enter your command here: \n")
        validate_user_function(user_command)



def list_respondents():
    """
    Returns a list of the names of all survey respondents
    """



def get_survey_data():
    """
    Gets survey input for a given responder from the 
    user.
    """
    print("Adding survey data...\n")
    print("Please enter a value between 1 to 5 for the following questions.\n")
    print("5 - Excellent")
    print("4 - Good")
    print("3 - Moderate")
    print("2 - Poor")
    print("1 - Very Poor\n")

    user_responses = []
    questions = [
        "Q1 - How satisfied are you with your job role?:",
        "Q2 - How satisfied are you with your pay and remuneration?:",
        "Q3 - How well do you feel supported by staff initiatives (e.g. Cycle to Work scheme, staff clubs, social events)?:",
        "Q4 - How satisfied are you with the number of holidays you receive per year?:",
        "Q5 - How would you rate the staff benefits on offer (e.g. gym fee subsidy, staff development fund)?:",
        "Q6 - How would you describe the quality of support provided to you by your line manager?:",
        "Q7 - How would you rate the opportunities for career growth within the organisation?:",
        "Q8 - How do you feel regarding life-work balance and workload within your current role?:",
        "Q9 - How well valued do you feel within your current role?:",
        #"Q10 - Rate your likelihood of recommending working at our organisation to others?:"
        "Q10 - Would you recommend working in our organisation to others? Answer 'Y' for yes or 'N' for no"
    ]

    for question in questions:
        print(question + "\n")
        user_response = input("Answer: ")
        validate_data(user_response, question)
        user_responses.append(user_response)

    #Q1 - 
    #Q2
    #Q3
    #Q4


    #would you like to enter another set of survey data? Y/N
    #Yes = loop back to start of this function
    #No = go back to get_user_function input


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

def validate_user_function(user_command):
    """
    Checks that the initial function passed by user to 
    perform on data set is valid.
    """
    command_list = ['add', 'list', 'read', 'analyse']
    print(user_command)
    if user_command in command_list:
        if user_command == 'add':
            get_survey_data()
        elif user_command == 'list':
            list_respondents()
        elif user_command == 'read':
            respondent_name = input("Enter the exact name of the respondent you wish to see survey results for: \n")
            read_user_data(respondent_name)
        elif user_command == 'analyse':
            analyse_data()
        elif user_command == 'exit':
            #exit
        else:
            print("Command was not valid. Please enter a valid command from the list provided.\n")
            get_user_function()

def validate_data(value, question):
    """
    Checks that the user input intended to be submitted 
    to the spreadsheet is in a valid format.
    """
    valid = False
    #if question == "Q10 - Would you recommend working in our organisation to others? Answer 'Y' for yes or 'N' for no":


def analyse_data():
    """
    Conducts analysis of the overall survey data set, returning
    summarised information for each question, overall statistics,
    highlighting questions with low scores i.e. areas to work on
    """

def main():
    """
    Run all program functions
    """
    print("Hello world")
    get_user_function()

print("Welcome to DT Survey Analytics.\n")
main()
