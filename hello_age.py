# Get user input
first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")

# Validate age input
while True:
    try:
        age = int(input("Enter your age: "))
        if 0 <= age <= 120:
            break
        else:
            print("Please enter a valid age between 0 and 120.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Store info in a tuple
person = (first_name, last_name, age)

# Display formatted message
print(f"Hello, {person[0]} {person[1]}! You are {person[2]} years old.")
