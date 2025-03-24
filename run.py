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
        validity_check = validate_user_function(user_command)
        if validity_check:
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
                print("The application will now close.")
                quit()
        else:
            print("Invalid command. Please enter a command from the list provided.")
    

def list_respondents():
    """
    Returns a list of the names of all survey respondents
    """
    respondent_column = SHEET.worksheet("survey_results").col_values(1)
    respondent_names = respondent_column[1:]
    print("**See below for a list of all respondents.**\n")
    for respondent in respondent_names:
        print(respondent)


def get_survey_data():
    """
    Gets survey input for a given responder from the user.
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
        "Q10 - Rate your likelihood of recommending working at our organisation to others?:"
    ]
    while True:
        user_name = input("What is your name?: ")
        user_responses.append(user_name)
        for question in questions:
            print(question + "\n")
            while True:
                try:
                    user_response = int(input("Answer: \n"))
                    if user_response in range(1,6):
                        print(f"User entered {user_response}.\n")
                        user_responses.append(user_response)
                        break
                    else:
                        print("Not a number between 1 and 5. Please enter a valid value.")
                except ValueError:
                    print("Not a number between 1 and 5. Please enter a valid value.")
        print(user_responses)
        #call update_sheet function to add the user_responses into the spreadsheet
        continue_data_entry = input("Would you like to enter another set of survey data? Y/N: \n")
        if continue_data_entry == "Y" or continue_data_entry == "y":
            user_responses = [] #resets the local user_responses variable for next set of data
            continue
        else: 
            get_user_function() #moves user back to main command menu


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
    command_list = ['add', 'list', 'read', 'analyse', 'exit']
    if user_command in command_list:
        return True
    else:
        return False

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
