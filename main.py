import datetime
import json

# Load Subjects from JSON
try:
    with open("data_subjects.json", "r") as file:
        content = file.read().strip()
        if not content:
            data_subjects = {}
        else:
            data_subjects = json.loads(content)
except (FileNotFoundError, json.JSONDecodeError):
    data_subjects = {}

# Load Grades from JSON
try:
    with open("data_grades.json", "r") as file:
        content = file.read().strip()
        if not content:
            data_grades = {}
        else:
            data_grades = json.loads(content)
except (FileNotFoundError, json.JSONDecodeError):
    data_grades = {}

# Load Grade_averages from JSON
try:
    with open("data_average_grades.json", "r") as file:
        content = file.read().strip()
        if not content:
            data_averages = {}
        else: data_averages = json.loads(content)
except (FileNotFoundError, json.JSONDecodeError):
    data_averages = {}

print("Geladene Fächer: ", data_subjects)
print("Geladene Noten: ", data_grades)
print("Geladene Durchschnittsnoten", data_averages)

type_of_grades = [
    "oral",
    "written",
    "vocabulary-test",
    "sportif",
    "art-project"
]
#grades_list = set()

def calculate_average_grades(selected_code, grade_type, points):

    # 1. Get Sum of all points and count of grades of the same type
    sum_points = 0
    grades_count = 0
    for  grade in data_grades[selected_code]:
        if grade["type"] == grade_type:
            sum_points = sum_points + int(grade["points"])
            grades_count = grades_count + 1

    # 3. Calculate average
    average = sum_points / grades_count

    # 4. Create new average JSON format
    data_averages[selected_code] = {
        "average":average
    }

    # 5. Overwrite old average grade from subject with new average
    with open("data_average_grades.json", "w") as file:
        json.dump(data_averages, file, indent=4)

def add_subject():
    # 1. Define new subject
    new_subject_name = input("\nSchreibe das Fach auf: ").strip()
    new_code = input("Schreibe den Kürzel des Faches auf-ABC").strip().upper()
    new_oral = float(input("Schreibe einen mündlichen Wert zwischen 0 und eins auf"))
    new_written = float(input("Schreibe einen schriftlichen Wert zwischen 0 und eins auf"))

    # 2. Add new subject to existing Data_subjects
    data_subjects[new_subject_name] = {
        "key": new_code,
        "ORA": new_oral,
        "WRI": new_written
    }

    # 3. Write whole new subject into JSON file
    with open("data_subjects.json", "w") as file:
        json.dump(data_subjects, file, indent=4)

    # 4. Print out new subject
    print(f"\nFach '{new_subject_name}' ({new_code}) wurde hinzugefügt – mündlich: {new_oral}, schriftlich: {new_written}")

def add_grade():
    try:
        # Try if subjects exist
        if not data_subjects:
            print("\nEs sind noch keine Fächer vorhanden! Füge zuerst eins hinzu")
            return

        # 1. Get data from json as a list to get their index
        subject_names = list(data_subjects.keys())

        # 2. Print out all subjects
        print("\nVerfügbare Fächer:")
        for count, name in enumerate(subject_names, start=0):
            print(f"{count}. {name}")

        # 3. Select subject
        user_input = int(input(f"\nWähle die Nummer des Faches: "))
        selected_name = subject_names[user_input]
        selected_code = data_subjects[selected_name]["key"]

        # 4. Select type of grade
        print("\nNotenarten:")
        for count, t in enumerate(type_of_grades, start=0):
            print(f"{count}. {t}")
        type_input = int((input(f"\nSchreibe die Art auf: ")))
        grade_type = type_of_grades[type_input]

        # 5. Type in your points
        points = int((input(f"\nSchreibe deine Punktzahl auf: ")))

        # 6. Get daytime
        date = str(datetime.date.today())
        #print(date)

        # 7. Load grade into data_grades
        # check if subject is already in grades list
        if selected_code not in data_grades:
            data_grades[selected_code] = []

        data_grades[selected_code].append({
            "type":grade_type,
            "points":points,
            "date":date,
        })
        #grades_list.add(f"{selected_code}_{grade_type}_{points}_{date}")

        # 8. Write whole grade into JSON file
        with open("data_grades.json", "w") as file:
            json.dump(data_grades, file, indent=4)

        # 9. Calculate average grade
        calculate_average_grades(selected_code, grade_type, points)

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
        else:
            print("\nBitte wähle eine Zahl von oben")
    except ValueError:
        print("\n!!! Das war keine gültige Zahl! Bitte gib Ziffern ein !!!")


while True:
    ask_for_user_input()