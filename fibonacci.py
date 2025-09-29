# Homework 3
n = 100
divisor = int(input("Enter an integer divisor: "))


fib = [0, 1]
for i in range(2, n):
    fib.append(fib[-1] + fib[-2])


print(f"{'Fibonacci':>10} {'//':>5} {'%':>5}")
for num in fib:
    print(f"{num:10} {num // divisor:5} {num % divisor:5}")
