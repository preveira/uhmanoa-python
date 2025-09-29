# Homework 1
data = ["10", 5, 3.5, "20", 7]

total = 0
for item in data:
    if isinstance(item, str) and item.isdigit():
        total += int(item)
    elif isinstance(item, (int, float)):
        total += item

print("Sum of numbers:", total)
