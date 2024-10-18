# Define SimpleInterest directly
def SimpleInterest(principal, rate, time):
    return principal * rate * time / 100

# Define CompoundInterest directly
def CompoundInterest(principal, rate, time, compounds_per_year):
    return principal * (1 + (rate / (100 * compounds_per_year)))**(compounds_per_year * time) - principal

def main():
    # Ask user to choose between Simple Interest or Compound Interest
    print("Select Interest Calculation Type:")
    print("1. Simple Interest")
    print("2. Compound Interest")
    
    choice = input("Enter 1 for Simple Interest or 2 for Compound Interest: ")
    
    if choice == '1':
        # Get input for Simple Interest
        principal = float(input("Enter the principal amount: "))
        rate = float(input("Enter the annual interest rate (in %): "))
        time = float(input("Enter the time period (in years): "))
        
        # Calculate Simple Interest
        result = SimpleInterest(principal, rate, time)
        print(f"The Simple Interest is: {result}")
        
    elif choice == '2':
        # Get input for Compound Interest
        principal = float(input("Enter the principal amount: "))
        rate = float(input("Enter the annual interest rate (in %): "))
        time = float(input("Enter the time period (in years): "))
        compounds_per_year = int(input("Enter the number of times interest is compounded per year: "))
        
        # Calculate Compound Interest
        result = CompoundInterest(principal, rate, time, compounds_per_year)
        print(f"The Compound Interest is: {result}")
        
    else:
        print("Invalid choice. Please select 1 or 2.")

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
