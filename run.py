import gspread
import statistics
from termcolor import colored

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


def get_user_type():
    """
    Requests user to indicate what access type they have:
    - 'admin' can use all features and functions
    - 'respondent' can only input and update their own data
    Keeps prompting user until a valid command is entered.
    """
    while True:
        print("Please enter your user type:")
        print("- " + colored("'admin'", 'blue') + " can add or update "
              "responses on behalf others, read individual or whole survey "
              "data, add and delete questions.")
        print("- " + colored("'respondent'", 'blue') + " can add and update "
              "their own responses.")
        print("- " + colored("'exit'", 'blue') + " to exit the application.")
        print("Enter " + colored("'home'", 'blue') + " in any field to return "
              "to this menu.")
        user_type = input("Enter user type:\n")
        if user_type == "exit":
            quit()
        elif user_type == "home":
            print("\n")
            main()
        validated_user_type = validate_command(user_type, "user type")
        if validated_user_type is True:
            return user_type
        else:
            print(colored("You did not enter a valid user type. Please enter "
                  "'admin' or 'respondent'\n", "yellow"))


def validate_password():
    """
    Checks that the user has administrator priveleges by requesting them to
    enter the admin password, which is contained outside of the application
    in a text file named "admin_password.txt".
    """
    admin_password = open('admin_password.txt', 'r').read()
    response = input("Please enter the administrator password:\n")
    main_menu_check(response)
    if response == admin_password:
        print(colored("Password correct. Going to admin command menu...\n",
                      "yellow"))
        return
    else:
        print(colored("Password invalid. Returning to main menu...\n",
                      "yellow"))
        main()


def process_main_command(user_type):
    """
    Requests user to indicate what function they want to perform via command:
    - 'add' adds new survey data to existing spreadsheet
    - 'update' updates values for a given individual
    - 'delete' removes a given individual's set of responses from the
       spreadsheet
    - 'list' returns a list of names of individual respondents
    - 'read' returns a given individual's responses
    - 'add q' adds a new question to the survey
    - 'read q' returns a list of responses for a given question
    - 'delete q' deletes an exiting question within the survey
    - 'analyse' returns general analysis over all survey data
    - 'exit' exits the program
    Admin level users have access to all functions.
    Respondent level users can only access 'add', 'update' and 'exit'.
    Keeps prompting user until a valid command is entered.
    """
    if user_type == "admin":
        while True:
            print("Please enter a command to perform on the survey:\n")
            print("- " + colored("'add'", 'blue') + " to add new survey data "
                  "to existing spreadsheet.")
            print("- " + colored("'update'", 'blue') + " to update existing "
                  "survey data within the spreadsheet")
            print("- " + colored("'delete'", 'blue') + " to delete a record "
                  "based on an inputted name")
            print("- " + colored("'list'", 'blue') + " to see a list of names "
                  "of individual respondents")
            print("- " + colored("'read'", 'blue') + " to read a specific "
                  "individual's responses")
            print("- " + colored("'add q'", 'blue') + " to add a new question "
                  "to the survey")
            print("- " + colored("'read q'", 'blue') + " to read all responses"
                  " for a given question")
            print("- " + colored("'delete q'", 'blue') + " to delete a "
                  "question from the survey and all associated data")
            print("- " + colored("'analyse'", 'blue') + " to conduct general "
                  "analysis over all survey data")
            print("- " + colored("'exit'", 'blue') + " to exit the "
                  "application\n")
            main_command = input("Enter your command here:\n")
            validity_check = validate_command(main_command, "main admin")
            if validity_check:
                return main_command
            else:
                print(colored("Invalid command. Please enter a command from "
                              "the list provided.\n", "yellow"))
    elif user_type == "respondent":
        while True:
            print("Please enter a command to perform on the survey:\n")
            print("- " + colored("'add'", 'blue') + " to add new survey data "
                  "to existing spreadsheet.")
            print("- " + colored("'update'", 'blue') + " to update existing "
                  "survey data within the spreadsheet")
            print("- " + colored("'exit'", 'blue') + " to exit the "
                  "application\n")
            main_command = input("Enter your command here:\n")
            validity_check = validate_command(main_command, "main respondent")
            if validity_check:
                return main_command
            else:
                print(colored("Invalid command. Please enter a command from "
                              "the list provided.\n", "yellow"))


def process_update_command():
    """
    Requests user to indicate how they wish to amend the data:
    - 'one' updates a single cell
    - 'all' updates a full survey response
    Keeps prompting user until a valid command is entered.
    """
    while True:
        print("Please enter a command to perform on the survey:\n")
        print("- 'one' to update the response to a single question")
        print("- 'all' to update the full list of survey responses")
        update_command = input("Enter your command here:\n")
        main_menu_check(update_command)
        validity_check = validate_command(update_command, "update")
        if validity_check:
            return update_command
        else:
            print(colored("Invalid command. Please enter a command from the "
                          "list provided.\n", "yellow"))


def validate_command(command, menu):
    """
    Validates input entered by user in various menus to ensure this matches a
    valid command available to their permission level. Returns True if the
    command is validated, False if not.
    """
    print(colored("Validating command...", "yellow"))
    main_admin_command_list = ['add', 'update', 'delete', 'list', 'read',
                               'add q', 'read q', 'delete q', 'analyse',
                               'exit', 'home']
    main_respondent_command_list = ['add', 'update', 'exit', 'home']
    update_command_list = ['one', 'all', 'home']
    user_type_list = ['admin', 'respondent', 'exit', 'home']
    match menu:
        case 'main admin':
            if command in main_admin_command_list:
                print(colored("Validated.\n", "yellow"))
                return True
            else:
                return False
        case 'main respondent':
            if command in main_respondent_command_list:
                print(colored("Validated.\n", "yellow"))
                return True
            else:
                return False
        case 'user type':
            if command in user_type_list:
                print(colored("Validated.\n", "yellow"))
                return True
            else:
                return False
        case 'update':
            if command in update_command_list:
                print(colored("Validated.\n", "yellow"))
                return True
            else:
                return False


def main_menu_check(user_input):
    """
    If the user has entered "home" into any input field, return to the
    main menu.
    """
    if user_input == "home":
        print(colored("Returning to main menu...\n", "yellow"))
        main()


def get_respondent_name(main_command, user_type):
    """
    Requests user to input the respondent name. The input string depends on
    the user type and command passed from previous menus.
    """
    admin_string = "Please enter the exact name of the respondent you wish to "
    respondent_string = "Please enter your full name to "
    if user_type == "admin":
        match main_command:
            case 'add':
                respondent_name = input(f"{admin_string}add data for:\n")
                return respondent_name
            case 'update':
                respondent_name = input(f"{admin_string}update data for:\n")
                return respondent_name
            case 'delete':
                respondent_name = input(f"{admin_string}delete data for:\n")
                return respondent_name
            case 'read':
                respondent_name = input(f"{admin_string}read data for:\n")
                return respondent_name
    elif user_type == "respondent":
        match main_command:
            case 'add':
                respondent_name = input(f"{respondent_string}add your data:\n")
                return respondent_name
            case 'update':
                respondent_name = input(f"{respondent_string}update your "
                                        "data:\n")
                return respondent_name


def list_respondents():
    """
    Reads the first column of data from the spreadsheet. Removes heading
    ("Name"). Prints the list of names with a corresponding counter.
    """
    respondent_column = SHEET.worksheet("survey_results").col_values(1)
    respondent_names = respondent_column[1:]
    print(get_border())
    print(colored("RESPONDENT LIST\n", 'green', attrs=['bold']))
    respondent_number = 1
    for respondent in respondent_names:
        print(f"{respondent_number}. {respondent}")
        respondent_number += 1
    print(get_border())


def add_respondent_data():
    """
    Gets survey input from the user. Checks the user inputs an integer between
    1 and 5, continues prompting until valid valid input is received.
    Individual responses are added to a list variable which is passed back to
    the main function.
    """
    print(colored("Adding survey data...\n", "yellow"))
    print("Please enter a value between 1 to 5 for the following questions, "
          "\n")
    print("5 - Excellent")
    print("4 - Good")
    print("3 - Moderate")
    print("2 - Poor")
    print("1 - Very Poor\n")
    responses = []
    questions = get_questions("full")
    for question in questions:
        while True:
            try:
                response = input(f"{question}:\n")
                main_menu_check(response)
                if int(response) in range(1, 6):
                    responses.append(response)
                    break
                else:
                    print(colored("Not a number between 1 and 5. Please "
                                  "enter a valid value.", "yellow"))
            except ValueError:
                print(colored("Not a number between 1 and 5. Please enter "
                              "a valid value.", "yellow"))
    return responses


def update_survey_sheet(new_data):
    """
    Updates the survey spreadsheet with the list of new responses.
    """
    print(colored("Updating survey results spreadsheet...\n", "yellow"))
    SURVEY.append_row(new_data)
    print(colored("Update complete!\n", "yellow"))


def validate_name(name):
    """
    Takes the name input by user and checks whether it matches any of the names
    in the spreadsheet. If no match is found, user will be prompted until a
    match is detected, then the valid name is passedback to the main function.
    """
    print(colored("Validating name...\n", "yellow"))
    existing_names = SURVEY.col_values(1)
    while name not in existing_names:
        name = input("The name you entered does not exist. Please submit the "
                     "name of a respondent who has completed the survey.\n")
        main_menu_check(name)
    print(colored("Name validated.\n", "yellow"))
    return name


def validate_question():
    """
    Requests question number input by user following and checks it is valid
    - must be a number between 1 and the number of the last column in the
    spreadsheet.
    """
    print(colored("Validating question...\n", "yellow"))
    full_questions = get_questions("full")
    print(colored("List of existing Qs:", 'green', attrs=['bold']))
    for question in full_questions:
        print(question)
    print("")
    while True:
        try:
            question_number = input("Which question would you like to read "
                                    "the values for?:\n")
            main_menu_check(question_number)
            if int(question_number) in range(1, SURVEY.col_count):
                break
            else:
                print(colored(f"Not a valid question number. Please enter a "
                              f"value between 1 and {SURVEY.col_count - 1}.",
                              "yellow"))
        except ValueError:
            print(colored(f"Not a valid question number. Please enter a value "
                  f"between 1 and {SURVEY.col_count - 1}.", "yellow"))
    return int(question_number)


def check_existing_names(name):
    """
    Takes the name input by user and checks whether it matches any of the
    names in the spreadsheet. If the name matches, user will be prompted until
    a new name is submitted, then the valid name is passed back to the main
    function.
    """
    main_menu_check(name)
    print(colored("Checking existing names...\n", "yellow"))
    existing_names = SURVEY.col_values(1)
    existing_names.pop(0)  # removes "Name" column header from list
    while name in existing_names:
        print(colored("The name you entered already exists - you have already "
              "completed the survey!\n", "yellow"))
        name = input("Please enter the name of a new respondent.\n")
    print(colored("New respondent confirmed.\n", "yellow"))
    return name


def read_respondent_data(name):
    """
    Reads a row of data from the spreadsheet, based on the respondent name,
    returned as a list of scores.
    """
    print(colored(f"Reading {name}'s data...\n", "yellow"))
    name_cell = SURVEY.find(name)
    respondent_scores = SURVEY.row_values(name_cell.row)
    return respondent_scores


def read_question_data(question_number):
    """
    Outputs a list of respondent names and their scores for a given question.
    """
    existing_names = SURVEY.col_values(1)
    existing_names.pop(0)  # removes "Name" column header from list
    responses = SURVEY.col_values(question_number + 1)
    # The first item in responses will be the column heading i.e. summarised Q
    summarised_question = responses.pop(0)
    # gets length of the longest name in the list to help with spacing output
    longest_name = len(max(existing_names, key=len))
    print(get_border())
    print(colored(f"LISTING RESULTS FOR {summarised_question}:\n", 'green',
                  attrs=['bold']))
    name_index = 0
    print(colored("Name", "green").ljust(longest_name+12)+colored("Score",
                                                                  "green"))
    for response in responses:
        #  prints name & score for each respondent, spaced with .ljust method
        print(f"{existing_names[name_index].ljust(longest_name+5)}{response}")
        name_index += 1
    survey_data = SURVEY.get_all_values()
    survey_averages = get_averages(survey_data, "False")
    float_averages = [float(avg) for avg in survey_averages]
    float_responses = [float(response) for response in responses]
    organisation_average = round(statistics.mean(float_averages), 1)
    question_average = round(statistics.mean(float_responses), 1)
    print(get_border())
    if question_average > organisation_average + 0.4:
        print(f"The average score for this question was {question_average}, "
              f"which is higher than the average score across all questions "
              f"({organisation_average}).")
    elif question_average < organisation_average - 0.4:
        print(f"The average score for this question was {question_average}, "
              f"which is lower than the average score across all questions "
              f"({organisation_average}).")
    else:
        print(f"The average score for this question was {question_average}, "
              f"which is close to the average score across all questions "
              f"({organisation_average}).")
    print(get_border())
    print(colored("Analysis complete. Returning to main menu...\n", "yellow"))


def analyse_respondent_data(respondent_data):
    """
    Conducts analysis on data passed through the main function following
    a "read" command, displaying the question responses and statistics
    for the given individual.
    """
    print(colored("Analysing data...\n", "yellow"))
    # removes the name from the row, leaving just the scores
    respondent_name = respondent_data.pop(0)
    print(colored(f"Results for {respondent_name} are as follows:\n",
                  "yellow"))
    summarised_questions = get_questions("summarised")
    # converts scores to integers so that numerical analysis can be performed
    converted_scores = [int(x) for x in respondent_data]
    # calculates the mean score from the list rounded to 1 decimal
    average_score = round(statistics.mean(converted_scores), 1)
    # calculates the variance from the list rounded to 1 decimal place
    score_variance = round(statistics.variance(converted_scores), 1)
    survey_data = SURVEY.get_all_values()
    survey_averages = get_averages(survey_data, "False")
    float_averages = [float(x) for x in survey_averages]
    organisation_average = round(statistics.mean(float_averages), 1)
    if score_variance > 2:
        variance_string = "high level of variance, indicating significant \n" \
            "disparity between the 'best' and 'worst' aspects of the job."
    elif score_variance > 1.3:
        variance_string = "moderate level of variance."
    else:
        variance_string = "low level of variance, suggesting the \n" \
            "respondent is very consistent in their perception about the " \
            "qualities of the job."
    print(get_border())
    print(colored('OVERALL RESULTS', 'green', attrs=['bold']))
    print(f"{respondent_name} gave an average score of "
          f"{average_score} across all questions.")
    if average_score > organisation_average + 0.4:
        print(f"This is significantly higher than the overall organisation "
              f"average score of {organisation_average}.")
    elif average_score < organisation_average - 0.4:
        print(f"This is significantly lower than the overall organisation "
              f"average score of {organisation_average}.")
    else:
        print(f"This is close to the organisation average score of "
              f"{organisation_average}.")
    print(f"{respondent_name} had a variance of {round(score_variance, 1)} in "
          f"their scores. This is a {variance_string}")
    print(get_border())
    print(colored("QUESTION".ljust(32) + "SCORE".ljust(8) + "COMPARISON WITH "
                  "ORGANISATION", 'green', attrs=['bold']))
    question_index = 0
    for score in respondent_data:
        if float(score) < (float(survey_averages[question_index]) - 0.4):
            print(f"{summarised_questions[question_index].ljust(32)}  {score} "
                  f"    Lower than organisation average "
                  f"({survey_averages[question_index]})")
        elif float(score) > (float(survey_averages[question_index]) + 0.4):
            print(f"{summarised_questions[question_index].ljust(32)}  {score} "
                  f"    Higher than organisation average "
                  f"({survey_averages[question_index]})")
        else:
            print(f"{summarised_questions[question_index].ljust(32)}  {score} "
                  f"    Close to the organisation average "
                  f"({survey_averages[question_index]})")
        question_index += 1
    print(get_border())
    min_score = min(converted_scores)
    max_score = max(converted_scores)
    lowest_scored_questions = []
    highest_scored_questions = []
    count_index = 0
    while count_index < SURVEY.col_count - 1:
        if converted_scores[count_index] == min_score:
            lowest_scored_questions.append(
                summarised_questions[count_index])
        elif converted_scores[count_index] == max_score:
            highest_scored_questions.append(
                summarised_questions[count_index])
        count_index += 1
    print(colored('HIGHLIGHTS', 'green', attrs=['bold']))
    print(f"Highest scored question(s) scored {max_score} as follows: ")
    [print(question) for question in highest_scored_questions]
    print("")
    print(f"Lowest scored question(s) scored {min_score} as follows: ")
    [print(question) for question in lowest_scored_questions]
    print(get_border())
    print(colored("Analysis complete. Returning to main menu...\n", "yellow"))


def update_data(name_to_update, update_command):
    """
    Takes as parameters the name of the individual whose record is to be
    updated and whether user wishes to update one field, or their entire
    response set. Displays the current response set and requests
    confirmation that the user wishes to proceed. Updates the relevant cell
    or row of cells before returning to the main menu.
    """
    print(colored("Updating data...\n", "yellow"))
    name_cell = SURVEY.find(name_to_update)
    row_to_update = name_cell.row
    while True:
        try:
            confirm = input(f"{name_to_update}'s responses are currently "
                            f"{read_respondent_data(name_to_update)[1:]}.\n"
                            "Are you sure you wish to amend this data? "
                            "(Y/N):\n")
            main_menu_check(confirm)
            if confirm in ["Y", "y"]:
                break
            elif confirm in ["N", "n"]:
                print(colored("Update aborted. Returning to main menu.\n",
                              "yellow"))
                main()
            else:
                print(colored("Please respond with 'Y' to proceed or 'N' to "
                              "cancel."))
        except ValueError:
            print(colored("Please respond with 'Y' to proceed or 'N' to "
                          "cancel.", "yellow"))
    if update_command == 'all':
        update_data_list = add_respondent_data()
        print(colored(f"Value responses {update_data_list} will now be updated"
                      f" for {name_to_update}...", "yellow"))
        # The values start from the 2nd column onwards and .update_cell method
        # is 1-indexed, so the loop index must start at 2 to insert correctly
        column_index = 2
        for update_value in update_data_list:
            SURVEY.update_cell(row_to_update, column_index, update_value)
            column_index += 1
        print(colored("Update complete. Returning to main menu...\n",
                      "yellow"))
    elif update_command == 'one':
        while True:
            try:
                question_number = input("Which question would you like to "
                                        "update the value for?:\n")
                main_menu_check(question_number)
                if int(question_number) in range(1, SURVEY.col_count):
                    break
                else:
                    print(colored(f"Not a valid question number. Please enter "
                                  f"a value between 1 and "
                                  f"{SURVEY.col_count - 1}.", "yellow"))
            except ValueError:
                print(colored(f"Not a valid question number. Please enter a "
                              f"value between 1 and {SURVEY.col_count - 1}.",
                              "yellow"))
        while True:
            try:
                update_value = input("Please enter the value you wish to "
                                     "add:\n")
                main_menu_check(update_value)
                int_question_number = int(question_number)
                if int(update_value) in range(1, 6):
                    print(colored(f"A score of {update_value} will now be "
                                  f"updated to Q{question_number} for "
                                  f"{name_to_update}...", "yellow"))
                    SURVEY.update_cell(row_to_update, int_question_number + 1,
                                       int(update_value))
                    print(colored("Update complete. Returning to main menu... "
                                  "\n", "yellow"))
                    return
                else:
                    print(colored("Not a number between 1 and 5. Please enter "
                                  "a valid value.", "yellow"))
            except ValueError:
                print(colored("Not a number between 1 and 5. Please enter a "
                              "valid value.", "yellow"))


def add_question():
    """
    Adds a new question to the survey and spreadsheet, with a summarised
    heading and the full text question held within the cell's note.
    """
    print(colored("Adding new question to survey...\n", "yellow"))
    print("Please note that the responses for all previous respondents who "
          "have not answered the new question will be set to the median value "
          "(3).")
    print("You can update the default values by using the " +
          colored("'update'", "blue") + " function from the main menu.\n")
    new_question = input("Please enter the full text question you wish to add."
                         "\nPlease note that the question should be formatted "
                         "such that it can be answered with a value between 1 "
                         "to 5, with 1 = 'Very Poor' and 5 = 'Excellent':\n")
    main_menu_check(new_question)
    new_summarised_question = input("Please enter the a summarised version "
                                    "(1 to 2 words):\n")
    main_menu_check(new_summarised_question)
    SURVEY.add_cols(1)  # adds a new empty column to the spreadsheet
    next_question_column = SURVEY.col_count
    SURVEY.insert_note(1, next_question_column, 1, next_question_column,
                       f"Q{next_question_column - 1} - {new_question}")
    SURVEY.update_cell(1, next_question_column, f"Q{next_question_column - 1}"
                       f" - {new_summarised_question}")
    print(colored("Adding question heading...\n", "yellow"))
    number_of_rows = len(SURVEY.col_values(1))
    cell_index = 2
    print(colored("Adding default value to past respondents...\n", "yellow"))
    while cell_index <= number_of_rows:
        SURVEY.update_cell(cell_index, next_question_column, 3)
        cell_index += 1
    print(colored("The question has successfully been added to the survey.\n",
                  "yellow"))


def delete_respondent(name):
    """
    Takes the validated name input by the user and deletes the corresponding
    row in the spreadsheet.
    """
    name_cell = SURVEY.find(name)
    while True:
        try:
            confirm = input(f"{name}'s responses are currently "
                            f"{read_respondent_data(name)[1:]}.\n"
                            "Are you sure you wish to delete this data? "
                            "(Y/N):\n")
            main_menu_check(confirm)
            if confirm in ["Y", "y"]:
                break
            elif confirm in ["N", "n"]:
                print(colored("Delete aborted. Returning to main menu.\n",
                              "yellow"))
                main()
            else:
                print(colored("Please respond with 'Y' to proceed or 'N' to "
                              "cancel."))
        except ValueError:
            print(colored("Please respond with 'Y' to proceed or 'N' to "
                          "cancel.", "yellow"))
    print(colored(f"Deleting {name}'s data...\n", "yellow"))
    SURVEY.delete_rows(name_cell.row)
    print(colored(f"Deletion complete. {name}'s entry has been removed from "
                  f"the survey.\n", "yellow"))


def delete_question():
    """
    Provides a list of existing question then prompts user to give the number
    of the question they wish to delete from the survey. The column is then
    deleted and the number of the deleted question is returned to the main
    function.
    """
    # list all current Qs
    full_questions = get_questions("full")
    print(colored("List of existing Qs:", 'green', attrs=['bold']))
    for q in full_questions:
        print(q)
    print("")
    while True:
        try:
            question_number = input("Which question would you like to "
                                    "delete?:\n")
            main_menu_check(question_number)
            if int(question_number) in range(1, SURVEY.col_count):
                print(colored(f"Deleting question {question_number} from "
                              f"survey...\n", "yellow"))
                SURVEY.delete_columns(int(question_number) + 1)
                print(colored("Deletion complete.\n", "yellow"))
                return int(question_number)
            else:
                print(colored(f"Not a valid question number. Please enter a "
                              f"value between 1 and {SURVEY.col_count - 1}.",
                              "yellow"))
        except ValueError:
            print(colored(f"Not a valid question number. Please enter a value "
                          f"between 1 and {SURVEY.col_count - 1}.", "yellow"))


def update_question_cells(number_of_deleted_question):
    """
    Following the deletion of a question, if the question was not the last one
    in the survey, this function updates the numbers in the summarised and full
    versions of questions to the right of the deleted question to keep in
    numerical ascending order.
    """
    print(colored("Updating question headings...\n", "yellow"))
    full_questions = get_questions("full")
    position_index = number_of_deleted_question
    print(f"NUMBER OF DELETED QUESTION: {number_of_deleted_question}")
    column_to_update = number_of_deleted_question + 1
    question_index = 0
    while position_index < SURVEY.col_count:
        # Rebuilds the question and heading strings based on deleted Q
        old_summary_string = SURVEY.cell(1, position_index + 1).value
        old_question_string = full_questions[position_index - 1]
        split_summary_string = old_summary_string.split(" ")
        split_question_string = old_question_string.split(" ")
        new_question_number = int(split_summary_string[0][1:]) - 1
        split_summary_string[0] = f"Q{new_question_number}"
        split_question_string[0] = f"Q{new_question_number}"
        new_summarised_question = ' '.join(split_summary_string)
        new_full_question = ' '.join(split_question_string)
        SURVEY.update_cell(1, position_index + 1, new_summarised_question)
        SURVEY.insert_note(1, column_to_update, 1, column_to_update,
                           new_full_question)
        position_index += 1
        question_index += 1
    print(colored("Updating complete.\n", "yellow"))


def get_questions(question_type):
    """
    Returns a list of the survey questions. The get_notes function returns
    a list of lists containing cell notes which needs to be unpacked before
    returning.
    """
    if question_type == "full":
        full_questions = SURVEY.get_notes()
        return full_questions[0][1:]
    elif question_type == "summarised":
        survey_data = SURVEY.get_all_values()
        # Extracts the first row of data (i.e. name and all questions)
        headings = survey_data.pop(0)
        # Removes the name from list, leaving only the summarised questions
        headings.pop(0)
        summarised_questions = headings
        return summarised_questions


def get_border():
    """
    Returns a string of hyphens to use as border when outputting results in
    different sections.
    """
    table_border = "—"*80
    return table_border


def analyse_survey():
    """
    Conducts analysis of the overall survey data set, returning average
    response values for each question.
    """
    print(colored("Analysing survey data...\n", "yellow"))
    survey_data = SURVEY.get_all_values()
    print(get_border())
    question_averages = get_averages(survey_data, True)
    summarised_questions = get_questions("summarised")
    print(get_border())
    print(colored('AVERAGE SCORES\n', 'green', attrs=['bold']))
    q_index = 0
    # prints all summarised Qs and average organisational score
    longest_q = len(max(summarised_questions, key=len))
    for average_score in question_averages:
        print(f"{summarised_questions[q_index].ljust(longest_q + 5)} "
              f"{average_score}")
        q_index += 1
    print(get_border())
    return question_averages


def get_averages(survey_data, full_analysis):
    """
    Extracts values (excludes questions & names) from survey data. Calculates
    and returns an overall average score for each question. Outputs
    organisation average score if full analysis is being conducted.
    """
    response_values = []
    for data_row in survey_data:
        data_row.pop(0)
        for value in data_row:
            if len(value) == 1:
                response_values.append(int(value))
            else:
                continue
    overall_average = statistics.mean(response_values)
    if full_analysis is True:
        print(colored('OVERALL SCORE', 'green', attrs=['bold']))
        print(f"Overall average score across organisation: "
              f"{round(overall_average, 1)}")
    question_totals = []
    number_of_responses = len(survey_data) - 1
    for index in range(SURVEY.col_count - 1):
        question_totals.append(0)
    survey_data.pop(0)
    for dataset in survey_data:
        for index in range(len(dataset)):
            question_totals[index] += int(dataset[index])
    question_averages = [x/number_of_responses for x in question_totals]
    question_averages_rounded = ['%.1f' % x for x in question_averages]
    return question_averages_rounded


def get_data_insights(analysed_data):
    """
    Extracts and displays low and high scoring questions based on average
    responses. Makes recommendations on what the organisation needs to work
    on based on lower scoring metrics.
    """
    print(colored('HIGHLIGHTS', 'green', attrs=['bold']))
    float_data = [float(x) for x in analysed_data]
    low_scores = []
    high_scores = []
    question_index = 0
    summarised_questions = get_questions("summarised")
    for score in float_data:
        if score <= 2.5:  # If the average score is below 2.5 it is "Low".
            low_scores.append(summarised_questions[question_index])
        elif score >= 3.5:  # If the average score is above 3.5 it is "High".
            high_scores.append(summarised_questions[question_index])
        question_index += 1
    print("Low scoring questions:")
    [print(question) for question in low_scores]
    print("")
    print("High scoring questions:")
    [print(question) for question in high_scores]
    print("")
    low_scores_headings = []
    for question in low_scores:
        # removes text before words from questions (e.g. "Q1 - ") before append
        low_scores_headings.append(question[5:])
    print("Based on the average scores, areas of concern for the organisation "
          "should be: ")
    for heading in low_scores_headings:
        print(f"{heading}")
    print(get_border())
    print(colored("Analysis complete. Returning to main menu...\n", "yellow"))


def main():
    """
    Runs all program functions. Gets the user permissions. Uses a case
    statement to decide which functions to call.
    """
    user_type = get_user_type()
    if user_type == "admin":
        validate_password()
    while True:  # loops until user enters 'exit' command
        main_command = process_main_command(user_type)
        main_menu_check(main_command)
        match main_command:
            case 'add':
                respondent_name = get_respondent_name('add', user_type)
                main_menu_check(respondent_name)
                respondent_name_checked = check_existing_names(respondent_name)
                responses = add_respondent_data()
                responses.insert(0, respondent_name_checked)
                update_survey_sheet(responses)
            case 'update':
                respondent_name = get_respondent_name('update', user_type)
                main_menu_check(respondent_name)
                validated_name_to_update = validate_name(respondent_name)
                update_command = process_update_command()
                update_data(validated_name_to_update, update_command)
            case 'delete':
                respondent_name = get_respondent_name('delete', user_type)
                main_menu_check(respondent_name)
                validated_name_to_delete = validate_name(respondent_name)
                delete_respondent(validated_name_to_delete)
            case 'list':
                list_respondents()
            case 'read':
                respondent_name = get_respondent_name('read', user_type)
                main_menu_check(respondent_name)
                validated_read_name = validate_name(respondent_name)
                respondent_data = read_respondent_data(validated_read_name)
                analyse_respondent_data(respondent_data)
            case 'add q':
                add_question()
            case 'read q':
                question_number = validate_question()
                read_question_data(question_number)
            case 'delete q':
                number_of_deleted_question = delete_question()
                # Skips if the last question was deleted, no need to update
                if number_of_deleted_question < SURVEY.col_count:
                    update_question_cells(number_of_deleted_question)
            case 'analyse':
                analysed_data = analyse_survey()
                get_data_insights(analysed_data)
            case 'exit':
                print(colored("The application will now close.", "yellow"))
                quit()


print("")
print(colored('Welcome to DT Survey Analytics.\n', 'green', attrs=['bold']))
main()
