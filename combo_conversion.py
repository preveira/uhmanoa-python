# Homework 5
import math

# Inputs
integer = int(input("Enter an integer: "))
flt = float(input("Enter a float: "))
string_input = input("Enter a string: ")

# Convert string to integer if possible
try:
    string_value = int(string_input)
    print("String converted to integer:", string_value)
except ValueError:
    print("String is not numeric, skipping conversion.")
    string_value = 0

# Multiply float and integer
result = flt * integer
print("Float * Integer =", result)

# Floor division & modulo with user-defined number
divisor = int(input("Enter another integer divisor: "))
print("Floor division:", result // divisor)
print("Modulo:", result % divisor)

# Cosine using math module
print("Cosine of result:", math.cos(result))
