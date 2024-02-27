import math, os

def get_temp_folder():
    return os.path.join(os.getcwd(), 'temp')

def round_to_nearest_multiple_of_6(number):
    return math.ceil(number / 6) * 6

def get_request_number(file_path=os.path.join(get_temp_folder(), 'request_counter.txt')):
    # Check if the file exists
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            # Initialize the counter if the file doesn't exist
            file.write('1')
            return 1

    # Read the counter value from the file
    with open(file_path, 'r+') as file:
        counter = int(file.read())
        return counter

def increment_request_number(file_path=os.path.join(get_temp_folder(), 'request_counter.txt')):
    # Read the current counter value
    counter = get_request_number(file_path)
    
    # Increment the counter
    counter += 1
    
    # Write the updated counter value back to the file
    with open(file_path, 'w') as file:
        file.write(str(counter))
    
    return counter

