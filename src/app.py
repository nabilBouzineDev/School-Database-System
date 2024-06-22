""" [app.py]: this file where the user interact with our program """

import database
import utils.util_display as um
import utils.util_validations as uv

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

    try:
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
    finally:
        print("\n -- Thank You for visiting us! --")
        database.cleanup(connection)


# Name: Functions with syntax like [prompt_feature()]
# Goal: Used to prompt messages to guide user interactions at each step.
def prompt_add_new_student(connection):
    student_detail = []
    lesson_detail = []

    print("\n -- Press 'c' to cancel the whole operation! --")

    while True:

        student_id = uv.get_valid_input(
            prompt_message="Enter student ID: ",
            validation_function=uv.validate_student_id,
            container=student_detail,
            label="add",
            connection=connection
        )
        if student_id is None:
            return

        first_name = uv.get_valid_input(
            prompt_message="Enter student first name: ",
            validation_function=uv.validate_labels,
            container=student_detail,
            label="first_name"
        )
        if first_name is None:
            return

        last_name = uv.get_valid_input(
            prompt_message="Enter student last name: ",
            validation_function=uv.validate_labels,
            container=student_detail,
            label="last_name"
        )
        if last_name is None:
            return

        age = uv.get_valid_input(
            prompt_message="Enter student age: ",
            validation_function=uv.validate_age,
            container=student_detail,
        )
        if age is None:
            return

        grade = uv.get_valid_input(
            prompt_message="Enter student grade: ",
            validation_function=uv.validate_labels,
            container=student_detail,
            label="grade"
        )
        if grade is None:
            return

        enrol_date = uv.get_valid_input(
            prompt_message="""
            Enter student enrolled date in this format (dd-MM-YYYY). Press Enter to get default date: """
            .lstrip(),
            validation_function=uv.validate_enrolled_date,
            container=student_detail,
            )
        if enrol_date is None:
            return

        lesson_num = uv.get_valid_input(
            prompt_message="Enter number of student's enrolled lessons: ",
            validation_function=uv.validate_lesson_number,
        )
        if lesson_num is None:
            return
        else:
            for num in range(0, int(lesson_num)):
                lesson = uv.get_valid_input(
                    prompt_message=f"Lesson {num + 1}: ",
                    validation_function=uv.validate_labels,
                    container=lesson_detail,
                    label="lesson"
                )
                if lesson is None:
                    return

        # If we reach this point, all inputs are valid and the student can be added
        break

    database.add_records(connection, student_detail, lesson_detail)
    um.display_success_message("added student")


def prompt_update_old_student(connection):
    # records initially are empty
    updated_student_records = {}
    updated_lesson_records = {}

    print("\n -- Press 'c' to cancel the whole operation! -- ")

    # We check if the student already exist
    student_id = uv.get_valid_input(
        prompt_message="Enter Student ID of the student you want to update: ",
        validation_function=uv.validate_student_id,
        label="update",
        connection=connection
    )
    if student_id is None:
        return

    while (user_input := input(MENU_UPDATE_PROMPT)) != '7':

        if user_input == '1':
            first_name = uv.get_valid_input(
                prompt_message="Enter a new first name: ",
                validation_function=uv.validate_labels,
                container=updated_student_records,
                label="first_name",
                key="first_name"
            )
            if first_name is None:
                return

        elif user_input == '2':
            last_name = uv.get_valid_input(
                prompt_message="Enter a new last name: ",
                validation_function=uv.validate_labels,
                container=updated_student_records,
                label="last_name",
                key="last_name"
            )
            if last_name is None:
                return

        elif user_input == '3':
            age = uv.get_valid_input(
                prompt_message="Enter a new student age: ",
                validation_function=uv.validate_age,
                container=updated_student_records,
                key="age"
            )
            if age is None:
                return

        elif user_input == '4':
            grade = uv.get_valid_input(
                prompt_message="Enter a new student grade: ",
                validation_function=uv.validate_labels,
                container=updated_student_records,
                label="grade",
                key="grade"
            )
            if grade is None:
                return

        elif user_input == '5':
            enrol_date = uv.get_valid_input(
                prompt_message="""
                 Enter updated student's enrolled date in this format (dd-MM-YYYY). Press Enter to get default date: """
                .lstrip(),
                validation_function=uv.validate_enrolled_date,
                container=updated_student_records,
                key="enrol_date"
            )
            if enrol_date is None:
                return

        elif user_input == '6':
            # Get lessons that selected student enroll in
            enrolled_lessons = database.get_lesson_names_by_student_id(connection, student_id)
            select_done_idx = len(enrolled_lessons) + 1

            # Turn them into an input prompt for updating
            menu_update_lesson_names_prompt = create_menu_update_lesson_names_prompt(
                enrolled_lessons,
                select_done_idx
            )
            while True:
                selected_enrolled_lesson = uv.get_valid_input(
                    prompt_message=menu_update_lesson_names_prompt,
                    validation_function=uv.validate_selected_enrolled_lesson,
                    extra=select_done_idx
                )
                if selected_enrolled_lesson is None:
                    return

                # User is done with updating: Nothing left
                if selected_enrolled_lesson == select_done_idx:
                    break
                else:
                    old_lesson = enrolled_lessons[int(selected_enrolled_lesson) - 1][0]
                    new_lesson = uv.get_valid_input(
                        prompt_message=f"Update {old_lesson} with: ",
                        validation_function=uv.validate_labels,
                        container=updated_lesson_records,
                        label="lesson",
                        key=old_lesson
                    )
                    if new_lesson is None:
                        return

        elif um.cancel_operation(user_input):
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
        um.display_success_message("updated enrolled lessons")
    else:
        um.display_error_message("No lesson name have been updated!")


def prompt_delete_student(connection):
    print("\n -- Press 'c' to cancel the whole operation! -- ")

    student_id = uv.get_valid_input(
        prompt_message="Enter student ID You want to delete: ",
        validation_function=uv.validate_student_id,
        label="delete",
        connection=connection
    )
    if student_id is None:
        return

    database.delete_student(connection, student_id)
    um.display_success_message("deleted student")


def prompt_select_student(connection):
    print("\n -- Press 'c' to cancel the whole operation! --")

    student_id = uv.get_valid_input(
        prompt_message="Enter student ID You want to display: ",
        validation_function=uv.validate_student_id,
        label="select",
        connection=connection
    )
    if student_id is None:
        return

    # display the results
    student_infos = database.get_student_infos(connection, student_id)
    um.display_student_infos_table(student_infos)


# Generate a menu message based on lessons we've
def create_menu_update_lesson_names_prompt(lessons, select_done_idx):
    menu_lessons_prompt = "\n -- Choose which lesson you want to update. Press c to cancel! -- \n"

    # make it as a prompt
    for lesson_num in range(len(lessons)):
        lesson = f"{lessons[lesson_num]}".strip("( , ) ' .")
        menu_lessons_prompt += f"\n{lesson_num + 1}) {lesson}"

    menu_lessons_prompt += f"\n\n{select_done_idx}) I'm Done!" + "\n\nYour Selection: "
    return menu_lessons_prompt


menu()
