from collections import UserDict
from datetime import datetime, timedelta
class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value):
        pass

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def validate(self, value):
        if not(isinstance(value, str) and value.isdigit() and len(value) == 10):
            raise ValueError('Invalid phone number')

class Birthday(Field):
    def validate(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError('Invalid birthday format. Use YYYY-MM-DD')

class Record(Field):
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [num for num in self.phones if num.value != phone]

    def edit_phone(self, old_phone, new_phone):
        found = False
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                found = True
                break

        if not found:
            raise ValueError(f"Phone number '{old_phone}' not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days_remaining = (next_birthday - today).days
            return days_remaining

    def __str__(self):
        return f'Contact name: {self.name.value}, phones: {",".join(p.value for p in self.phones)}'

class AddressBook(UserDict):
    def add_record(self, record):
       self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, batch_size=1):
        keys = list(self.data.keys())
        for i in range(0, len(keys), batch_size):
            yield [self.data[key] for key in keys[i:i + batch_size]]

