import csv
import random

import id_generator

BASE_PATH = "../data"
DEFAULT_PATH = BASE_PATH + "/defaults"
FIRST_NAME_FILE = DEFAULT_PATH + "/first_names.txt"
LAST_NAME_FILE = DEFAULT_PATH + "/last_names.txt"
DEPARTMENT_FILE = DEFAULT_PATH + "/departments.txt"
HES_CSV_FILE = BASE_PATH + "/hes_data.csv"
MUSAADE_CSV_FILE = BASE_PATH + "/musaade_data.csv"


class Person:
    def __init__(self, national_id, first_name, last_name, department):
        self.national_id = national_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = "{}.{}@{}.com".format(first_name.lower(), last_name.lower(), "musaade")
        self.department = department
        self.active = random.choice([True, False])
        self.health_status = random.choice([True, False])

    def get_data_for_hes(self):
        return [self.national_id, self.first_name, self.last_name, self.health_status]

    def get_data_for_musaade(self):
        return [self.national_id, self.first_name, self.last_name, self.email, self.department, self.active]

    @staticmethod
    def get_hes_fields():
        return ["National ID", "First Name", "Last Name", "Health Status"]

    @staticmethod
    def get_musaade_fields():
        return ["National ID", "First Name", "Last Name", "Email", "Department", "Active"]


def generate(person_count: int = 200):
    ids = id_generator.generate(person_count)

    with open(FIRST_NAME_FILE, "r") as f:
        first_names = f.readlines()
        random.shuffle(first_names)

    with open(LAST_NAME_FILE, "r") as f:
        last_names = f.readlines()
        random.shuffle(last_names)

    with open(DEPARTMENT_FILE, "r") as f:
        departments = f.readlines()

    people = []
    for i in range(person_count):
        people.append(Person(
            ids[i],
            first_names[i].strip().lower().capitalize(),
            last_names[i].strip().lower().capitalize(),
            random.choice(departments).strip()
        ))

    with open(HES_CSV_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(Person.get_hes_fields())
        for person in people:
            writer.writerow(person.get_data_for_hes())

    with open(MUSAADE_CSV_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(Person.get_musaade_fields())
        for person in people:
            writer.writerow(person.get_data_for_musaade())


if __name__ == "__main__":
    try:
        generate()
        print("Done!")
    except Exception as error:
        print("Error occurred! Exception: {}".format(error))
