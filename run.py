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


def get_user_type():
    """
    Requests user to indicate what access type they have:
    - 'admin' can use all features and functions
    - 'respondent' can only input and update their own data
    """
    while True:
        print("Please enter your user type:")
        print("- 'admin' can add or update responses on behalf others, "
              "read individual or whole survey data, add and delete "
              "questions.")
        print("- 'respondent' can add and update their own responses.")
        print("Enter 'home' in any field to return to this main menu.\n")
        user_type = input("Enter user type: ")
        validated_user_type = validate_command(user_type, "user type")
        if validated_user_type is True:
            return user_type
        else:
            print("You did not enter a valid user type. Please enter "
                  "'admin' or 'respondent'")


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
    Respondent level users can only access 'add', 'update' and 'exit'
    """
    # print(f"PROCESS_MAIN_COMMAND - user type is: {user_type}")
    if user_type == "admin":
        while True:
            print("Please enter a command to perform on the survey:\n")
            print("- 'add' to add new survey data to existing spreadsheet")
            print("- 'update' to update existing survey data within the "
                  "spreadsheet")
            print("- 'delete' to delete a record based on an inputted name")
            print("- 'list' to see a list of names of individual respondents")
            print("- 'read' to read a specific individual's responses")
            print("- 'add q' to add a new question to the survey")
            print("- 'read q' to read all responses for a given question")
            print("- 'delete q' to delete a question from the survey and all "
                  "associated data")
            print("- 'analyse' to conduct general analysis over all survey "
                  "data")
            print("- 'exit' to exit the application\n")
            main_command = input("Enter your command here: ")
            validity_check = validate_command(main_command, "main admin")
            if validity_check:
                return main_command
            else:
                print("Invalid command. Please enter a command from the list "
                      "provided.\n")
    elif user_type == "respondent":
        while True:
            print("Please enter a command to perform on the survey:\n")
            print("- 'add' to add new survey data to existing spreadsheet")
            print("- 'update' to update existing survey data within the "
                  "spreadsheet")
            print("- 'exit' to exit the application\n")
            main_command = input("Enter your command here: ")
            validity_check = validate_command(main_command, "main respondent")
            if validity_check:
                return main_command
            else:
                print("Invalid command. Please enter a command from the list "
                      "provided.\n")


def process_update_command():
    """
    Requests user to indicate how they wish to amend the data:
    - 'one' updates a single cell
    - 'all' updates a full survey response
    """
    while True:
        print("Please enter a command to perform on the survey:\n")
        print("- 'one' to update the response to a single question")
        print("- 'all' to update the full list of survey responses")
        update_command = input("Enter your command here: ")
        main_menu_check(update_command)
        validity_check = validate_command(update_command, "update")
        if validity_check:
            return update_command
        else:
            print("Invalid command. Please enter a command from the list "
                  "provided.\n")


def validate_command(command, menu):
    """
    Checks that the initial command passed by user to perform on data set is
    valid.
    """
    print("Validating command...")
    main_admin_command_list = ['add', 'update', 'delete', 'list', 'read',
                               'add q', 'read q', 'delete q', 'analyse',
                               'exit', 'home']
    main_respondent_command_list = ['add', 'update', 'exit', 'home']
    update_command_list = ['one', 'all', 'home']
    user_type_list = ['admin', 'respondent', 'home']
    match menu:
        case 'main admin':
            if command in main_admin_command_list:
                print("Validated.\n")
                return True
            else:
                return False
        case 'main respondent':
            if command in main_respondent_command_list:
                print("Validated.\n")
                return True
            else:
                return False
        case 'user type':
            if command in user_type_list:
                print("Validated.\n")
                return True
            else:
                return False
        case 'update':
            if command in update_command_list:
                print("Validated.\n")
                return True
            else:
                return False


def main_menu_check(user_input):
    """
    If the user has entered "home" into any input field, return to the
    main menu.
    """
    if user_input == "home":
        print("Returning to main menu...\n")
        main()


def list_respondents():
    """
    Returns a list of the names of all survey respondents
    """
    respondent_column = SHEET.worksheet("survey_results").col_values(1)
    respondent_names = respondent_column[1:]
    print(get_border())
    print("RESPONDENT LIST\n")
    respondent_number = 1
    for respondent in respondent_names:
        print(f"{respondent_number}. {respondent}")
        respondent_number += 1
    print(get_border())


def get_respondent_data():
    """
    Gets survey input from the user. Checks the user inputs an integer between
    1 and 5,continues prompting until valid valid input is received. Individual
    responses are added to a list variable which is passed back to the main()
    function.
    """
    print("Adding survey data...\n")
    print("Please enter a value between 1 to 5 for the following questions, "
          "where appropriate.\n")
    print("5 - Excellent")
    print("4 - Good")
    print("3 - Moderate")
    print("2 - Poor")
    print("1 - Very Poor\n")
    responses = []
    questions = get_questions("full")
    while True:
        for question in questions:
            print(question + ": \n")
            while True:
                try:
                    response = input("Answer: ")
                    main_menu_check(response)
                    if int(response) in range(1, 6):
                        responses.append(response)
                        break
                    else:
                        print("Not a number between 1 and 5. Please enter a "
                              "valid value.")
                except ValueError:
                    print("Not a number between 1 and 5. Please enter a valid "
                          "value.")
        return responses


def update_survey_sheet(new_data):
    """
    Updates the survey spreadsheet with the list of new responses.
    """
    print("Updating survey results spreadsheet...\n")
    SURVEY.append_row(new_data)
    print("Update complete!\n")


def validate_name(name):
    """
    Takes the name input by user following "read" command and checks whether
    it matches any of the names in the spreadsheet. If no match is found, user
    will be prompted until a match is detected, then the valid name is passed
    back to the main() function.
    """
    print("Validating name...")
    existing_names = SURVEY.col_values(1)
    while name not in existing_names:
        name = input("The name you entered does not exist. Please submit the "
                     "name of a respondent who has completed the survey.\n")
    print("Name validated.")
    return name


def validate_question():
    """
    Requests question number input by user following "read q" command and
    checks it is valid i.e. is a number between 1 and the number of the last
    column in the spreadsheet.
    """
    print("Validating question...\n")
    full_questions = get_questions("full")
    print("List of existing Qs:")
    for q in full_questions:
        print(q)
    print("")
    while True:
        try:
            question_number = input("Which question would you like to read "
                                    "the values for?: ")
            main_menu_check(question_number)
            if int(question_number) in range(1, SURVEY.col_count):
                break
            else:
                print(f"Not a valid question number. Please enter a value "
                      f"between 1 and {SURVEY.col_count - 1}.")
        except ValueError:
            print(f"Not a valid question number. Please enter a value "
                  f"between 1 and {SURVEY.col_count - 1}.")
    return int(question_number)


def check_existing_names(name):
    """
    Takes the name input by user following "add" command and checks whether it
    matches any of the names in the spreadsheet. If the name matches, user will
    be prompted until a new name is submitted, then the valid name is passed
    back to the main() function.
    """
    main_menu_check(name)
    print("Checking existing names...\n")
    existing_names = SURVEY.col_values(1)
    existing_names.pop(0)  # removes "Name" column header from list
    while name in existing_names:
        print("The name you entered already exists - you have already "
              "completed the survey!\n")
        name = input("Please enter the name of a new respondent.\n")
    return name


def read_respondent_data(name):
    """
    Reads a row of data from the spreadsheet based on the respondent name.
    """
    print(f"Reading {name}'s data...\n")
    name_cell = SURVEY.find(name)
    respondent_scores = SURVEY.row_values(name_cell.row)
    return respondent_scores


def read_question_data(question_number):
    """
    Outputs a list of respondent names and their scores for a given question.
    """
    existing_names = SURVEY.col_values(1)
    existing_names.pop(0)
    responses = SURVEY.col_values(question_number+1)
    summarised_question = responses.pop(0)
    longest_name = len(max(existing_names, key=len))
    print(get_border())
    print(f"LISTING RESULTS FOR {summarised_question}:\n")
    name_index = 0
    for response in responses:
        print(f"{existing_names[name_index].ljust(longest_name+5)}{response}")
        name_index += 1
    print("\n")


def analyse_respondent_data(respondent_data):
    """
    Conducts analysis on data passed through the main function following
    a "read" command, displaying the question responses and statistics
    for the given individual.
    """
    print("Analysing data...\n")
    # removes the name from the row, leaving just the scores
    respondent_name = respondent_data.pop(0)
    print(f"Results for {respondent_name} are as follows:\n")
    summarised_questions = get_questions("summarised")
    # converts scores to integers so that numerical analysis can be performed
    converted_scores = [int(x) for x in respondent_data]
    # calculates the mean score from the list
    average_score = statistics.mean(converted_scores)
    # calculates the variance from the list
    score_variance = statistics.variance(converted_scores)
    if score_variance > 2:
        variance_string = "high level of variance, indicating significant \n" \
        "disparity between the 'best' and 'worst' aspects of the job."
    elif score_variance > 1.3:
        variance_string = "moderate level of variance."
    else:
        variance_string = "low level of variance, suggesting the \n" \
        "respondent is very consistent in their perception about the "
        "qualities of the job."
    question_index = 0
    survey_data = SURVEY.get_all_values()
    survey_averages = get_averages(survey_data, "False")
    print(get_border())
    print("OVERALL RESULTS")
    print(f"{respondent_name} gave an average score of "
          f"{round(average_score, 1)} across all questions.")
    print(f"{respondent_name} had a variance of {round(score_variance, 1)} in "
          f"their scores. This is a {variance_string}")
    print(get_border())
    print("QUESTION".ljust(35) + "SCORE".ljust(8) + "COMPARISON")
    for score in respondent_data:
        if float(score) < (float(survey_averages[question_index]) - 0.4):
            print(f"{summarised_questions[question_index].ljust(35)}  {score} "
                  "    Significantly lower than the organisation average score"
                  f" ({survey_averages[question_index]})")
        elif float(score) > (float(survey_averages[question_index]) + 0.4):
            print(f"{summarised_questions[question_index].ljust(35)}  {score} "
                  "    Significantly higher than the organisation average "
                  f"score ({survey_averages[question_index]})")
        else:
            print(f"{summarised_questions[question_index].ljust(35)}  {score} "
                  f"    Close to the organisation average score ("
                  f"{survey_averages[question_index]})")
        question_index += 1
    print(get_border())
    min_score = min(converted_scores)
    # print(f"Min score: {min_score}")  # TESTING
    lowest_scored_questions = []
    count_min_index = 0
    # print(f"Converted scores for each Q: {converted_scores}")
    while count_min_index < SURVEY.col_count - 1:
        if converted_scores[count_min_index] == min_score:
            lowest_scored_questions.append(
                summarised_questions[count_min_index])
        count_min_index += 1
    print("AREAS OF CONCERN")
    print(f"Lowest scored question(s) scored {min_score} as follows: "
          f"{lowest_scored_questions}.")
    print(get_border())


def update_data(name_to_update, update_command):
    """
    Takes as parameters the name of the individual whose record is to be
    updated and whether user wishes to update one field, or their entire
    response set. Displays the current response set and requests
    confirmation that the user wishes to proceed. Updates the relevant cell
    or row of cells before returning to the main menu.
    """
    print("Updating data...\n")
    # print(f"UPDATE_DATA: Name {name_to_update}\n")
    # print(f"UPDATE_DATA: Command {update_command}\n")
    name_cell = SURVEY.find(name_to_update)
    row_to_update = name_cell.row
    while True:
        try:
            confirm = input(f"{name_to_update}'s responses are currently "
                            f"{read_respondent_data(name_to_update)[1:]}. "
                            "Are you sure you wish to amend this data? "
                            "(Y/N): ")
            main_menu_check(confirm)
            if confirm in ["Y", "y"]:
                break
            elif confirm in ["N", "n"]:
                print("Update aborted. Returning to main menu.\n")
                main()
            else:
                print("Please respond with 'Y' to proceed or 'N' to cancel.")
        except ValueError:
            print("Please respond with 'Y' to proceed or 'N' to cancel.")
    if update_command == 'all':
        update_data_list = get_respondent_data()
        print(f"Value responses {update_data_list} will now be updated for "
              f"{name_to_update}...")
        # The values start from the 2nd column onwards and .update_cell
        # is 1-indexed, so the loop index must start at 2 to insert correctly
        column_index = 2
        for update_value in update_data_list:
            SURVEY.update_cell(row_to_update, column_index, update_value)
            column_index += 1
        print("Update complete. Returning to main menu...\n")
    elif update_command == 'one':
        while True:
            try:
                question_number = input("Which question would you like to "
                                        "update the value for?: ")
                main_menu_check(question_number)
                if int(question_number) in range(1, SURVEY.col_count):
                    break
                else:
                    print(f"Not a valid question number. Please enter a value "
                          f"between 1 and {SURVEY.col_count - 1}.")
            except ValueError:
                print(f"Not a valid question number. Please enter a value "
                      f"between 1 and {SURVEY.col_count - 1}.")
        while True:
            try:
                update_value = input("Please enter the value you wish to "
                                     "add: ")
                main_menu_check(update_value)
                if int(update_value) in range(1, 6):
                    print(f"A score of {update_value} will now be updated to "
                          f"Q{question_number} for {name_to_update}...")
                    SURVEY.update_cell(row_to_update, question_number + 1,
                                       int(update_value))
                    print("Update complete. Returning to main menu...\n")
                    return
                else:
                    print("Not a number between 1 and 5. Please enter a valid "
                          "value.")
            except ValueError:
                print("Not a number between 1 and 5. Please enter a valid "
                      "value.")


def add_question():
    """
    Adds a new question to the survey and spreadsheet, with a summarised
    heading and the full text question held within the cell's note.
    """
    print("Adding new question to survey...\n")
    print("Please note that the responses for all previous respondents who "
          "have not answered the new question will be set to the median value "
          "(3).")
    print("You can update the default values by using the 'update' function "
          "from the main menu.\n")
    new_question = input("Please enter the full text question you wish to "
                         "add: \n")
    main_menu_check(new_question)
    new_summarised_question = input("Please enter the a summarised version "
                                    "(1 to 2 words): \n")
    main_menu_check(new_summarised_question)
    SURVEY.add_cols(1)
    next_question_column = SURVEY.col_count
    # print(next_question_column)
    potential_coordinates = get_potential_question_coordinates()
    cell_coordinate = f"{potential_coordinates[next_question_column - 2]}"
    # print(f"Column to insert to: {cell_coordinate[0]}")
    # print(f"Cell coordinate being passed: {cell_coordinate}")
    SURVEY.insert_note(cell_coordinate, f"Q{next_question_column - 1} - "
                       f"{new_question}")
    # print(f"column length to put in cell add {next_question_column}")
    SURVEY.update_cell(1, next_question_column, f"Q{next_question_column - 1}"
                       f" - {new_summarised_question}")
    print("Adding question heading...\n")
    col_values = SURVEY.col_values(1)
    number_of_rows = len(col_values)
    # print(number_of_rows)
    cell_index = 2
    print("Adding default value to past respondents...\n")
    while cell_index <= number_of_rows:
        SURVEY.update_cell(cell_index, next_question_column, 3)
        # print(f"put 3 in {cell_index} {next_question_column}")
        cell_index += 1
    print("The question has successfully been added to the survey.\n")


def get_potential_question_coordinates():
    """
    Creates a list of potential cell names to be used then calling the
    .insert_note gspread function, since this only accepts alphabetical
    column values (e.g. A1, K1)
    """
    potential_coordinates = []
    column_ids = ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                  "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y",
                  "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI",
                  "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS",
                  "AT", "AU", "AV", "AW", "AX", "AY", "AZ"]
    index = 0
    for letter in column_ids:
        potential_coordinates.append(letter + "1")
        index += 1
    # print(f"Potential coordinates (should be a list of A1, B1, C1, etc.): "
    #      f"{potential_coordinates}")
    return potential_coordinates


def delete_row(name):
    """
    Takes the validated name input by the user and deletes the corresponding
    row in the spreadsheet.
    """
    print(f"Deleting {name}'s data...\n")
    name_cell = SURVEY.find(name)
    SURVEY.delete_rows(name_cell.row)
    print(f"Deletion complete. {name}'s entry has been removed from the "
          "survey.\n")


def delete_question():
    """
    Provides a list of existing question then prompts user to give the number
    of the question they wish to delete from the survey. The column is then
    deleted and the number of the deleted question is returned to the main
    function.
    """
    # list all current Qs
    full_questions = get_questions("full")
    print("List of existing Qs:")
    for q in full_questions:
        print(q)
    print("")
    # print(q for q in full_questions)
    while True:
        try:
            question_number = input("Which question would you like to "
                                    "delete?: ")
            main_menu_check(question_number)
            if int(question_number) in range(1, SURVEY.col_count):
                print(f"Deleting question {question_number} from survey...\n")
                SURVEY.delete_columns(int(question_number) + 1)
                print("Deletion complete.\n")
                return int(question_number)
            else:
                print(f"Not a valid question number. Please enter a value "
                      f"between 1 and {SURVEY.col_count - 1}.")
        except ValueError:
            print(f"Not a valid question number. Please enter a value between "
                  f"1 and {SURVEY.col_count - 1}.")


def update_question_cells(number_of_deleted_question):
    """
    Following the deletion of a question, if the question was not the last one
    in the survey, this function updates the numbers in the summarised and full
    versions of questions to the right of the deleted question to keep in
    numerical ascending order.
    """
    print("Updating question headings...\n")
    potential_coordinates = get_potential_question_coordinates()
    full_questions = get_questions("full")
    position_index = number_of_deleted_question
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
        # print(f"New summary q string: {new_summarised_question}")
        # print(f"New full q string: {new_full_question}")
        # print(f"{new_summarised_question} will be added to Row 1, column "
        #       f"{position_index + 1}")
        # print(f"{new_full_question} will be added to Row 1, column "
        #       f"{position_index + 1}")
        # print(f"Potential coords: {potential_coordinates}")
        # print(f"Current: {potential_coordinates[SURVEY.col_count]}")
        cell_coordinate = f"{potential_coordinates[position_index - 1]}"
        SURVEY.update_cell(1, position_index + 1, new_summarised_question)
        SURVEY.insert_note(cell_coordinate, new_full_question)
        position_index += 1
        question_index += 1
    print("Updating complete.\n")


def get_questions(question_type):
    """
    Returns a list of the survey questions. The get_notes function returns
    a list of lists containing cell notes which needs to be unpacked before
    returning.
    """
    # print(f"Reading questions from survey spreadsheet...\n")
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
    table_border = "—"*100
    return table_border


def analyse_survey():
    """
    Conducts analysis of the overall survey data set, returning summarised
    information for each question, overall statistics, highlighting questions
    with low scores i.e. areas to work on
    """
    print("Analysing survey data...\n")
    survey_data = SURVEY.get_all_values()
    print(get_border())
    question_averages = get_averages(survey_data, True)
    summarised_questions = get_questions("summarised")
    print(get_border())
    print("AVERAGE SCORES\n")
    q_index = 0
    # prints all summarised Qs and avergae organisational score
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
        print("OVERALL SCORE")
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


def make_recommendations(analysed_data):
    """
    Makes recommendations based on the average scores calculated across the
    dataset.
    """
    print("HIGHLIGHTS\n")
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
    print(f"Low scoring questions: {low_scores}")
    print(f"High scoring questions: {high_scores}\n")
    low_scores_headings = []
    for question in low_scores:
        # removes text before words from questions (e.g. "Q1 - ") before append
        low_scores_headings.append(question[5:])
    print("Based on the average scores, areas of concern for the organisation "
          "should be: ")
    for heading in low_scores_headings:
        print(f"{heading}")
    print(get_border())
    print("Analysis complete. Returning to main menu...\n")


def main():
    """
    Run all program functions.
    """
    user_type = get_user_type()
    while True:  # loops until user enters 'exit' command
        main_command = process_main_command(user_type)
        main_menu_check(main_command)
        match main_command:
            case 'add':
                if user_type == "admin":
                    respondent_name = input("Please enter the exact name you "
                                            "wish to add data for: ")
                elif user_type == "respondent":
                    respondent_name = input("Please enter your full name: ")
                main_menu_check(respondent_name)
                respondent_name_checked = check_existing_names(respondent_name)
                responses = get_respondent_data()
                responses.insert(0, respondent_name_checked)
                update_survey_sheet(responses)
            case 'update':
                if user_type == "admin":
                    name_to_update = input("Enter the exact name of the person"
                                           " whose results you wish to update:"
                                           " ")
                elif user_type == "respondent":
                    name_to_update = input("Please enter your full name: ")
                main_menu_check(name_to_update)
                validated_name_to_update = validate_name(name_to_update)
                update_command = process_update_command()
                update_data(validated_name_to_update, update_command)
            case 'delete':
                name_to_delete = input("Enter the exact name of the respondent"
                                       "you wish to delete survey results for:"
                                       " \n")
                main_menu_check(name_to_delete)
                validated_name_to_delete = validate_name(name_to_delete)
                delete_row(validated_name_to_delete)
            case 'list':
                list_respondents()
            case 'read':
                read_name = input("Enter the exact name of the respondent you "
                                  "wish to see survey results for: \n")
                main_menu_check(read_name)
                validated_read_name = validate_name(read_name)
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
                make_recommendations(analysed_data)
            case 'exit':
                print("The application will now close.")
                quit()


print("")
print("Welcome to DT Survey Analytics.\n")
main()
