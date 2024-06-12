""" [app.py]: this file where the user interact with our program """

import re
from datetime import datetime

from src import database

MENU_PROMPT = """\n--SCHOOL APP SYSTEM--
a) Add a new student.
b) Exit.

Your Selection: """


def menu():
    connection = database.connect()
    database.create_tables(connection)

    while (user_input := input(MENU_PROMPT)) != 'b':
        if user_input == 'a':
            prompt_add_new_student(connection)
        else:
            print("\n===Invalid operation, please try again!===\n")

    print("\n===Thank You for visiting us!===\n")
    database.cleanup(connection)


def prompt_add_new_student(connection):
    student_detail = []
    lesson_detail = []
    try:
        while True:
            try:
                student_id = input("Enter student ID: ")
                validate_student_id(connection, student_id)
                student_detail.append(student_id)
                break
            except ValueError:
                continue

        while True:
            try:
                first_name = input("Enter student first name: ")
                validate_labels(first_name, "first_name")
                student_detail.append(first_name)
                break
            except ValueError:
                continue

        while True:
            try:
                last_name = input("Enter student last name: ")
                validate_labels(last_name, "last_name")
                student_detail.append(last_name)
                break
            except ValueError:
                continue

        while True:
            try:
                age = input("Enter student age: ")
                validate_age(age)
                student_detail.append(age)
                break
            except ValueError:
                continue

        while True:
            try:
                grade = input("Enter student grade: ")
                validate_labels(grade, "grade")
                student_detail.append(grade)
                break
            except ValueError:
                continue

        while True:
            try:
                enrolled_date = input(
                    "Enter student enrolled date in this format (dd-MM-YYYY). Press Enter to get default date: "
                )
                enrolled_date = validate_enrolled_date(enrolled_date)
                student_detail.append(enrolled_date)
                break
            except ValueError:
                continue

        while True:
            try:
                lesson_num = input("Enter number of student enrolled lessons: ")
                lesson_detail = validate_lesson_detail(lesson_num)
                break
            except ValueError:
                continue

        database.add_records(connection, student_detail, lesson_detail)
        display_success_message("added student")

    except ValueError:
        return


# Name: Functions with syntax like [validate_input()]
# Goal: Used to assure data is inserted correctly by the user.
def validate_student_id(connection, student_id):
    student_id = validate_filled_records(student_id)

    if not student_id.isdigit():
        display_error_message(f"Try again, ({student_id}) is not allowed. Enter a unique integer number!")
        raise ValueError
    if database.is_student_exist(connection, student_id):
        display_error_message(
            f"Try again, this id: ({student_id}) is reserved for another student. Press u to update it!"
        )
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
                display_error_message(
                    f'Try again, {label} cannot contain "{char}". Please enter letters only!'
                )
                raise ValueError

        if len(user_input) < 3:
            display_error_message(
                f"Try again, ({user_input}) is not allowed. {label} must contain 3 letters at least!"
            )
            raise ValueError

    if len(user_input) >= 15:
        display_error_message(
            f'Try again, {label} is too long. Max allowed characters is 15!'
        )
        raise ValueError

    for char in not_allowed_chars:
        if char in user_input:
            display_error_message(
                f'Try again, {label} cannot contain "{char}". Please enter valid characters  only!'
            )
            raise ValueError


def validate_age(age):
    age = validate_filled_records(age)

    if not age.isdigit() or 5 > int(age) or int(age) > 35:
        display_error_message(
            f"Try again, ({age}) is not allowed. Enter a valid age (must be between 5 and 35)!"
        )
        raise ValueError


def validate_enrolled_date(enrolled_date):
    pattern_date = r'^\d{2}-\d{2}-\d{4}$'
    today_date = datetime.today().strftime('%d-%m-%Y')

    if enrolled_date == "":
        enrolled_date = today_date
        print(f'\n--> enrolled date is {enrolled_date} <--\n')

    if not re.match(pattern_date, enrolled_date):
        display_error_message(
            f"Try again, {enrolled_date} is invalid. Make sure your enrolled date match this format (dd-MM-YYYY)"
        )
        raise ValueError

    if not int(enrolled_date.split('-')[0]) <= 31:
        display_error_message(
            f"Try again, this day {enrolled_date.split('-')[0]} is invalid. Max day number is 31"
        )
        raise ValueError

    if not int(enrolled_date.split('-')[1]) <= 12:
        display_error_message(
            f"Try again, this month {enrolled_date.split('-')[1]} is invalid. Max month number is 12"
        )
        raise ValueError

    if not int(enrolled_date.split('-')[2]) >= 1900:
        display_error_message(
            f"Try again, this year {enrolled_date.split('-')[2]} is invalid. Min year number is 1900"
        )
        raise ValueError
    return enrolled_date


def validate_lesson_detail(lesson_num):
    lesson_num = validate_filled_records(lesson_num)

    if not lesson_num.isdigit():
        display_error_message(
            f"Try again, ({lesson_num}) is not allowed. lesson number must be an integer!"
        )
        raise ValueError

    if lesson_num == '0':
        display_error_message(
            f"Try again, ({lesson_num}) is not allowed. Student must have at least 1 lesson!"
        )
        raise ValueError

    lesson_detail = []
    for num in range(0, int(lesson_num)):
        lesson = input(f"Lesson {num + 1}: ")
        lesson = validate_filled_records(lesson)
        validate_labels(lesson, "lesson")
        lesson_detail.append(lesson)

    return lesson_detail


def validate_filled_records(user_input):
    user_input = user_input.strip()
    if user_input == "":
        display_error_message(
            f"Try again. You cannot add empty value!"
        )
        raise ValueError
    return user_input


# Name: Functions with syntax like [display_state_message()]
# Goal: Used to show helpful messages for the user.
def display_error_message(error):
    print(f"\n{error}")


def display_success_message(message):
    print("\n You've " + message + " successfully!")


menu()
