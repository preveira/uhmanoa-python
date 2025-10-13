scores = []
print('Please enter a test score (Enter "done" when finished):')

count = 1
while True:
    val = input(f"Enter score {count}: ")
    if val.lower() == "done":
        break
    scores.append(float(val))
    count += 1

print("Calculating results...")

avg = sum(scores) / len(scores)
print(f"Average score: {avg:.2f}")
print("Passing grade:", "Yes" if avg >= 70 else "No")

statuses = []
for i, s in enumerate(scores, 1):
    diff = s - avg
    status = ""
    if diff > 10:
        status = f"Score {i} is more than 10 points above the average"
    elif diff < -10:
        status = f"Score {i} is more than 10 points below the average"
    else:
        status = f"Score {i} is within 10 points of the average"
    statuses.append(status)

    direction = "above" if diff > 0 else "below"
    print(f"Score {i}: {diff:+.2f} {direction} average")

print("Score status:", ", ".join(statuses) + ".")
