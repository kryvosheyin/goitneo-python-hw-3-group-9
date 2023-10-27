from datetime import datetime
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            self.value = value
        else:
            raise ValueError("Invalid phone number format.")


class Birthday(Field):
    def __init__(self, year, month, day):
        self.validate(year, month, day)
        self.year = year
        self.month = month
        self.day = day
        super().__init__(datetime(year, month, day).date())

    @staticmethod
    def validate(year, month, day):
        if month < 1 or month > 12:
            raise ValueError("Invalid month. Must be between 1 and 12 inclusive.")

        if day < 1 or day > 31:
            raise ValueError("Invalid day. Must be between 1 and 31 inclusive.")

        if month in [4, 6, 9, 11] and day == 31:
            raise ValueError(f"Invalid day for month {month}.")

        if month == 2:
            if Birthday.is_leap_year(year) and day > 29:
                raise ValueError(f"Invalid day for February in a leap year.")
            elif not Birthday.is_leap_year(year) and day > 28:
                raise ValueError(f"Invalid day for February in a non-leap year.")

    @staticmethod
    def is_leap_year(year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def as_datetime(self):
        return self.value

    def __str__(self):
        return self.value.strftime("%d %B %Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, year, month, day):
        self.birthday = Birthday(year, month, day)

    def edit_phone(self, new_phone):
        if len(self.phones) > 1:
            response = input(
                f"There is more than one phone saved for {self.name}:\n{self.get_phones()}\nPlease pick position of the number to change: "
            )
            try:
                self.phones[int(response) - 1] = Phone(new_phone)
            except IndexError:
                raise IndexError("The number provided is not valid, please try again")
        else:
            self.phones.clear()
            self.phones.append(Phone(new_phone))

    def remove_phone(self):
        self.phones.clear()
        return self.phones

    def get_phones(self):
        if len(self.phones) == 0:
            return f"There are no phones saved for {self.name}"
        return "\n".join(
            f"{index+1}. {phone.value}" for index, phone in enumerate(self.phones)
        )

    def __str__(self):
        birthday_str = str(self.birthday) if self.birthday else "Not set"
        return f"Contact name: {self.name.value}, phones: {';' .join(p.value for p in self.phones)}, birthday: {birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, record_name):
        contact = self.data.get(record_name)
        if contact is None:
            raise KeyError(f"Contact {record_name} is not found")
        return contact

    def delete(self, record_name):
        self.data.pop(record_name, None)
