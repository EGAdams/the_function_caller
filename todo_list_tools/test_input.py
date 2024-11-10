# test_input.py
try:
    user_input = input("Please enter something: ")
    print(f"You entered: {user_input}")
except EOFError:
    print("EOFError: No input available.")
