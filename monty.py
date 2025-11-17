import random

choice = input("Stay(1) or Switch(2) for this round")
prize = 1
for i in range(0, 20):
  doors = [0,0,0]
  doors[random.randint(0,2)] = 1
  print(doors)
  selection = random.randint(0,2)
  print(selection)
  for i in range(3):
    if doors[i] == 1:
      prize = i