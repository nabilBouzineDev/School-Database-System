""" [app.py]: this file where the user interact with our program """

from src import database
from utils import util_messages as um
from utils import utils_validations as uv

MENU_PROMPT = """\n -- SCHOOL APP SYSTEM --
a) Add a new student.
u) Update a student.
d) Delete a student. 
s) See student infos.
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
        elif user_input == 'd':
            prompt_delete_student(connection)
        elif user_input == 's':
            prompt_select_student(connection)
        else:
            print("\n -- Invalid operation, please try again! -- ")

    print("\n -- Thank You for visiting us! --")
    database.cleanup(connection)


def prompt_add_new_student(connection):
    student_detail = []
    lesson_detail = []

    print("\n -- Press 'c' to cancel the whole operation! -- \n")

    while True:
        while True:
            student_id = input("Enter student ID: ")
            if um.cancel_operation(student_id):
                return
            try:
                uv.validate_student_id(connection, student_id, "add")
                student_detail.append(student_id)
                break
            except ValueError:
                continue

        while True:
            first_name = input("Enter student first name: ")
            if um.cancel_operation(first_name):
                return
            try:
                uv.validate_labels(first_name, "first_name")
                student_detail.append(first_name)
                break
            except ValueError:
                continue

        while True:
            last_name = input("Enter student last name: ")
            if um.cancel_operation(last_name):
                return
            try:
                uv.validate_labels(last_name, "last_name")
                student_detail.append(last_name)
                break
            except ValueError:
                continue

        while True:
            age = input("Enter student age: ")
            if um.cancel_operation(age):
                return
            try:
                uv.validate_age(age)
                student_detail.append(age)
                break
            except ValueError:
                continue

        while True:
            grade = input("Enter student grade: ")
            if um.cancel_operation(grade):
                return
            try:
                uv.validate_labels(grade, "grade")
                student_detail.append(grade)
                break
            except ValueError:
                continue

        while True:
            enrol_date = input(
                "Enter student enrolled date in this format (dd-MM-YYYY). Press Enter to get default date: ")
            if um.cancel_operation(enrol_date):
                return
            try:
                enrol_date = uv.validate_enrolled_date(enrol_date)
                student_detail.append(enrol_date)
                break
            except ValueError:
                continue

        while True:
            lesson_num = input("Enter number of student's enrolled lessons: ")
            if um.cancel_operation(lesson_num):
                return

            try:
                lesson_detail = uv.validate_lesson_detail(lesson_num)
                if 'c' in lesson_detail:
                    return

                break
            except ValueError:
                continue

        # If we reach this point, all inputs are valid and the student can be added
        break

    database.add_records(connection, student_detail, lesson_detail)
    um.display_success_message("added student")


def prompt_update_old_student(connection):
    # records initially are empty
    updated_student_records = {}
    updated_lesson_records = {}

    print("\n -- Press 'c' to cancel the whole operation! -- \n")

    # We check if the student exist first
    while True:

        student_id = input("Enter Student ID of the student you want to update: ")
        if um.cancel_operation(student_id):  # User press c -> cancel the operation
            return
        try:
            uv.validate_student_id(connection, student_id, "update")
            break
        except ValueError:
            continue

    while (user_input := input(MENU_UPDATE_PROMPT)) != '7':

        if user_input == '1':
            while True:
                first_name = input("Enter a new first name: ")
                if um.cancel_operation(first_name):
                    return
                try:
                    uv.validate_labels(first_name, "first_name")
                    updated_student_records["first_name"] = first_name
                    break
                except ValueError:
                    continue

        elif user_input == '2':
            while True:
                last_name = input("Enter a new last name: ")
                if um.cancel_operation(last_name):
                    return
                try:
                    uv.validate_labels(last_name, "last_name")
                    updated_student_records["last_name"] = last_name
                    break  # this will break the inner loop
                except ValueError:
                    continue

        elif user_input == '3':
            while True:
                age = input("Enter a new age: ")
                if um.cancel_operation(age):
                    return
                try:
                    uv.validate_age(age)
                    updated_student_records["age"] = age
                    break
                except ValueError:
                    continue

        elif user_input == '4':
            while True:
                grade = input("Enter a new grade: ")
                if um.cancel_operation(grade):
                    return
                try:
                    uv.validate_labels(grade, "grade")
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
                if um.cancel_operation(enrol_date):
                    return
                try:
                    enrol_date = uv.validate_enrolled_date(enrol_date)
                    updated_student_records["enrol_date"] = enrol_date
                    break
                except ValueError:
                    continue

        elif user_input == '6':
            # Get lessons that selected student enroll in
            lessons = database.get_lesson_names_by_student_id(connection, student_id)
            number_of_enrolled_lessons = len(lessons)

            # Turn them into an input prompt for updating
            menu_update_lesson_names_prompt = create_menu_update_lesson_names_prompt(
                lessons,
                number_of_enrolled_lessons
            )

            while True:

                selected_enrolled_lesson = input(menu_update_lesson_names_prompt)
                if um.cancel_operation(selected_enrolled_lesson):
                    return
                try:
                    selected_enrolled_lesson = uv.validate_selected_enrolled_lesson(
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
                            if um.cancel_operation(new_lesson):
                                return
                            try:
                                validated_lesson = uv.validate_filled_records(new_lesson)
                                uv.validate_labels(validated_lesson, "lesson")
                                updated_lesson_records[old_lesson] = validated_lesson
                                break
                            except ValueError:
                                continue
                except ValueError:
                    continue

        elif user_input == 'c':
            um.cancel_operation(user_input)
            return

        else:
            print("\n -- Invalid operation, please try again! -- ")

    if len(updated_student_records) != 0:
        database.update_student(connection, student_id, updated_student_records)
        um.display_success_message("updated student's info")
    else:
        um.display_error_message("No student info have been updated!")

    if len(updated_lesson_records) != 0:
        database.update_lesson(connection, updated_lesson_records, student_id)
        um.display_success_message("updated lesson")
    else:
        um.display_error_message("No lesson name have been updated!")


def prompt_delete_student(connection):
    print("\n -- Press 'c' to cancel the whole operation! -- \n")

    while True:
        student_id = input("Enter student ID You want to delete: ")
        if um.cancel_operation(student_id):
            return
        try:
            uv.validate_student_id(connection, student_id, "delete")
            break
        except ValueError:
            continue

    database.delete_student(connection, student_id)
    um.display_success_message("deleted student")


def prompt_select_student(connection):
    print("\n -- Press 'c' to cancel the whole operation! --")

    while True:
        student_id = input("\nEnter student ID You want to display: ")
        if um.cancel_operation(student_id):
            return
        try:
            uv.validate_student_id(connection, student_id, "select")
            break
        except ValueError:
            continue

    # display the results
    student_infos = database.get_student_infos(connection, student_id)
    um.display_student_infos_table(student_infos)


# turn lessons fetched from db as tuples into a list
def get_list_of_available_lessons(lessons):
    lesson_names = []

    for lesson in lessons:
        lesson_names.append(lesson[0])

    return lesson_names


# Generate a menu message based on lessons we've
def create_menu_update_lesson_names_prompt(lessons, number_of_lessons):
    lesson_names = get_list_of_available_lessons(lessons)
    menu_lessons_prompt = "\n -- Choose which lesson you want to update. Press c to cancel! -- \n"

    # make it as a prompt
    for lesson_num in range(number_of_lessons):
        menu_lessons_prompt += f"\n{lesson_num + 1}) {lesson_names[lesson_num]}."

    menu_lessons_prompt += f"\n\n{number_of_lessons + 1}) I'm Done!." + "\n\nYour Selection: "
    return menu_lessons_prompt


menu()
