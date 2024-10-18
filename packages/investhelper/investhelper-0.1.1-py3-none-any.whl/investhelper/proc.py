def calculate_profit(income, expenses):
    return income - expenses

def calculate_roi(income,expenses):
    return (calculate_profit(income,expenses) / expenses) * 100
