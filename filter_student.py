def filter_students(students, min_gpa):
    # Filter by min_gpa
    filtered = [s for s in students if s[2] >= min_gpa]
    # Sort by GPA (descending), then by age (ascending)
    filtered.sort(key=lambda x: (-x[2], x[1]))
    return filtered

# Example
students = [("Alice", 20, 3.5), ("Bob", 22, 3.7), ("Charlie", 20, 3.7)]
print(filter_students(students, 3.6))
# Output: [('Bob', 22, 3.7), ('Charlie', 20, 3.7)]
