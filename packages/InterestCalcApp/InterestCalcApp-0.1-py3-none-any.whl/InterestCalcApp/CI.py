def CompoundInterest(principal, rate, time, compounds_per_year):
    amount = principal * (1 + rate / (compounds_per_year * 100)) ** (compounds_per_year * time)
    interest = amount - principal
    return interest
