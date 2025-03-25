import gspread
import statistics
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
SURVEY = SHEET.worksheet("survey_results")
data = SURVEY.get_all_values()
headings = data.pop(0)
headings.pop(0)
SUMMARISED_QUESTIONS = headings

def process_user_command():
    """
    Requests user to indicate what function they want to
    perform via command:
    - 'add' adds new survey data to existing spreadsheet
    - 'delete' removes a given individual's set of responses from the spreadsheet
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
        print("- 'analyse' to conduct general analysis over all survey data")
        print("- 'delete' to delete a record based on an inputted name")
        print("- 'exit' to exit the application\n")
        user_command = input("Enter your command here: \n")
        validity_check = validate_user_command(user_command)
        if validity_check:
            return user_command
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


def get_user_data():
    """
    Gets survey input for a given responder from the user.
    """
    print("Adding survey data...\n")
    print("Please enter a value between 1 to 5 for the following questions, where appropriate.\n")
    print("5 - Excellent")
    print("4 - Good")
    print("3 - Moderate")
    print("2 - Poor")
    print("1 - Very Poor\n")

    user_responses = []
    questions = get_questions()
    print(questions)
    while True:
        user_name = input("Please enter your name: ")
        user_name_checked = check_existing_names(user_name)
        user_responses.append(user_name_checked)
        for question in questions:
            print(question + ": \n")
            while True:
                try:
                    user_response = int(input("Answer: "))
                    if user_response in range(1,6):
                        print(f"User entered {user_response}.\n")
                        user_responses.append(user_response)
                        break
                    else:
                        print("Not a number between 1 and 5. Please enter a valid value.")
                except ValueError:
                    print("Not a number between 1 and 5. Please enter a valid value.")
        return user_responses


def update_survey_sheet(new_data_row):
    """
    Updates the survey spreadsheet with a list of new values, provided by the user.
    """
    print(f"Updating survey results spreadsheet...\n")
    SURVEY.append_row(new_data_row)
    print(f"Update complete!\n")


def read_user_data(name):
    """
    Reads a row of data from the spreadsheet based on the employees name, which is passed by user.
    """
    print(f"Reading {name}'s data...\n")
    name_cell = SURVEY.find(name)
    user_scores = SURVEY.row_values(name_cell.row)
    return user_scores


def delete_row(name):
    """
    Takes the validated name input by the user and deletes the corresponding row in the spreadsheet.
    """
    print(f"Deleting {name}'s data...\n")
    name_cell = SURVEY.find(name)
    SURVEY.delete_rows(name_cell.row)
    print(f"Deletion complete. {name}'s entry has been removed from the survey.\n")


def validate_name(name):
    """
    Takes the name input by user following "read" command and checks whether it matches any of the names 
    in the spreadsheet. If no match is found, user will be prompted until a match is detected, then the 
    valid name is passed back to the main() function.
    """
    existing_names = SURVEY.col_values(1)
    while name not in existing_names:
        name = input("The name you entered does not exist. Please submit the name of a respondent who has completed the survey.\n")
    return name


def check_existing_names(name):
    """
    Takes the name input by user following "add" command and checks whether it matches any of the names 
    in the spreadsheet. If the name matches, user will be prompted until a new name is submitted, then the 
    valid name is passed back to the main() function.
    """
    existing_names = SURVEY.col_values(1)
    while name in existing_names:
        print("The name you entered already exists - you have already completed the survey!\n")
        name = input("Please enter the name of a new respondent.\n")
    return name


def validate_user_command(user_command):
    """
    Checks that the initial command passed by user to perform on data set is valid.
    """
    command_list = ['add', 'delete', 'list', 'read', 'analyse', 'exit']
    if user_command in command_list:
        return True
    else:
        return False


def get_questions():
    """
    Returns a list of the survey questions. The get_notes function returns 
    a list of lists containing cell notes which needs to be unpacked before
    returning.
    """
    questions = SURVEY.get_notes()
    return questions[0][1:]


def analyse_user_data(user_data):
    """
    Conducts analysis on data passed through the main function following
    a "read" command, displaying the question responses and statistics
    for the given individual. 
    """
    #notes = SURVEY.row_values(1)
    survey_data = SURVEY.get_all_values()
    print(f"Analysing user data...\n")
    user_name = user_data.pop(0)  # removes the first value in the row (i.e. name) so we can convert the remaining numbers in the string to int for analysis
    print(f"Survey data being fed into averages function: {survey_data}\n")
    #print(f"Qs data being fed into averages function: {summarised_questions}\n")
    survey_averages = get_question_averages(survey_data, False)
    print(f"Printing survey_averages from within analyse_user_data function: {survey_averages}")
    print(f"Results for {user_name} are as follows:")
    question_index = 0
    for score in user_data:  # this for loop prints out a list of strings containing a shortened version of the question along with the individual's score
        print(f"{SUMMARISED_QUESTIONS[question_index]} : {score}")
        question_index += 1
    converted_scores = [int(x) for x in user_data]  # converts user data to a list of integers so that numerical analysis can be performed
    average_score = statistics.mean(converted_scores)
    score_variance = statistics.variance(converted_scores)
    if score_variance > 1.5:
        variance_string = "high level of variance, indicating significant disparity between the 'best' and 'worst' aspects of the job."
    elif score_variance > 1:
        variance_string = "moderate level of variance."
    else:
        variance_string = "low level of variance, suggesting the respondent is very consistent in their perception about the qualities of the job." 
    print(f"{user_name} gave an average score of {average_score} across all questions.")
    print(f"{user_name} had a variance of {round(score_variance, 1)} in their scores. This is a {variance_string}")

    min_score = min(converted_scores)
    print(f"Min score: {min_score}")  # TESTING
    lowest_scored_questions = []
    i = 0
    while i < 10:
        if converted_scores[i] == min_score:
            lowest_scored_questions.append(SUMMARISED_QUESTIONS[i])
        i += 1
    print(f"Lowest scored question(s) scored {min_score} as follows: {lowest_scored_questions}.")


def analyse_survey():
    """
    Conducts analysis of the overall survey data set, returning
    summarised information for each question, overall statistics,
    highlighting questions with low scores i.e. areas to work on
    """
    print(f"Analysing survey data...\n")
    # intialise survey_data variable, pulling all data from survey
    survey_data = SURVEY.get_all_values()
    #print(f"Survey data: {survey_data}\n")
    # call get_questions and assign to questions variable
    
    #print(summarised_questions)
    #names = []  # May not be required, might only need to pop names off if they're not used
    #print(f"Names list: {names}\n")  
    #print(f"Names list without NAME heading: {names[1:]}\n")

    
    print(f"Printing summarised questions from inside analyse_survey, should exclude name: {SUMMARISED_QUESTIONS}")
    #print(f"List of responses: {survey_data}\n")
    #print(f"Summarised questions: {summarised_questions}\n")
    #print(f"Response values only, should only be numbers: {response_values}\n")
    print("See below for average scores for each question in the survey:\n")
    question_averages = get_question_averages(survey_data, True)
    #print(f"Printing question averages from analyse_survey function after call: {question_averages}")

    question_index = 0
    for average_score in question_averages:  # this for loop prints out a list of strings containing a shortened version of the question along with the average organisational score
        print(f"{SUMMARISED_QUESTIONS[question_index]} : {average_score}")
        question_index += 1

    print("-- End of analyse_survey function")
    return question_averages
    
    
    # potential nested array, list of qs and results. or zip dictionary?
    # print dataset for testing
    # print statement "Results for Individual questions"
    # loop through dataset, gett


def get_question_averages(survey_data, full_analysis):
    """
    Extracts only values (excludes questions & names) from survey data. Calculates and overall average score.
    Calculates individual questio
    """
    print("Printing questions and length of q array in getqavgs function")
    print(SUMMARISED_QUESTIONS)
    print(len(SUMMARISED_QUESTIONS))

    response_values = []
    for data_row in survey_data:
        data_row.pop(0)
        for value in data_row:
            if len(value) == 1:
                response_values.append(int(value))
            else:
                continue
    print(f"Response values within get_question_averages, should be all numbers: {response_values}")
    
    overall_average = statistics.mean(response_values)
    if full_analysis:  # Only outputs the organisational score if the function is being called from analyse_survey, not analyse_user_data
        print(f"Overall average score across organisation: {round(overall_average, 1)}")
    
    # initialises totals variable depending on the number of responses
    question_totals = []
    number_of_responses = len(survey_data) - 1  # survey data contains all column data including headings, so need to loop through the lenth minus 1
    #print(f"Number of responses, should be 14: {number_of_responses}")
    for index in range(len(SUMMARISED_QUESTIONS)):
        question_totals.append(0)
    print(f"Question totals from inside get_question_averages function: {question_totals}")
    #print(f"Initialised question totals, should all be 0: {question_totals}")

    #Gets totals for each question
    print(survey_data)
    survey_data.pop(0)
    print(survey_data)
    for dataset in survey_data:
        #dataset.pop(0)
        for index in range(len(dataset)):
            print(f"Current value being looked at: {dataset[index]}")
            print(f"Index: {index}")
            question_totals[index] += int(dataset[index])
    print(f"List of total scores for each question: {question_totals}\n")
    print(f"Number of responses which the totals will be divided by: {number_of_responses}")

    # for loop comprehensions to generate a list of averages then round all values to one decimal place
    question_averages = [x/number_of_responses for x in question_totals]
    question_averages_rounded = ['%.1f' % x for x in question_averages]
    #print(f"List of average scores for each question: {question_averages_rounded}\n")
    #print("Q1 below")
    #print(question_averages_rounded[0])

    return question_averages_rounded

def make_recommendations(analysed_data):
    """
    Makes recommendations based on the average scores calculated across the dataset.
    """
    print("Recommendations for your organisation based on overall survey results...\n")
    #print(analysed_data)
    float_data = [float(x) for x in analysed_data]  # converts the list of strings of averages into floats for numerical comparison
    #print(float_data)
    low_scores = []
    high_scores = []
    question_index = 0
    for score in float_data:
        if score <= 2.5:  # If the average score is below 2.8 it is deemed "Low". Arbitrary, can be changed.
            low_scores.append(SUMMARISED_QUESTIONS[question_index])
        elif score >= 3.5:  # If the average score is above 3.2 it is deemed "High". Arbitrary, can be changed.
            high_scores.append(SUMMARISED_QUESTIONS[question_index])
        question_index += 1
    print(f"Low scoring questions: {low_scores}")
    print(f"High scoring questions: {high_scores}\n")
    low_scores_headings = []
    for question in low_scores:
        low_scores_headings.append(question[5:])
    print("Based on the average scores, major areas of concern for the organisation should be: ")
    #print([heading for heading in low_scores_headings])
    for heading in low_scores_headings:
        print(f"{heading}")


def main():
    """
    Run all program functions
    """
    while True:  # The program will keep requesting user commands until they input the "exit" command
        user_command = process_user_command()
        print(f"MAIN: user command is {user_command}") #TESTING
        match user_command:
            case 'add':
                user_responses = get_user_data()
                update_survey_sheet(user_responses)
            case 'delete':
                delete_name = input("Enter the exact name of the respondent you wish to delete survey results for: \n")
                validated_delete_name = validate_name(delete_name)
                delete_row(validated_delete_name)
            case 'list':
                list_respondents()
            case 'read':
                read_name = input("Enter the exact name of the respondent you wish to see survey results for: \n")
                validated_read_name = validate_name(read_name)
                user_data = read_user_data(validated_read_name)
                analyse_user_data(user_data)
            case 'analyse':
                analysed_data = analyse_survey()
                make_recommendations(analysed_data)
            case 'exit':
                print("The application will now close.")
                quit()


print("Welcome to DT Survey Analytics.\n")
main()
