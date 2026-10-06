import datetime
import json

# Load JSON from a file
try:
    with open("data.json", "r") as file:
        data = json.load(file)
except FileNotFoundError:
    data = {}

"Acces JSON Data"
print("Geladene Daten: ", data)

type_of_grades = [
    "ORA",
    "WRI",
]
grades_list = set()

def recalculate_grades_and_averages():
    pass

def add_subject():
    # 1. Define new subject
    new_subject_name = input("\nSchreibe das Fach auf: ").strip()
    new_code = input("Schreibe den Kürzel des Faches auf-ABC").strip().upper()
    new_oral = float(input("Schreibe einen mündlichen Wert zwischen 0 und eins auf"))
    new_written = float(input("Schreibe einen schriftlichen Wert zwischen 0 und eins auf"))

    # 2. Add new subject to existing Data
    data[new_subject_name] = {
        "key": new_code,
        "ORA": new_oral,
        "WRI": new_written
    }

    # 3. Write whole Data into JSON file
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

    # 4. Print out new subject
    print(f"\nFach '{new_subject_name}' ({new_code}) wurde hinzugefügt – mündlich: {new_oral}, schriftlich: {new_written}")

def add_grade():
    try:
        # Try if subjects exist
        if not data:
            print("\nEs sind noch keine Fächer vorhanden! Füge zuerst eins hinzu")
            return

        # 1. Get data from json as a list to get their index
        subject_names = list(data.keys())

        # 2. Print out all subjects
        print("\nVerfügbare Fächer:")
        for count, name in enumerate(subject_names, start=0):
            print(f"{count}. {name}")

        # 3. Select subject
        user_input = int(input(f"\nWähle die Nummer des Faches: "))
        selected_name = subject_names[user_input]
        selected_code = data[selected_name]["key"]

        # 4. Select type of grade
        print("\nNotenarten:")
        for count, t in enumerate(type_of_grades, start=0):
            print(f"{count}. {t}")
        type_input = int((input(f"\nSchreibe die Art auf: ")))
        grade_type = type_of_grades[type_input]

        # 5. Type in your points
        points = int((input(f"\nSchreibe deine Punktzahl auf: ")))

        # 6. Get daytime
        date = datetime.date.today()

        # 7. Add grades to grades list
        # Key_gradeType_Points_Date
        grades_list.add(f"{selected_code}_{grade_type}_{points}_{date}")

        # 8. Print out grades list
        print(grades_list)

    except ValueError:
        print("\n!!! Das war keine gültige Zahl! Bitte gib Ziffern ein !!!")
    except IndexError:
        print("\n!!! Diese Nummer existiert nicht in der Auswahl! !!!")

def ask_for_user_input():
    try:
        user_input = int(input("\nWas möchtest du tun\n1: Fach hinzufügen\n2:Note hinzufügen\n->"))
        if user_input == 1:
            add_subject()
        elif user_input == 2:
            add_grade()
        elif user_input == 3:
            recalculate_grades_and_averages()
        else:
            print("\nBitte wähle eine Zahl von oben")
    except ValueError:
        print("\n!!! Das war keine gültige Zahl! Bitte gib Ziffern ein !!!")


while True:
    ask_for_user_input()
