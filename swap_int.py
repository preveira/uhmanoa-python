# Take two integers from the user
a = int(input("Enter first number (a): "))
b = int(input("Enter second number (b): "))

# Swap without using a temporary variable
a, b = b, a

# Display formatted result
print(f"After swapping: a = {a}, b = {b}")
