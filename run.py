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


def process_main_command():
    """
    Requests user to indicate what function they want to perform via command:
    - 'add' adds new survey data to existing spreadsheet
    - 'update' updates values for a given individual
    - 'delete' removes a given individual's set of responses from the spreadsheet
    - 'list' returns a list of names of individual respondents
    - 'read' returns a given individual's responses
    - 'add q' adds a new question to the survey
    - 'delete q' deletes an exiting question within the survey
    - 'analyse' returns general analysis over all survey data
    - 'exit' exits the program
    """
    while True:
        print("Please enter a command to perform on the survey\n")
        print("- 'add' to add new survey data to existing spreadsheet")
        print("- 'update' to update existing survey data within the spreadsheet")
        print("- 'delete' to delete a record based on an inputted name")
        print("- 'list' to see a list of names of individual respondents")
        print("- 'read' to read a specific individual's responses")
        print("- 'add q' to add a new question to the survey")
        print("- 'delete q' to delete a question from the survey and all associated data")
        print("- 'analyse' to conduct general analysis over all survey data")
        print("- 'exit' to exit the application\n")
        main_command = input("Enter your command here: \n")
        validity_check = validate_command(main_command, "main")
        if validity_check:
            return main_command
        else:
            print("Invalid command. Please enter a command from the list provided.\n")


def process_update_command():
    """
    Requests user to indicate how they wish to amend the data:
    - 'one' updates a single cell
    - 'all' updates a full survey response
    """
    while True:
        print("Please enter a command to perform on the survey\n")
        print("- 'one' to update the response to a single question")
        print("- 'all' to update the full list of survey responses")
        update_command = input("Enter your command here: \n")
        validity_check = validate_command(update_command, "update")
        if validity_check:
            return update_command
        else:
            print("Invalid command. Please enter a command from the list provided.\n")


def list_respondents():
    """
    Returns a list of the names of all survey respondents
    """
    respondent_column = SHEET.worksheet("survey_results").col_values(1)
    respondent_names = respondent_column[1:] 
    print("**See below for a list of all respondents.**\n")
    for respondent in respondent_names:
        print(respondent)
    print("\n")


def get_respondent_data():
    """
    Gets survey input from the user. Checks the user inputs an integer between 1 and 5,continues prompting 
    until valid valid input is received. Individual responses are added to a list variable which is passed 
    back to the main() function.
    """
    print("Adding survey data...\n")
    print("Please enter a value between 1 to 5 for the following questions, where appropriate.\n")
    print("5 - Excellent")
    print("4 - Good")
    print("3 - Moderate")
    print("2 - Poor")
    print("1 - Very Poor\n")
    responses = []
    questions = get_questions("full")
    print(f"Questions inside get_respondent_data after return: {questions}")
    while True:
        for question in questions:
            print(question + ": \n")
            while True:
                try:
                    response = int(input("Answer: "))
                    if response in range(1,6):
                        # print(f"You entered {response}.\n")
                        responses.append(response)
                        break
                    else:
                        print("Not a number between 1 and 5. Please enter a valid value.")
                except ValueError:
                    print("Not a number between 1 and 5. Please enter a valid value.")
        return responses


def update_survey_sheet(new_data):
    """
    Updates the survey spreadsheet with the list of new responses.
    """
    print(f"Updating survey results spreadsheet...\n")
    #if type == "respondent":
    SURVEY.append_row(new_data)
    #elif type == "question":
    #SURVEY.add_cols(new_data)
    print(f"Update complete!\n")


def read_respondent_data(name):
    """
    Reads a row of data from the spreadsheet based on the respondent name, which is passed by user.
    """
    print(f"Reading {name}'s data...\n")
    name_cell = SURVEY.find(name)
    respondent_scores = SURVEY.row_values(name_cell.row)
    return respondent_scores


def update_data(name_to_update, update_command):
    """
    Takes as parameters the name of the individual whose record is to be updated and whether user wishes
    to update one field, or their entire response set. Displays the current response set and requests 
    confirmation that the user wishes to proceed. Updates the relevant cell or row of cells before returning
    to the main menu.
    """
    print(f"Updating data...\n")
    print(f"UPDATE_DATA: Name {name_to_update}\n")
    print(f"UPDATE_DATA: Command {update_command}\n")

    name_cell = SURVEY.find(name_to_update)
    row_to_update = name_cell.row
    while True:
        try:
            confirm = input(f"{name_to_update}'s responses are currently {read_respondent_data(name_to_update)[1:]}. Are you sure you wish to amend this data? (Y/N): ")
            if confirm in ["Y", "y"]:
                break
            elif confirm in ["N", "n"]:
                print("Update aborted. Returning to main menu.\n")
                return
            else:
                print("Please respond with 'Y' to proceed or 'N' to cancel.")
        except ValueError:
            print("Please respond with 'Y' to proceed or 'N' to cancel.")
    #print(f"Row to update, based on being passed {name_to_update}: {row_to_update}")

    if update_command == 'all':
        update_data_list = get_respondent_data()
        print(f"Value responses {update_data_list} will now be updated for {name_to_update}...")
        column_index = 2  # The values start from the 2nd column onwards
        for update_value in update_data_list:
            SURVEY.update_cell(row_to_update, column_index, update_value)
            column_index += 1
        print("Update complete. Returning to main menu...\n")
    elif update_command == 'one':
        while True:
            try:
                question_number = int(input("Which question would you like to update the value for?:"))
                if question_number in range(1, SURVEY.col_count):
                    break
                else:
                    print(f"Not a valid question number. Please enter a value between 1 and {SURVEY.col_count - 1}.")
            except ValueError:
                print(f"Not a valid question number. Please enter a value between 1 and {SURVEY.col_count - 1}.")
        while True:
            try:
                update_value = int(input("Please enter the value: "))
                if update_value in range(1, 6):
                    print(f"A score of {update_value} will now be updated to Q{question_number} for {name_to_update}...")
                    #print(f"Row to update: {row_to_update}")
                    #print(f"Col to update: {question_number + 1}")
                    SURVEY.update_cell(row_to_update, question_number + 1, update_value)
                    print("Update complete. Returning to main menu...\n")
                    return
                else:
                    print("Not a number between 1 and 5. Please enter a valid value.")
            except ValueError:
                print("Not a number between 1 and 5. Please enter a valid value.")


def add_question():
    """
    Adds a new question to the survey and spreadsheet, with a summarised heading
    and the full text question held within the note. 
    """
    print("Adding new question to survey...\n")
    print("Please note that the responses for all previous respondents who have not answered the new question will be set to the median value (3).")
    print("You can update the default values by using the 'update' function from the main menu.\n")
    new_question = input("Please enter the full text question you wish to add: \n")
    new_summarised_question = input("Please enter the a summarised version (1 to 2 words): \n")
    SURVEY.add_cols(1)
    #summarised_questions = get_questions("summarised")
    next_question_column = SURVEY.col_count
    print(next_question_column)
    # Can't find a gspread method which returns the letter value of the column so need to zip this to a list - not ideal, need to find fix!
    potential_coordinates = []
    column_ids = ["B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","AA","AB","AC","AD","AE","AF","AG","AH","AI","AJ","AK","AL","AM","AN","AO","AP","AQ","AR","AS","AT","AU","AV","AW","AX","AY","AZ"] 
    index = 0
    for letter in column_ids:
        potential_coordinates.append(letter + "1")
        #print(f"Coordinate being added: {letter + "1"}")
        index += 1
    print(f"Potential coordinates (should be a list of A1, B1, C1, etc.): {potential_coordinates}")
    cell_coordinate = f"{potential_coordinates[next_question_column - 2]}"
    #print(f"New question: {new_question}")
    #print(f"New heading: {new_summarised_question}")
    print(f"Column to insert to: {cell_coordinate[0]}")
    print(f"Cell coordinate being passed: {cell_coordinate}")
    SURVEY.insert_note(cell_coordinate, f"Q{next_question_column - 1} - {new_question}")
    print(f"column length to put in cell add {next_question_column}")
    SURVEY.update_cell(1, next_question_column, f"Q{next_question_column - 1} - {new_summarised_question}")
    print("The question has successfully been added to the survey.\n")
    col_values = SURVEY.col_values(1)
    number_of_rows = len(col_values)
    print(number_of_rows)
    cell_index = 2
    while cell_index <= number_of_rows:
        SURVEY.update_cell(cell_index, next_question_column, 3)
        print(f"put 3 in {cell_index} {next_question_column}")
        cell_index += 1

def delete_row(name):
    """
    Takes the validated name input by the user and deletes the corresponding row in the spreadsheet.
    """
    print(f"Deleting {name}'s data...\n")
    name_cell = SURVEY.find(name)
    SURVEY.delete_rows(name_cell.row)
    print(f"Deletion complete. {name}'s entry has been removed from the survey.\n")


def delete_question():
    #list all current Qs
    full_questions = get_questions("full")
    print("List of existing Qs:")
    for q in full_questions:
        print(q)
    print("\n")
    #print(q for q in full_questions)
    while True:
        try:
            question_number = int(input("Which question would you like to delete?: "))
            if question_number in range(1, SURVEY.col_count):
                print(f"Deleting question {question_number} from survey...\n")
                SURVEY.delete_columns(question_number + 1)
                print("Deletion complete. Returning to main menu...\n")
                break
            else:
                print(f"Not a valid question number. Please enter a value between 1 and {SURVEY.col_count - 1}.")
        except ValueError:
            print(f"Not a valid question number. Please enter a value between 1 and {SURVEY.col_count - 1}.")

#  REFACTOR? validate_name & check_existing_names perform similar, but inverse functions. 
def validate_name(name):
    """
    Takes the name input by user following "read" command and checks whether it matches any of the names 
    in the spreadsheet. If no match is found, user will be prompted until a match is detected, then the 
    valid name is passed back to the main() function.
    """
    print("Validating name...")
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
    print("Checking existing names...\n")
    existing_names = SURVEY.col_values(1)
    while name in existing_names:
        print("The name you entered already exists - you have already completed the survey!\n")
        name = input("Please enter the name of a new respondent.\n")
    return name


def validate_command(command, menu):
    """
    Checks that the initial command passed by user to perform on data set is valid.
    """
    print("Validating command...")
    main_command_list = ['add', 'update', 'delete', 'list', 'read', 'add q', 'delete q', 'analyse', 'exit']
    update_command_list = ['one', 'all']
    if menu == "main":
        if command in main_command_list:
            print("Validated.\n")
            return True
        else:
            return False
    elif menu == "update":
        if command in update_command_list:
            print("Validated.\n")
            return True
        else:
            return False


# better to just read this in as a global variable? 
def get_questions(question_type):
    """
    Returns a list of the survey questions. The get_notes function returns 
    a list of lists containing cell notes which needs to be unpacked before
    returning.
    """
    print(f"Reading questions from survey spreadsheet...\n")
    if question_type == "full":
        full_questions = SURVEY.get_notes()
        #print(f"Questions returns from inside get_questions: {full_questions[0][1:]}")
        return full_questions[0][1:]
    elif question_type == "summarised":
        survey_data = SURVEY.get_all_values()
        headings = survey_data.pop(0)  # Extracts the first row of data (i.e. name and all questions)
        headings.pop(0)  # Removes the name from list, leaving only the summarised questions
        summarised_questions = headings
        #print(f"get_questions function returning: {summarised_questions}")
        return summarised_questions
    


def analyse_respondent_data(respondent_data):
    """
    Conducts analysis on data passed through the main function following
    a "read" command, displaying the question responses and statistics
    for the given individual. 
    """
    # notes = SURVEY.row_values(1)
    #survey_data = SURVEY.get_all_values()
    print(f"Analysing respondent data...\n")
    respondent_name = respondent_data.pop(0)  # removes the first value in the row (i.e. name) so we can convert the remaining numbers in the string to int for analysis
    #print(f"Survey data being fed into averages function: {survey_data}\n")
    # print(f"Qs data being fed into averages function: {summarised_questions}\n")
    #survey_averages = get_averages(survey_data, False)
    #print(f"Printing survey_averages from within analyse_respondent_data function: {survey_averages}")  # test
    print(f"Results for {respondent_name} are as follows:\n")
    question_index = 0
    summarised_questions = get_questions("summarised")
    for score in respondent_data:  # this for loop prints out a list of strings containing a shortened version of the question along with the individual's score
        print(f"{summarised_questions[question_index]} : {score}")
        question_index += 1
    converted_scores = [int(x) for x in respondent_data]  # converts data to a list of integers so that numerical analysis can be performed
    average_score = statistics.mean(converted_scores)  # calculates the mean score from the list
    score_variance = statistics.variance(converted_scores)  # calculates the variance from the list
    if score_variance > 2:
        variance_string = "high level of variance, indicating significant disparity between the 'best' and 'worst' aspects of the job."
    elif score_variance > 1.3:
        variance_string = "moderate level of variance."
    else:
        variance_string = "low level of variance, suggesting the respondent is very consistent in their perception about the qualities of the job." 
    print(f"{respondent_name} gave an average score of {round(average_score, 1)} across all questions.")
    print(f"{respondent_name} had a variance of {round(score_variance, 1)} in their scores. This is a {variance_string}")

    min_score = min(converted_scores)
    #print(f"Min score: {min_score}")  # TESTING
    lowest_scored_questions = []
    i = 0
    print(f"Converted scores for each Q: {converted_scores}")
    while i < SURVEY.col_count - 1:
        print(f"Index within append loop for low scores: {i}")
        if converted_scores[i] == min_score:
            lowest_scored_questions.append(summarised_questions[i])
        i += 1
    print(f"Lowest scored question(s) scored {min_score} as follows: {lowest_scored_questions}.\n")


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
    #names = []  # May not be required, might only need to pop names off if they're not used
    #print(f"Names list: {names}\n")  
    #print(f"Names list without NAME heading: {names[1:]}\n")
    #print(f"Printing summarised questions from inside analyse_survey, should exclude name: {summarised_questions}")
    #print(f"List of responses: {survey_data}\n")
    #print(f"Summarised questions: {summarised_questions}\n")
    #print(f"Response values only, should only be numbers: {response_values}\n")
    print("See below for average scores for each question in the survey:\n")
    question_averages = get_averages(survey_data, True)
    #print(f"Printing question averages from analyse_survey function after call: {question_averages}")
    summarised_questions = get_questions("summarised")
    question_index = 0
    for average_score in question_averages:  # this for loop prints out a list of strings containing a shortened version of the question along with the average organisational score
        print(f"{summarised_questions[question_index]} : {average_score}")
        question_index += 1

    print("Analysis complete. Returning to main menu...\n")
    return question_averages


def get_averages(survey_data, full_analysis):
    """
    Extracts values (excludes questions & names) from survey data. Calculates and returns 
    an overall average score for each question.
    """
    #print("Printing questions and length of q array in getqavgs function")
    response_values = []
    for data_row in survey_data:
        data_row.pop(0)
        for value in data_row:
            if len(value) == 1:
                response_values.append(int(value))
            else:
                continue
    
    #print(f"Response values within get_averages, should be all numbers: {response_values}")
    
    overall_average = statistics.mean(response_values)
    if full_analysis:  # Only outputs the organisational score if the function is being called from analyse_survey, not analyse_respondent_data
        print(f"Overall average score across organisation: {round(overall_average, 1)}\n")
    
    # initialises totals variable depending on the number of responses
    question_totals = []
    number_of_responses = len(survey_data) - 1  # survey data contains all column data including headings, so need to loop through the lenth minus 1
    #print(f"Number of responses, should be 14: {number_of_responses}")
    #summarised_questions = get_questions("summarised")
    for index in range(SURVEY.col_count - 1):
        question_totals.append(0)
    #print(f"Question totals from inside get_averages function: {question_totals}")  # test
    #print(f"Initialised question totals, should all be 0: {question_totals}")

    #Gets totals for each question
    #print(survey_data)
    survey_data.pop(0)
    #print(survey_data)
    for dataset in survey_data:
        #dataset.pop(0)
        for index in range(len(dataset)):
            #print(f"Current value being looked at: {dataset[index]}")  # test
            #print(f"Index: {index}")  # test
            question_totals[index] += int(dataset[index])
    #print(f"List of total scores for each question: {question_totals}\n")  # test
    #print(f"Number of responses which the totals will be divided by: {number_of_responses}")  # test

    # for loop comprehensions to generate a list of averages then round all values to one decimal place
    question_averages = [x/number_of_responses for x in question_totals]
    question_averages_rounded = ['%.1f' % x for x in question_averages]  # alternative method of rounding since round() does not work with lists
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
    summarised_questions = get_questions("summarised")
    for score in float_data:
        if score <= 2.5:  # If the average score is below 2.5 it is deemed "Low". Arbitrary, can be changed.
            low_scores.append(summarised_questions[question_index])
        elif score >= 3.5:  # If the average score is above 3.5 it is deemed "High". Arbitrary, can be changed.
            high_scores.append(summarised_questions[question_index])
        question_index += 1
    print(f"Low scoring questions: {low_scores}")
    print(f"High scoring questions: {high_scores}\n")
    low_scores_headings = []
    for question in low_scores:
        low_scores_headings.append(question[5:])  # removes text before words from questions (e.g. "Q1 - ") 
    print("Based on the average scores, major areas of concern for the organisation should be: ")
    # print([heading for heading in low_scores_headings])
    for heading in low_scores_headings:
        print(f"{heading}")
    print("\n")


def main():
    """
    Run all program functions
    """
    #test = get_questions("summarised")
    #print(test)
    print(f"#rows: {SURVEY.row_count}")
    print(f"#cols: {SURVEY.col_count}")

    #summarised_questions = get_questions("summarised")
    #print(f"#cols based on old variable: {len(summarised_questions)}")

    while True:  # The program will keep requesting user commands until they input the "exit" command
        main_command = process_main_command()
        #print(f"MAIN: user command is {main_command}") #TESTING
        match main_command:
            case 'add':
                respondent_name = input("Please enter the exact name you wish to add data for: ")
                respondent_name_checked = check_existing_names(respondent_name)
                responses = get_respondent_data()
                responses.insert(0, respondent_name_checked)  # adds the respondent's name to the start of the responses list
                update_survey_sheet(responses)
            case 'update':
                name_to_update = input("Enter the exact name of the person whose results you wish to update: ")
                validated_name_to_update = validate_name(name_to_update)
                update_command = process_update_command()
                update_data(validated_name_to_update, update_command)
            case 'delete':
                name_to_delete = input("Enter the exact name of the respondent you wish to delete survey results for: \n")
                validated_name_to_delete = validate_name(name_to_delete)
                delete_row(validated_name_to_delete)
            case 'list':
                list_respondents()
            case 'read':
                read_name = input("Enter the exact name of the respondent you wish to see survey results for: \n")
                validated_read_name = validate_name(read_name)
                respondent_data = read_respondent_data(validated_read_name)
                analyse_respondent_data(respondent_data)
            case 'add q':
                add_question()
            case 'delete q':
                delete_question()
            case 'analyse':
                analysed_data = analyse_survey()
                make_recommendations(analysed_data)
            case 'exit':
                print("The application will now close.")
                quit()


print("Welcome to DT Survey Analytics.\n")
main()