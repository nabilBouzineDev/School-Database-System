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
