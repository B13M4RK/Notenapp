import json
import os
FILENAME = "data.json"

#Datei laden oder mit einem leeren Objekt starten, falls sie noch nicht existiert
if os.path.exists(FILENAME):
    with open(FILENAME, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)
else:
    json_data = {}

print("Geladene Daten:", json_data)

def add_subject():

    new_subject = input("\nSchreibe das Fach auf: ").strip()

    if not new_subject:
        print("Das Fach darf nicht lehr sein")
        return

    #Neues Fach als Schlüssel im Dictionary anlegen
    if new_subject not in json_data:
        json_data[new_subject] = {
            "gewichtung": [],
            "noten":[]
        }
    else:
        print(f"Das Fach {new_subject}existiert bereits")

    #Direkt in die Datei speichern
    with open(FILENAME, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

    print(f"Fach {new_subject} erfolgreich gespeichert")

    #Alle Fächer durchnummeriert ausgeben
    print("Aktuelle Fächer:")
    for iterator, subject in enumerate(json_data.keys(), start=1):
        print(f"{iterator}. {subject}")


def add_grade():
    pass

def ask_for_user_input():
    user_input = input("\nWas möchtest du tun\n1: Fach hinzufügen\n2:Note hinzufügen\n->")

    try:
        user_input = int(user_input)
        if user_input == 1:
            add_subject()
    except ValueError:
        print("\n!!! Das war keine gültige Zahl! Bitte gib Ziffern ein !!!")


while True:
    ask_for_user_input()