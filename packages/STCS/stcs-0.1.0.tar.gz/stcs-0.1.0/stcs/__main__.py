from datetime import datetime

import typer

from stcs import __app_name__, cli, date_conversion, time_conversion

conv_app = typer.Typer(help="Converts between STCS and traditional times and dates")
cli.app.add_typer(conv_app, name="conv")


def main():
    cli.app(prog_name=__app_name__)


@cli.app.command()
def time():
    """
    Gives the current time in STCS format and exits
    """
    current_hour = int(datetime.today().strftime("%H"))
    current_minute = int(datetime.today().strftime("%M"))
    current_second = int(datetime.today().strftime("%S"))
    print(
        f"{time_conversion.convert_to_standardized_time(current_hour, current_minute, current_second)} STDZ"
    )


@cli.app.command()
def date():
    """
    Gives the current date in STCS format and exits
    """
    current_day = int(datetime.today().strftime("%d"))
    current_month = int(datetime.today().strftime("%m"))
    current_year = int(datetime.today().strftime("%Y"))
    day_number = date_conversion.convert_traditional_date_to_days(
        current_day, current_month, current_year
    )
    print(
        f"{date_conversion.convert_to_standardized_date(day_number, current_year)} STDZ"
    )


@cli.app.command()
def now():
    """
    Gives the current time and date in STCS format and exits
    """
    current_hour = int(datetime.today().strftime("%H"))
    current_minute = int(datetime.today().strftime("%M"))
    current_second = int(datetime.today().strftime("%S"))

    current_day = int(datetime.today().strftime("%d"))
    current_month = int(datetime.today().strftime("%m"))
    current_year = int(datetime.today().strftime("%Y"))
    day_number = date_conversion.convert_traditional_date_to_days(
        current_day, current_month, current_year
    )

    print(
        f"{date_conversion.convert_to_standardized_date(day_number, current_year)} {time_conversion.convert_to_standardized_time(current_hour, current_minute, current_second)} STDZ"
    )


@conv_app.command("time")
def conv_time(
    time: str,
    from_stdz: bool = typer.Option(False, "--from-stdz"),
    from_traditional: bool = typer.Option(False, "--from-traditional"),
):
    """
    Converts a timestamp in the HH:MM:SS format from traditional time to STCS time or vice versa
    """
    if from_traditional:
        timestamp = time.split(":")
        traditional_hours = int(timestamp[0])
        traditional_minutes = int(timestamp[1])
        traditional_seconds = int(timestamp[2])
        print(
            f"{time_conversion.convert_to_standardized_time(traditional_hours, traditional_minutes, traditional_seconds)} STDZ"
        )
    else:
        timestamp = time.split(":")
        stdz_hours = int(timestamp[0])
        stdz_minutes = int(timestamp[1])
        stdz_seconds = int(timestamp[2])
        print(
            time_conversion.convert_to_traditional_time(
                stdz_hours, stdz_minutes, stdz_seconds
            )
        )


@conv_app.command("date")
def conv_date(
    date: str,
    from_stdz: bool = typer.Option(False, "--from-stdz"),
    from_traditional: bool = typer.Option(False, "--from-traditional"),
):
    """
    Converts a datestamp in the DD/MM/YYYY format from traditional dates to STCS dates or vice versa
    """
    if from_traditional:
        datestamp = date.split("/")
        traditional_day = int(datestamp[0])
        traditional_month = int(datestamp[1])
        traditional_year = int(datestamp[2])
        day_number = date_conversion.convert_traditional_date_to_days(
            traditional_day, traditional_month, traditional_year
        )
        print(
            f"{date_conversion.convert_to_standardized_date(day_number, traditional_year)} STDZ"
        )
    else:
        datestamp = date.split("/")
        stdz_day = int(datestamp[0])
        stdz_month = int(datestamp[1])
        stdz_year = int(datestamp[2])
        day_number = date_conversion.convert_standardized_date_to_days(
            stdz_day, stdz_month
        )
        print(date_conversion.convert_to_traditional_date(day_number, stdz_year))


if __name__ == "__main__":
    main()
