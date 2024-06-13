""" [app.py]: this file where the user interact with our program """

import re
from datetime import datetime

from src import database

MENU_PROMPT = """\n -- SCHOOL APP SYSTEM --
a) Add a new student.
u) Update existed student.
e) Exit.

Your Selection: """

MENU_UPDATE_PROMPT = """\n -- What do you want to update? Note: Press c to cancel! --
1) Student's first name.
2) Student's last name.
3) Student's age.
4) Student's grade.
5) Student's enrollment date.
6) Student's enrolled lessons.

7) I'm Done. (!CHANGES WILL BE SAVED ONLY IF YOU PRESS 7!)

Your selection: """


def menu():
    connection = database.connect()
    database.create_tables(connection)

    while (user_input := input(MENU_PROMPT)) != 'e':
        if user_input == 'a':
            prompt_add_new_student(connection)
        elif user_input == 'u':
            prompt_update_old_student(connection)
        else:
            print("\n -- Invalid operation, please try again! -- ")

    print("\n -- Thank You for visiting us! --")
    database.cleanup(connection)


def cancel_operation(input_value):
    if input_value.lower() == 'c':
        print("\n -- Operation Canceled! -- ")
    return input_value.lower() == 'c'


def prompt_add_new_student(connection):
    student_detail = []
    lesson_detail = []

    print("\n -- Press 'c' to cancel the whole operation! -- \n")

    while True:
        while True:
            student_id = input("Enter student ID: ")
            if cancel_operation(student_id):
                return
            try:
                validate_student_id(connection, student_id, "add")
                student_detail.append(student_id)
                break
            except ValueError:
                continue

        while True:
            first_name = input("Enter student first name: ")
            if cancel_operation(first_name):
                return
            try:
                validate_labels(first_name, "first_name")
                student_detail.append(first_name)
                break
            except ValueError:
                continue

        while True:
            last_name = input("Enter student last name: ")
            if cancel_operation(last_name):
                return
            try:
                validate_labels(last_name, "last_name")
                student_detail.append(last_name)
                break
            except ValueError:
                continue

        while True:
            age = input("Enter student age: ")
            if cancel_operation(age):
                return
            try:
                validate_age(age)
                student_detail.append(age)
                break
            except ValueError:
                continue

        while True:
            grade = input("Enter student grade: ")
            if cancel_operation(grade):
                return
            try:
                validate_labels(grade, "grade")
                student_detail.append(grade)
                break
            except ValueError:
                continue

        while True:
            enrol_date = input(
                "Enter student enrolled date in this format (dd-MM-YYYY). Press Enter to get default date: ")
            if cancel_operation(enrol_date):
                return
            try:
                enrol_date = validate_enrolled_date(enrol_date)
                student_detail.append(enrol_date)
                break
            except ValueError:
                continue

        while True:
            lesson_num = input("Enter number of student's enrolled lessons: ")
            if cancel_operation(lesson_num):
                return

            try:
                lesson_detail = validate_lesson_detail(lesson_num)
                if 'c' in lesson_detail:
                    return

                break
            except ValueError:
                continue

        # If we reach this point, all inputs are valid and the student can be added
        break

    database.add_records(connection, student_detail, lesson_detail)
    display_success_message("added student")


def prompt_update_old_student(connection):
    # records initially are empty
    updated_student_records = {}
    updated_lesson_records = {}

    print("\n -- Press 'c' to cancel the whole operation! -- \n")

    # We check if the student exist first
    while True:

        student_id = input("Enter Student ID of the student you want to update: ")
        if cancel_operation(student_id):  # User press c -> cancel the operation
            return
        try:
            validate_student_id(connection, student_id, "update")
            break
        except ValueError:
            continue

    while (user_input := input(MENU_UPDATE_PROMPT)) != '7':

        if user_input == '1':
            while True:
                first_name = input("Enter a new first name: ")
                if cancel_operation(first_name):
                    return
                try:
                    validate_labels(first_name, "first_name")
                    updated_student_records["first_name"] = first_name
                    break
                except ValueError:
                    continue

        elif user_input == '2':
            while True:
                last_name = input("Enter a new last name: ")
                if cancel_operation(last_name):
                    return
                try:
                    validate_labels(last_name, "last_name")
                    updated_student_records["last_name"] = last_name
                    break  # this will break the inner loop
                except ValueError:
                    continue

        elif user_input == '3':
            while True:
                age = input("Enter a new age: ")
                if cancel_operation(age):
                    return
                try:
                    validate_age(age)
                    updated_student_records["age"] = age
                    break
                except ValueError:
                    continue

        elif user_input == '4':
            while True:
                grade = input("Enter a new grade: ")
                if cancel_operation(grade):
                    return
                try:
                    validate_labels(grade, "grade")
                    updated_student_records["grade"] = grade
                    break
                except ValueError:
                    continue

        elif user_input == '5':
            while True:
                enrol_date = input(
                    "Enter updated student's enrolled date in this format (dd-MM-YYYY). Press Enter to get default "
                    "date: "
                )
                if cancel_operation(enrol_date):
                    return
                try:
                    enrol_date = validate_enrolled_date(enrol_date)
                    updated_student_records["enrol_date"] = enrol_date
                    break
                except ValueError:
                    continue

        elif user_input == '6':
            # Get lessons that selected student enroll in
            lessons = database.get_lesson_name_by_student_id(connection, student_id)
            number_of_enrolled_lessons = len(lessons)

            # Turn them into an input prompt for updating
            menu_update_lesson_names_prompt = create_menu_update_lesson_names_prompt(
                lessons,
                number_of_enrolled_lessons
            )

            while True:

                selected_enrolled_lesson = input(menu_update_lesson_names_prompt)
                if cancel_operation(selected_enrolled_lesson):
                    return
                try:
                    selected_enrolled_lesson = validate_selected_enrolled_lesson(
                        selected_enrolled_lesson,
                        number_of_enrolled_lessons
                    )
                    if selected_enrolled_lesson == number_of_enrolled_lessons + 1:
                        print("\nAll changes have been saved. Press '7' to update it!")
                        break
                    else:
                        while True:
                            old_lesson = lessons[selected_enrolled_lesson - 1][0]
                            new_lesson = input(f"Update {old_lesson} with: ")
                            if cancel_operation(new_lesson):
                                return
                            try:
                                validated_lesson = validate_filled_records(new_lesson)
                                validate_labels(validated_lesson, "lesson")
                                updated_lesson_records[old_lesson] = validated_lesson
                                break
                            except ValueError:
                                continue
                except ValueError:
                    continue

        elif user_input == 'c':
            cancel_operation(user_input)
            return

        else:
            print("\n -- Invalid operation, please try again! -- ")

    if len(updated_student_records) != 0:
        database.update_student(connection, student_id, updated_student_records)
        display_success_message("updated student's info")
    else:
        display_error_message("No student info have been updated!")

    if len(updated_lesson_records) != 0:
        database.update_lesson(connection, updated_lesson_records, student_id)
        display_success_message("updated student's info")
    else:
        display_error_message("No lesson name have been updated!")


# Name: Functions with syntax like [validate_input()]
# Goal: Used to assure data is inserted correctly by the user.
def validate_student_id(connection, student_id, operation):
    student_id = validate_filled_records(student_id)

    if not student_id.isdigit():
        display_error_message(f"Try again, ({student_id}) is not allowed. Enter a unique integer number!")
        raise ValueError

    if operation == "add":
        if database.is_student_exist(connection, student_id):
            display_error_message(
                f"Try again, this student id: ({student_id}) is reserved for another student!"
            )
            raise ValueError

    if operation == "update":
        if not database.is_student_exist(connection, student_id):
            display_error_message(
                f"Try again, this student id: ({student_id}) doesn't exist. Please add it first!"
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

    if len(user_input) >= 20:
        display_error_message(
            f'Try again, {label} is too long. Max allowed characters is 20!'
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
        if cancel_operation(lesson):
            break

    return lesson_detail


def validate_selected_enrolled_lesson(lesson_num, number_of_lessons):
    lesson_num = validate_filled_records(lesson_num)

    if not lesson_num.isdigit():
        display_error_message(
            f"Try again, ({lesson_num}) is not allowed. lesson number must be an integer!"
        )
        raise ValueError

    if lesson_num == '0':
        display_error_message(
            f"Try again, ({lesson_num}) is not allowed. This selection is not available option!"
        )
        raise ValueError

    lesson_availability = int(lesson_num) - 1 in range(number_of_lessons + 1)
    if not lesson_availability:
        display_error_message(
            f"Try again, ({lesson_num}) is not allowed. This selection is not available option!"
        )
        raise ValueError

    return int(lesson_num)


def get_list_of_available_lessons(lessons):
    lesson_names = []

    # turn lessons into a list
    for lesson in lessons:
        lesson_names.append(lesson[0])

    return lesson_names


def create_menu_update_lesson_names_prompt(lessons, number_of_lessons):
    lesson_names = get_list_of_available_lessons(lessons)
    menu_lessons_prompt = "\nChoose which lesson you want to update: \n"

    # make it as a prompt
    for lesson_num in range(number_of_lessons):
        menu_lessons_prompt += f"\n{lesson_num + 1}) {lesson_names[lesson_num]}."

    menu_lessons_prompt += f"\n\n{number_of_lessons + 1}) I'm Done!." + "\n\nYour Selection: "
    return menu_lessons_prompt


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
