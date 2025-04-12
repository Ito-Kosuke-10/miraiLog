from datetime import datetime

def estimate_lifespan(gender):
    return 81 if gender == "男性" else 87

def calculate_remaining_life(birthdate_str, lifespan_years):
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
    death_year = birthdate.year + lifespan_years
    death_date = datetime(death_year, birthdate.month, birthdate.day)
    today = datetime.today()
    remaining_days = (death_date - today).days
    return remaining_days
