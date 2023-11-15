def try_convert_to_int(s):
    return int(s)

def try_convert_to_float(s):
    return float(s)

def handle_input(user_input):
    # Fill this in with your application code
    # Here is an example
    print(f"Processing Input: {user_input}")

def handle_input_2(user_input):
    conversion_functions = [try_convert_to_int, try_convert_to_float]

    for func in conversion_functions:
        try:
            result = func(user_input)
            print(f"Conversion successful: {result}")
            break
        except ValueError as e:
            print(f"Conversion using {func.__name__} failed: {e}")

while True:
    user_input = input("Please Enter an Input (q to quit): ")
    if user_input.lower() == 'q':
        print("Quitting...")
        break
    handle_input_2(user_input)

