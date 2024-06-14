import re
from datetime import datetime

from src import database
from src.utils import util_messages as um


# Name: Functions with syntax like [validate_input()]
# Goal: Used to assure data is inserted correctly by the user.
def validate_student_id(connection, student_id, operation):
    student_id = validate_filled_records(student_id)

    if not student_id.isdigit():
        um.display_error_message(f"Try again, ({student_id}) is not allowed. Enter a unique integer number!")
        raise ValueError

    if operation == "add":
        if database.is_student_exist(connection, student_id):
            um.display_error_message(f"Try again, this student id: ({student_id}) is reserved for another student!")
            raise ValueError

    if operation == "update" or operation == "delete":
        if not database.is_student_exist(connection, student_id):
            um.display_error_message(f"Try again, this student id: ({student_id}) doesn't exist. Please add it first!")
            raise ValueError


def validate_labels(user_input, label):
    not_allowed_chars = (
        '.', ';', '/', '-', '%', '*', '$', '+', '-', '#', '{', '[', '~', '@', '=', '?', '&', '|', '^', '<', '>',
        ':', '£', '!', '°', '('
    )
    not_allowed_num_chars = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

    user_input = validate_filled_records(user_input)

    if not label == "grade" and not label == "lesson":
        for char in not_allowed_num_chars:
            if char in user_input:
                um.display_error_message(f'Try again, {label} cannot contain "{char}". Please enter letters only!')
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

    if not age.isdigit() or 5 > int(age) or int(age) > 35:
        um.display_error_message(f"Try again, ({age}) is not allowed. Enter a valid age (must be between 5 and 35)!")
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


def validate_lesson_detail(lesson_num):
    lesson_num = validate_filled_records(lesson_num)

    if not lesson_num.isdigit():
        um.display_error_message(f"Try again, ({lesson_num}) is not allowed. lesson number must be an integer!")
        raise ValueError

    if lesson_num == '0':
        um.display_error_message(f"Try again, ({lesson_num}) is not allowed. Student must have at least 1 lesson!")
        raise ValueError

    lesson_detail = []
    for num in range(0, int(lesson_num)):
        lesson = input(f"Lesson {num + 1}: ")
        lesson = validate_filled_records(lesson)
        validate_labels(lesson, "lesson")
        lesson_detail.append(lesson)
        if um.cancel_operation(lesson):
            break

    return lesson_detail


def validate_selected_enrolled_lesson(lesson_num, number_of_lessons):
    lesson_num = validate_filled_records(lesson_num)

    if not lesson_num.isdigit():
        um.display_error_message(f"Try again, ({lesson_num}) is not allowed. lesson number must be an integer!")
        raise ValueError

    if lesson_num == '0':
        um.display_error_message(f"Try again, ({lesson_num}) is not allowed. This selection is not available option!")
        raise ValueError

    lesson_availability = int(lesson_num) - 1 in range(number_of_lessons + 1)
    if not lesson_availability:
        um.display_error_message(f"Try again, ({lesson_num}) is not allowed. This selection is not available option!")
        raise ValueError

    return int(lesson_num)


def validate_filled_records(user_input):
    user_input = user_input.strip()
    if user_input == "":
        um.display_error_message(f"Try again. You cannot add empty value!")
        raise ValueError
    return user_input
