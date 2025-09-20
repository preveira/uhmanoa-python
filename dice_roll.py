import random

total = 0
while total < 20:
  ask = input("Roll dice? y/n")
  roll = random.randint(1,6)
  total += roll
  print(f"You rolled a {roll}, Total is now {total}")
print(f"Game Over, Final Total: {total}")