#Write a Python program that takes two numbers as input and performs the following operations: 
# addition, subtraction, multiplication, division, and modulus. Print the results of each operation in a clear format. 


num1= float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

addition =  num1 + num2
subtraction = num1 - num2
multiplication = num1 * num2

if num2 != 0:
  division = num1 / num2
  modulus = num1 % num2

else:
  division = "Error: Division by 0 not allowed"
  modulus = "Error: Modulus by 0 not allowed"

print("\nResults:")
print(f"{num1} + {num2} = {addition}")
print(f"{num1} - {num2} = {subtraction}")
print(f"{num1} * {num2} = {multiplication}")
print(f"{num1} / {num2} = {division}")
print(f"{num1} % {num2} = {modulus}")