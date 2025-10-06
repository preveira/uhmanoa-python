def count_vowels(s):
    vowels = "aeiou"
    count = 0
    for char in s.lower():  # make lowercase to handle both upper and lower
        if char in vowels:
            count += 1
    return count

# Example
print(count_vowels("Python Programming"))  # Output: 4
