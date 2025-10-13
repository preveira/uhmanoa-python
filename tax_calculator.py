income = float(input("Enter your income: "))
dependents = int(input("Enter the number of dependents: "))

if dependents < 0:
    print("Number of dependents cannot be negative.")
else:
    deduction = dependents * 2000
    taxable_income = income - deduction

    print(f"Income after deductions: ${taxable_income:,.0f}")

    if taxable_income < 10000:
        print("No tax owed")
    elif taxable_income <= 40000:
        tax = taxable_income * 0.10
        print(f"Your tax is: ${tax:,.0f}")
    elif taxable_income <= 100000:
        tax = taxable_income * 0.20
        print(f"Your tax is: ${tax:,.0f}")
    else:
        tax = taxable_income * 0.30
        print(f"Your tax is: ${tax:,.0f}")
