from tabulate import tabulate


def cancel_operation(input_value):
    if input_value.lower() == 'c':
        print("\n -- Operation Canceled! -- ")
    return input_value.lower() == 'c'


# Name: Functions with syntax like [display_state_message()]
# Goal: Used to show helpful messages for the user.
def display_error_message(error):
    print(f"\n{error}")


def display_success_message(message):
    print("\n You've " + message + " successfully!")


def display_student_infos_table(student_infos):
    # turn tuple as a list
    student_list_infos = list(student_infos)

    table_headers = ["student ID", "first name", "last name", "age", "grade", "enrollment's date", "enrolled lessons"]
    table_data = [student_list_infos]

    # make enrolled lessons on separate lines
    enrolled_lessons = student_list_infos[-1]
    student_list_infos[-1] = f",{enrolled_lessons}".replace(",", "\n--> ")

    table = tabulate(table_data, headers=table_headers, tablefmt="rounded_grid")
    print()
    print(table)
