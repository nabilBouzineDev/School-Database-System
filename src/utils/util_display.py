from tabulate import tabulate


def cancel_operation(input_value):
    input_str = str(input_value)
    if input_str.lower() == 'c':
        print("\n -- Operation Canceled! -- ")
    return input_str.lower() == 'c'


# Name: Functions with syntax like [display_state_message()]
# Goal: Used to show helpful messages for the user.
def display_error_message(error):
    print(f"\n{error}")


def display_success_message(message):
    print("\nYou've " + message + " successfully!")


def display_student_infos_table(student_infos):
    # turn tuple as a list
    student_list_infos = list(student_infos)

    table_headers = ["student ID", "first name", "last name", "age", "grade", "enrollment's date", "enrolled lessons"]
    table_data = [student_list_infos]

    # make enrolled lessons on separate lines
    student_list_infos[-1] = f",{student_list_infos[-1]}".replace(",", "\n--> ")

    table = tabulate(table_data, headers=table_headers, tablefmt="rounded_grid")
    print()
    print(table)
