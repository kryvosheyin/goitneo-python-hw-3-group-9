from fields import Record, AddressBook
from birthdays import get_upcoming_birthdays
import pickle


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError, IndexError) as e:
            return str(e)

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args: list, book: AddressBook):
    name, phone = extract_args(args)
    contact = Record(name)
    contact.add_phone(phone)
    book.add_record(contact)
    return f"Contact {name} was added"


@input_error
def add_phone(args: list, book: AddressBook):
    name, phone = extract_args(args)
    contact = book.find(name)
    contact.add_phone(phone)
    return f"Phone {phone} added to contact {contact.name}"


@input_error
def change_contact(args: list, book: AddressBook):
    name, phone = extract_args(args)
    contact = book.find(name)
    contact.edit_phone(phone)
    return f"Contact {contact.name} was updated with {phone}"


@input_error
def remove_phone(args: list, book: AddressBook):
    contact_name = extract_name(args)
    contact = book.find(contact_name)
    contact.remove_phone()
    return f"All phone numbers for {contact.name} were removed"


@input_error
def get_phone(args: list, book: AddressBook):
    contact_name = extract_name(args)
    contact = book.find(contact_name)
    return contact.get_phones()


@input_error
def add_birthday(args: list, book: AddressBook):
    try:
        contact_name, date_of_birth = args
        day, month, year = date_of_birth.split(".")
    except ValueError:
        raise ValueError("Please provide name and date of birth in format DD.MM.YYY")
    contact = book.find(contact_name)
    contact.add_birthday(int(year), int(month), int(day))
    return f"{contact.name}'s birthday was added to the Address book"


@input_error
def show_birthday(args: list, book: AddressBook):
    contact_name = extract_name(args)
    contact = book.find(contact_name)
    if contact.birthday is None:
        return f"{contact.name} does not have birthday saved in the Address book"
    return contact.birthday


def print_contacts(_, book: AddressBook):
    print("\nHere are all contacts in the Address Book:\n")
    for contact, contact_info in book.data.items():
        print(contact_info)


def get_birthdays(_, book: AddressBook):
    return get_upcoming_birthdays(book.data.values())


def print_hello(_, __):
    return "How can I help you?"


def parse_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()


def print_help_message(_, __):
    with open("commands_helper.txt", "r") as file:
        lines = file.readlines()
    print("{:<20} {:<40} {:<}".format("Command", "Description", "Action"))
    for line in lines:
        command, description, action = line.strip().split("|")
        print("{:<20} {:<40} {:<}".format(command, description, action))


def extract_name(args: list):
    try:
        return args[0]
    except IndexError:
        raise IndexError("Please provide contact name")


def extract_args(args: list):
    try:
        name, phone = args
    except ValueError:
        raise ValueError("Please provide name and phone")
    return name, phone


def save_to_file(book: AddressBook, filename: str = "address_book.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)
    return f"Address book was saved to {filename}"


def load_from_file(filename: str = "address_book.pkl") -> AddressBook:
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        print("Saved contacts not found. Creating new Address Book")
        return AddressBook()


def main():
    book = load_from_file()
    COMMANDS = {
        "help": print_help_message,
        "hello": print_hello,
        "add": add_contact,
        "add-phone": add_phone,
        "change": change_contact,
        "phone": get_phone,
        "all": print_contacts,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": get_birthdays,
        "delete-phone": remove_phone,
    }

    print("Welome to the assistant bot!\n")
    while True:
        user_input = input("Enter the command: ").strip().lower()
        command, *args = parse_input(user_input)

        if command in ["close", "exit", "goodbye"]:
            print("Saving contacts..")
            save_to_file(book)
            print("Goodbye!")
            break
        elif command in COMMANDS:
            result = COMMANDS[command](args, book)
            if result:
                print(result)
        else:
            print("Invalid command")


if __name__ == "__main__":
    main()
