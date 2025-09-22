def fahrenheit_to_celsius_chart(low, high):
    print("Fahrenheit | Celsius")
    print("--------------------")
    for f in range(low, high + 1, 5):
        c = (f - 32) * 5/9
        print(f"{f:10} | {c:7.2f}")


low = int(input("Enter the low Fahrenheit value: "))
high = int(input("Enter the high Fahrenheit value: "))

fahrenheit_to_celsius_chart(low, high)
