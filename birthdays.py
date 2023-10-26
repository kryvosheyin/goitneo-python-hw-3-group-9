from datetime import datetime, timedelta
from collections import defaultdict


def get_upcoming_birthdays(users):
    today = datetime.now().date()
    next_week_date = today + timedelta(days=7)

    upcoming_birthdays = defaultdict(list)

    for user in users:
        if user.birthday is None:
            continue
        birthday_this_year = user.birthday.as_datetime().replace(year=today.year)
        upcoming_date = (
            birthday_this_year
            if birthday_this_year >= today
            else user.birthday.as_datetime().replace(year=today.year + 1)
        )

        if upcoming_date.weekday() >= 5:
            upcoming_date += timedelta(days=(7 - upcoming_date.weekday()))

        if today < upcoming_date <= next_week_date:
            upcoming_birthdays[upcoming_date].append(str(user.name))

    sorted_days = sorted(upcoming_birthdays)

    print("Upcoming birthdays:")

    if len(upcoming_birthdays) == 0:
        print("There are no upcoming birthdays within next week time period")

    for day in sorted_days:
        if day in upcoming_birthdays:
            print(f"{day.strftime('%A')}: {', '.join(upcoming_birthdays[day])}")
