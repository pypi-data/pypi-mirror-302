from datetime import datetime

TRADITIONAL_YEAR_MONTH_LENGTHS = [
    (1, 31),
    (2, 28),
    (3, 31),
    (4, 30),
    (5, 31),
    (6, 30),
    (7, 31),
    (8, 31),
    (9, 30),
    (10, 31),
    (11, 30),
    (12, 31),
]

TRADITIONAL_LEAP_YEAR_MONTH_LENGTHS = [
    (1, 31),
    (2, 29),
    (3, 31),
    (4, 30),
    (5, 31),
    (6, 30),
    (7, 31),
    (8, 31),
    (9, 30),
    (10, 31),
    (11, 30),
    (12, 31),
]


def is_leap_year(year):
    if (year % 4) == 0 and (year % 100) != 0:
        return True
    elif (year % 400) == 0:
        return True
    return False


def convert_traditional_date_to_days(day, month, year):
    cumulative_days = 0
    month_lengths = (
        TRADITIONAL_LEAP_YEAR_MONTH_LENGTHS
        if is_leap_year(year)
        else TRADITIONAL_YEAR_MONTH_LENGTHS
    )

    # Finding the number of days in whole months which have passed
    for i in range(month - 1):
        cumulative_days += month_lengths[i][1]

    # Adding the remaining days
    cumulative_days += day

    return cumulative_days


def convert_standardized_date_to_days(day, month):
    days = (month - 1) * 30
    days += day

    return days


def convert_to_standardized_date(day_number, year):
    std_month = (day_number // 30) + 1
    std_day = day_number - ((std_month - 1) * 30)

    std_year = year - 2000

    return f"{std_day:02}/{std_month:02}/{std_year}"


def convert_to_traditional_date(day_number, year):
    month_lengths = (
        TRADITIONAL_LEAP_YEAR_MONTH_LENGTHS
        if is_leap_year(year)
        else TRADITIONAL_YEAR_MONTH_LENGTHS
    )

    traditional_month = 1
    for _, days in month_lengths:
        if day_number <= days:
            break
        day_number -= days
        traditional_month += 1

    traditional_day = day_number
    traditional_year = 2000 + year

    return f"{traditional_day:02}/{traditional_month:02}/{traditional_year}"


if __name__ == "__main__":
    action = input(
        "Select an action: \n1) Convert Traditional Date to Standardized Date\n2) Convert Standardized Date to Traditional Date\n3) Get Current Standardized Date\n\nSelction: "
    )
    if action == "1":
        traditional_day = int(input("\nEnter Traditional Day: "))
        traditional_month = int(input("Enter Traditional Month: "))
        traditional_year = int(input("Enter Traditional Year: "))
        print("\n****************")
        day_number = convert_traditional_date_to_days(
            traditional_day, traditional_month, traditional_year
        )
        print("Result: " + convert_to_standardized_date(day_number, traditional_year))
    elif action == "2":
        std_day = int(input("\nEnter Standardized Day: "))
        std_month = int(input("Enter Standardized Month: "))
        std_year = int(input("Enter Standardized Year: "))
        print("\n******************")
        day_number = convert_standardized_date_to_days(std_day, std_month)
        print("Result: " + convert_to_traditional_date(day_number, std_year))
    elif action == "3":
        current_day = int(datetime.today().strftime("%d"))
        current_month = int(datetime.today().strftime("%m"))
        current_year = int(datetime.today().strftime("%Y"))
        print("\n***********************************")
        day_number = convert_traditional_date_to_days(
            current_day, current_month, current_year
        )
        print(
            "Current Standardized Date: "
            + convert_to_standardized_date(day_number, current_year)
        )
