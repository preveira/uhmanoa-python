import random

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Get first prime number
print("Please enter a prime number between 0 and 100.")
while True:
    first = int(input("Enter the first number: "))
    if 0 < first < 100 and is_prime(first):
        break
    print(f"{first} is not valid. Please enter a prime number between 0 and 100.")

# Get second prime number
print("Enter another prime number between 0 and 100.")
while True:
    second = int(input("Enter the second number: "))
    if 0 < second < 100 and is_prime(second):
        break
    print(f"{second} is not valid. Please enter a prime number between 0 and 100.")

# Random number
rand_num = random.randint(0, 200)
print(f"A random number between 0 and 200 has been chosen: {rand_num}")

# Check divisibility
div1 = rand_num % first == 0
div2 = rand_num % second == 0

if div1 and div2:
    print(f"{rand_num} is divisible by both {first} and {second}.")
elif div1:
    print(f"{rand_num} is divisible by {first} but not by {second}.")
elif div2:
    print(f"{rand_num} is divisible by {second} but not by {first}.")
else:
    print(f"{rand_num} is divisible by neither {first} nor {second}.")
