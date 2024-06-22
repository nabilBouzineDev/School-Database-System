import re
from datetime import datetime

import database
import utils.util_display as um


def get_valid_input(
        prompt_message,
        validation_function,
        container=None,
        label=None,
        connection=None,
        key=None,
        extra=None
):
    """
    It's responsible to validate different user inputs in different scenarios
    :param prompt_message:  The message to prompt the user.
    :param validation_function: The function to validate the input.
    :param container: An optional data structure to store the validated input.
    :param label: An optional label for the validation function.
    :param connection: An optional db connection for validation function.
    :param key: An optional key for the dict container.
    :param extra: An optional extra parameter for validation functions that depend on other variables
    :returns: None if user press 'c' or the validated user_input
    """

    while True:
        input_value = input(prompt_message)
        if um.cancel_operation(input_value):
            return None

        try:
            if connection is not None:
                validation_function(connection, input_value, label)
            else:
                if label is not None:
                    validation_function(input_value, label)
                else:
                    if extra is not None:
                        validation_result = validation_function(input_value, extra)
                    else:
                        validation_result = validation_function(input_value)

                    if validation_result:
                        input_value = validation_result

            if container is not None:
                if isinstance(container, list):
                    if isinstance(input_value, list):
                        container = input_value
                    else:
                        container.append(input_value)
                else:
                    container[key] = input_value

            return input_value
        except ValueError:
            continue


def is_record_a_number(user_input):
    return user_input.isdigit()


# Name: Functions with syntax like [validate_input()]
# Goal: Used to assure data is inserted correctly by the user.
def validate_filled_records(user_input):
    user_input = user_input.strip()
    if user_input == "":
        um.display_error_message(f"Try again. You cannot add empty value!")
        raise ValueError
    return user_input


def validate_student_id(connection, student_id, operation):
    student_id = validate_filled_records(student_id)

    if not is_record_a_number(student_id):
        um.display_error_message(f"Try again, ({student_id}) is not allowed. Enter a unique integer number!")
        raise ValueError

    if operation == "add":
        if database.is_student_exist(connection, student_id):
            um.display_error_message(f"Try again, this student id: ({student_id}) is reserved for another student!")
            raise ValueError

    if operation != "add":
        if not database.is_student_exist(connection, student_id):
            um.display_error_message(f"Try again, this student id: ({student_id}) doesn't exist. Please add it first!")
            raise ValueError


def validate_labels(user_input, label):
    not_allowed_chars = (
        '.', ';', '/', '-', '%', '*', '$', '+', '-', '#', '{', '[', '~', '@', '=', '?', '&', '|', '^', '<', '>',
        ':', '£', '!', '°', '('
    )

    user_input = validate_filled_records(user_input)

    if not label == "grade" and not label == "lesson":

        if is_record_a_number(user_input):
            um.display_error_message(f'Try again, {label} cannot contain numbers. Please enter letters only!')
            raise ValueError

    if len(user_input) < 3:
        um.display_error_message(
            f"Try again, ({user_input}) is not allowed. {label} must contain 3 letters at least!")
        raise ValueError

    if len(user_input) >= 20:
        um.display_error_message(f'Try again, {label} is too long. Max allowed characters is 20!')
        raise ValueError

    for char in not_allowed_chars:
        if char in user_input:
            um.display_error_message(
                f'Try again, {label} cannot contain "{char}". Please enter valid characters  only!')
            raise ValueError


def validate_age(age):
    age = validate_filled_records(age)

    if not is_record_a_number(age):
        um.display_error_message(f"Try again, ({age}) is not allowed. Age must be a number!")
        raise ValueError

    if 5 > int(age) or int(age) > 35:
        um.display_error_message(f"Try again, ({age}) is not allowed. Age must be between 5 and 35!")
        raise ValueError


def validate_enrolled_date(enrolled_date):
    pattern_date = r'^\d{2}-\d{2}-\d{4}$'
    today_date = datetime.today().strftime('%d-%m-%Y')

    if enrolled_date == "":
        enrolled_date = today_date
        print(f'\n--> enrolled date is {enrolled_date} <--\n')

    if not re.match(pattern_date, enrolled_date):
        um.display_error_message(
            f"Try again, {enrolled_date} is invalid. Make sure your enrolled date match this format (dd-MM-YYYY)")
        raise ValueError

    if not int(enrolled_date.split('-')[0]) <= 31:
        um.display_error_message(f"Try again, this day {enrolled_date.split('-')[0]} is invalid. Max day number is 31")
        raise ValueError

    if not int(enrolled_date.split('-')[1]) <= 12:
        um.display_error_message(
            f"Try again, this month {enrolled_date.split('-')[1]} is invalid. Max month number is 12")
        raise ValueError

    if not int(enrolled_date.split('-')[2]) >= 1900:
        um.display_error_message(
            f"Try again, this year {enrolled_date.split('-')[2]} is invalid. Min year number is 1900")
        raise ValueError
    return enrolled_date


def validate_lesson_number(lesson_num):
    lesson_num = validate_filled_records(lesson_num)

    if not is_record_a_number(lesson_num):
        um.display_error_message(f"Try again, ({lesson_num}) is not allowed. lesson number must be an integer!")
        raise ValueError

    if lesson_num == '0':
        um.display_error_message(f"Try again, ({lesson_num}) is not allowed. Student must have at least 1 lesson!")
        raise ValueError


def validate_selected_enrolled_lesson(selected_lesson_num, select_done_idx):
    if not is_record_a_number(selected_lesson_num):
        um.display_error_message(
            f"Try again, ({selected_lesson_num}) is not allowed. The index of selection must be a number!"
        )
        raise ValueError

    selected_enrolled_lesson_idx = int(selected_lesson_num)

    selection_availability = selected_enrolled_lesson_idx in range(1, select_done_idx + 1)
    if not selection_availability:
        um.display_error_message(
            f"Try again, ({selected_enrolled_lesson_idx}) is not allowed. This selection is not available option!"
        )
        raise ValueError

    # User is done with updating lessons
    if selected_enrolled_lesson_idx == select_done_idx:
        print("\nAll changes have been saved. Press '7' to update it!\n")
        return select_done_idx

    return selected_enrolled_lesson_idx
