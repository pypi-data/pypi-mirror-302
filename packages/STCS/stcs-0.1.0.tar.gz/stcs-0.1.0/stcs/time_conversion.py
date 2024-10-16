from datetime import datetime


def convert_to_standardized_time(
    traditional_hours, traditional_minutes, traditional_seconds
):
    std_hours = traditional_hours // 2.4  # Converting to standardized hours
    traditional_minutes += (
        traditional_hours % 2.4
    ) * 60  # Adding the remaining time to the minutes after converting them

    std_minutes = traditional_minutes // 1.44  # Converting to standardized minutes
    traditional_seconds += (
        traditional_minutes % 1.44
    ) * 60  # Adding the remaining time to the seconds after converting them

    std_seconds = traditional_seconds / 0.864  # Converting to standardized seconds

    if std_seconds > 99:
        std_minutes += 1
        std_seconds -= 100
    if std_minutes > 99:
        std_hours += 1
        std_minutes -= 100

    return f"{int(std_hours):02}:{int(std_minutes):02}:{int(std_seconds):02}"


def convert_to_traditional_time(std_hours, std_minutes, std_seconds):
    total_traditional_seconds = (
        ((std_hours * 2.4) * 3600) + ((std_minutes * 1.44) * 60) + (std_seconds * 0.864)
    )  # Converting the standardized time to traditional seconds for conversion

    traditional_hours = total_traditional_seconds / 3600
    total_traditional_seconds %= 3600  # Reducing the remaining seconds

    traditional_minutes = total_traditional_seconds / 60
    total_traditional_seconds %= 60  # Reducing the remaining seconds

    traditional_seconds = total_traditional_seconds

    return f"{int(traditional_hours):02}:{int(traditional_minutes):02}:{int(traditional_seconds):02}"


if __name__ == "__main__":
    action = input(
        "Select an action: \n1) Convert Traditional Time to Standardized Time\n2) Convert Standardized Time to Traditional Time\n3) Get Current Standardized Time\n\nSelction: "
    )
    if action == "1":
        traditional_hours = int(input("\nEnter Traditional Hours: "))
        traditional_minutes = int(input("Enter Traditional Minutes: "))
        traditional_seconds = int(input("Enter Traditional Seconds: "))
        print("\n*******************")
        print(
            "Result: "
            + convert_to_standardized_time(
                traditional_hours, traditional_minutes, traditional_seconds
            )
        )
    elif action == "2":
        std_hours = int(input("\nEnter Standardized Hours: "))
        std_minutes = int(input("Enter Standardized Minutes: "))
        std_seconds = int(input("Enter Standardized Seconds: "))
        print("\n*******************")
        print(
            "Result: "
            + convert_to_traditional_time(std_hours, std_minutes, std_seconds)
        )
    elif action == "3":
        current_hour = int(datetime.today().strftime("%H"))
        current_minute = int(datetime.today().strftime("%M"))
        current_second = int(datetime.today().strftime("%S"))
        print("\n**************************************")
        print(
            "Current Standardized Time: "
            + convert_to_standardized_time(current_hour, current_minute, current_second)
        )
