# -*- coding: utf-8 -*-

import sys
import datetime
import json
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QTreeWidget, QTreeWidgetItem, QComboBox, \
    QHBoxLayout, QLabel, QVBoxLayout, QWidget

# Globale Variablen sauber initialisieren
data_subjects = {}
data_grades = {}
data_averages = {}


class UiMainWindow(object):
    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(850, 650)
        self.centralwidget = QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")

        # Hauptlayout (Vertical) für obere Steuerungsleiste und Tabelle
        self.main_layout = QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)

        # Obergruppe für Quartals-/Halbjahres-Auswahl
        self.top_bar_layout = QHBoxLayout()
        self.label_quarter = QLabel("Aktuelles Halbjahr / Quartal:", self.centralwidget)
        self.label_quarter.setStyleSheet("font-weight: bold; color: #2c3e50;")

        self.combo_quarter = QComboBox(self.centralwidget)
        self.combo_quarter.addItems(["Q1", "Q2", "Q3", "Q4"])
        self.combo_quarter.setStyleSheet(
            "padding: 4px; font-weight: bold; background-color: white; border: 1px solid #dcdcdc; border-radius: 4px;")

        self.top_bar_layout.addWidget(self.label_quarter)
        self.top_bar_layout.addWidget(self.combo_quarter)
        self.top_bar_layout.addStretch()

        self.main_layout.addLayout(self.top_bar_layout)

        # TreeWidget für die Notenansicht
        self.treeWidget = QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.setColumnCount(4)
        self.treeWidget.setHeaderLabels(["Fach / Notenart", "Punkte", "Datum", "Durchschnitt (M / S / Ges)"])
        self.treeWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setRootIsDecorated(True)
        self.treeWidget.setIndentation(25)

        self.treeWidget.setStyleSheet("""
            QTreeWidget {
                background-color: #fcfcfc;
                alternate-background-color: #f4f6f9;
                border: 1px solid #dcdcdc;
                border-radius: 8px;
                font-size: 13px;
                color: #2c3e50;
            }
            QTreeWidget::item {
                padding: 6px 4px;
                border-bottom: 1px solid #eaeaea;
            }
            QTreeWidget::item:selected {
                background-color: #3498db;
                color: white;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
        """)

        self.main_layout.addWidget(self.treeWidget)

        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 850, 22))
        self.menubar.setObjectName("menubar")
        self.menu_datei = QtWidgets.QMenu(self.menubar)
        self.menu_datei.setObjectName("menuDatei")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        # Aktionen
        self.action_fach_hinzufuegen = QtWidgets.QAction(main_window)
        self.action_fach_hinzufuegen.setObjectName("actionFach_hinzufuegen")
        self.action_fach_loeschen = QtWidgets.QAction(main_window)
        self.action_fach_loeschen.setObjectName("actionFach_loeschen")
        self.action_note_hinzufuegen = QtWidgets.QAction(main_window)
        self.action_note_hinzufuegen.setObjectName("actionNote_hinzuf_gen")
        self.action_note_loeschen = QtWidgets.QAction(main_window)
        self.action_note_loeschen.setObjectName("actionNote_loeschen")

        self.menu_datei.addAction(self.action_fach_hinzufuegen)
        self.menu_datei.addAction(self.action_fach_loeschen)
        self.menu_datei.addSeparator()
        self.menu_datei.addAction(self.action_note_hinzufuegen)
        self.menu_datei.addAction(self.action_note_loeschen)
        self.menubar.addAction(self.menu_datei.menuAction())

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "Notenrechner - Abitur"))
        self.menu_datei.setTitle(_translate("MainWindow", "Datei"))
        self.action_fach_hinzufuegen.setText(_translate("MainWindow", "Fach hinzufügen"))
        self.action_fach_loeschen.setText(_translate("MainWindow", "Fach löschen"))
        self.action_note_hinzufuegen.setText(_translate("MainWindow", "Note hinzufügen"))
        self.action_note_loeschen.setText(_translate("MainWindow", "Note löschen"))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = UiMainWindow()
        self.ui.setup_ui(self)

        # Kompatibilitäts-Brücke für alle treeWidget-Aufrufe
        self.treeWidget = self.ui.treeWidget

        # --- TASCHENRECHNER ICON & TASKLEISTEN-FIX ---
        app_icon = QtGui.QIcon.fromTheme("accessories-calculator")
        if app_icon.isNull():
            app_icon = QtGui.QIcon.fromTheme("calc")

        if not app_icon.isNull():
            self.setWindowIcon(app_icon)
        # ---------------------------------------------

        # JSON-Daten und Einstellungen laden
        self.load_data()
        self.load_settings()

        # Menü-Aktionen verknüpfen
        self.ui.action_fach_hinzufuegen.triggered.connect(self.add_subject_gui)
        self.ui.action_fach_loeschen.triggered.connect(self.delete_subject_gui)
        self.ui.action_note_hinzufuegen.triggered.connect(self.add_grade_gui)
        self.ui.action_note_loeschen.triggered.connect(self.delete_grade_gui)

        # Wenn sich das Halbjahr ändert, speichern und Tabelle aktualisieren
        self.ui.combo_quarter.currentIndexChanged.connect(self.save_settings_and_update)

        # Ansicht füllen
        self.update_table()

    def load_data(self):
        global data_subjects, data_grades, data_averages

        try:
            with open("data_subjects.json", "r") as file:
                content = file.read().strip()
                data_subjects = json.loads(content) if content else {}
        except (FileNotFoundError, json.JSONDecodeError):
            data_subjects = {}

        try:
            with open("data_grades.json", "r") as file:
                content = file.read().strip()
                data_grades = json.loads(content) if content else {}
        except (FileNotFoundError, json.JSONDecodeError):
            data_grades = {}

        try:
            with open("data_average_grades.json", "r") as file:
                content = file.read().strip()
                data_averages = json.loads(content) if content else {}
        except (FileNotFoundError, json.JSONDecodeError):
            data_averages = {}

    def load_settings(self):
        try:
            with open("data_settings.json", "r") as file:
                settings = json.load(file)
                saved_quarter = settings.get("quarter", "Q1")
                index = self.ui.combo_quarter.findText(saved_quarter)
                if index >= 0:
                    self.ui.combo_quarter.blockSignals(True)
                    self.ui.combo_quarter.setCurrentIndex(index)
                    self.ui.combo_quarter.blockSignals(False)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_settings_and_update(self):
        current_quarter = self.ui.combo_quarter.currentText()
        settings = {"quarter": current_quarter}
        with open("data_settings.json", "w") as file:
            json.dump(settings, file, indent=4)
        self.update_table()

    def calculate_average_grades(self, selected_code, quarter):
        sum_oral = 0
        count_oral = 0
        sum_klausur = 0
        count_klausur = 0
        sum_vocabulary = 0
        count_vocabulary = 0
        vocabulary_test_exists = 0
        average_vocabulary = 0
        average_written = 0
        oral_weight = 0
        written_weight = 0

        if selected_code in data_grades and quarter in data_grades[selected_code]:
            for grade in data_grades[selected_code][quarter]:
                if grade["type"] in ["oral", "sportif", "art-project"]:
                    sum_oral += int(grade["points"])
                    count_oral += 1
                elif grade["type"] == "klausur":
                    sum_klausur += int(grade["points"])
                    count_klausur += 1
                elif grade["type"] == "vocabulary-test":
                    sum_vocabulary += int(grade["points"])
                    count_vocabulary += 1

        average_oral = (sum_oral / count_oral) if count_oral >= 1 else 0

        if count_klausur < 1 and count_vocabulary < 1:
            average_written = 0
        else:
            if count_vocabulary >= 1:
                average_vocabulary = sum_vocabulary / count_vocabulary
                vocabulary_test_exists = 1
            average_written = (sum_klausur + average_vocabulary) / (count_klausur + vocabulary_test_exists)

        for subject_name, subject_data in data_subjects.items():
            if subject_data["key"] == selected_code:
                oral_weight = subject_data["ORA"]
                written_weight = subject_data["WRI"]

        average = (average_written * written_weight) + (average_oral * oral_weight)

        if selected_code not in data_averages:
            data_averages[selected_code] = {}

        data_averages[selected_code][quarter] = {
            "average_oral": average_oral,
            "average_written": average_written,
            "average": average
        }

        with open("data_average_grades.json", "w") as file:
            json.dump(data_averages, file, indent=4)

    def add_subject_gui(self):
        name, ok = QInputDialog.getText(self, "Fach hinzufügen", "Name des Faches:")
        if not ok or not name.strip():
            return

        code, ok = QInputDialog.getText(self, "Fach hinzufügen", "Kürzel des Faches (z.B. ENG):")
        if not ok or not code.strip():
            return
        code = code.strip().upper()

        oral, ok = QInputDialog.getDouble(self, "Gewichtung", "Mündlicher Anteil (z.B. 0.5):", 0.5, 0.0, 1.0, 2)
        if not ok:
            return

        written, ok = QInputDialog.getDouble(self, "Gewichtung", "Schriftlicher Anteil (z.B. 0.5):", 0.5, 0.0, 1.0, 2)
        if not ok:
            return

        data_subjects[name.strip()] = {
            "key": code,
            "ORA": oral,
            "WRI": written
        }

        with open("data_subjects.json", "w") as file:
            json.dump(data_subjects, file, indent=4)

        QMessageBox.information(self, "Erfolg", f"Fach '{name}' wurde erfolgreich hinzugefügt!")
        self.update_table()

    def delete_subject_gui(self):
        if not data_subjects:
            QMessageBox.warning(self, "Achtung", "Es sind keine Fächer vorhanden zum Löschen.")
            return

        subject_names = list(data_subjects.keys())
        subject_name, ok = QInputDialog.getItem(self, "Fach löschen", "Wähle das zu löschende Fach:", subject_names, 0,
                                                False)
        if not ok:
            return

        confirm = QMessageBox.question(
            self,
            "Fach löschen",
            f"Möchtest du das Fach '{subject_name}' und alle dazugehörigen Noten wirklich löschen?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        selected_code = data_subjects[subject_name]["key"]

        del data_subjects[subject_name]
        with open("data_subjects.json", "w") as file:
            json.dump(data_subjects, file, indent=4)

        if selected_code in data_grades:
            del data_grades[selected_code]
            with open("data_grades.json", "w") as file:
                json.dump(data_grades, file, indent=4)

        if selected_code in data_averages:
            del data_averages[selected_code]
            with open("data_average_grades.json", "w") as file:
                json.dump(data_averages, file, indent=4)

        QMessageBox.information(self, "Erfolg", f"Fach '{subject_name}' wurde erfolgreich gelöscht!")
        self.update_table()

    def add_grade_gui(self):
        if not data_subjects:
            QMessageBox.warning(self, "Achtung", "Es sind noch keine Fächer vorhanden! Füge zuerst eins hinzu.")
            return

        current_quarter = self.ui.combo_quarter.currentText()

        subject_names = list(data_subjects.keys())
        subject_name, ok = QInputDialog.getItem(self, "Note hinzufügen", f"Wähle das Fach (für {current_quarter}):",
                                                subject_names, 0, False)
        if not ok:
            return

        selected_code = data_subjects[subject_name]["key"]

        type_of_grades = ["oral", "klausur", "vocabulary-test", "sportif", "art-project"]
        grade_type, ok = QInputDialog.getItem(self, "Note hinzufügen", "Wähle die Notenart:", type_of_grades, 0, False)
        if not ok:
            return

        points, ok = QInputDialog.getInt(self, "Note hinzufügen", "Gib deine Punktzahl ein (0-15):", 10, 0, 15, 1)
        if not ok:
            return

        date = str(datetime.date.today())

        if selected_code not in data_grades:
            data_grades[selected_code] = {}

        if current_quarter not in data_grades[selected_code]:
            data_grades[selected_code][current_quarter] = []

        data_grades[selected_code][current_quarter].append({
            "type": grade_type,
            "points": points,
            "date": date,
        })

        with open("data_grades.json", "w") as file:
            json.dump(data_grades, file, indent=4)

        self.calculate_average_grades(selected_code, current_quarter)
        QMessageBox.information(self, "Erfolg", f"Note für {current_quarter} erfolgreich gespeichert!")
        self.update_table()

    def delete_grade_gui(self):
        if not data_grades:
            QMessageBox.warning(self, "Achtung", "Es sind noch keine Noten vorhanden zum Löschen.")
            return

        current_quarter = self.ui.combo_quarter.currentText()

        available_subjects = []
        for subject_name, subject_data in data_subjects.items():
            code = subject_data["key"]
            if code in data_grades and current_quarter in data_grades[code] and data_grades[code][current_quarter]:
                available_subjects.append(subject_name)

        if not available_subjects:
            QMessageBox.warning(self, "Achtung", f"Keines der Fächer enthält Noten im Halbjahr {current_quarter}.")
            return

        subject_name, ok = QInputDialog.getItem(self, "Note löschen", f"Wähle das Fach ({current_quarter}):",
                                                available_subjects, 0, False)
        if not ok:
            return

        selected_code = data_subjects[subject_name]["key"]
        grades_list = data_grades[selected_code][current_quarter]

        grade_descriptions = [f"{i + 1}: Typ: {g['type']} | Punkte: {g['points']} | Datum: {g['date']}" for i, g in
                              enumerate(grades_list)]

        grade_choice, ok = QInputDialog.getItem(self, "Note löschen", "Wähle die zu löschende Note:",
                                                grade_descriptions, 0, False)
        if not ok:
            return

        selected_index = grade_descriptions.index(grade_choice)
        data_grades[selected_code][current_quarter].pop(selected_index)

        if not data_grades[selected_code][current_quarter]:
            del data_grades[selected_code][current_quarter]
        if not data_grades[selected_code]:
            del data_grades[selected_code]

        with open("data_grades.json", "w") as file:
            json.dump(data_grades, file, indent=4)

        self.calculate_average_grades(selected_code, current_quarter)

        QMessageBox.information(self, "Erfolg", f"Note in {current_quarter} wurde gelöscht!")
        self.update_table()

    def update_table(self):
        self.treeWidget.clear()
        current_quarter = self.ui.combo_quarter.currentText()

        total_all_quarters_sum = 0
        total_all_quarters_count = 0

        for subject_name, subject_data in data_subjects.items():
            code = subject_data["key"]

            sub_avgs = data_averages.get(code, {})
            current_q_avg = sub_avgs.get(current_quarter, {})
            avg_oral = current_q_avg.get("average_oral", 0)
            avg_written = current_q_avg.get("average_written", 0)
            total_avg = current_q_avg.get("average", 0)

            all_q_values = [q_data.get("average", 0) for q_data in sub_avgs.values() if q_data.get("average", 0) > 0]
            subject_overall_avg = (sum(all_q_values) / len(all_q_values)) if all_q_values else 0

            if subject_overall_avg > 0:
                total_all_quarters_sum += subject_overall_avg
                total_all_quarters_count += 1

            avg_text = f"M: {avg_oral:.1f}  |  S: {avg_written:.1f}  |  Ges ({current_quarter}): {total_avg:.1f}  |  Abi-Ø: {subject_overall_avg:.1f}"

            subject_item = QTreeWidgetItem(self.treeWidget)
            subject_item.setText(0, f"📚  {subject_name} ({code})")
            subject_item.setText(3, avg_text)

            font = subject_item.font(0)
            font.setBold(True)
            subject_item.setFont(0, font)
            subject_item.setFont(3, font)

            if code in data_grades and current_quarter in data_grades[code] and data_grades[code][current_quarter]:
                for grade in data_grades[code][current_quarter]:
                    grade_item = QTreeWidgetItem(subject_item)
                    grade_item.setText(0, f"▪  {grade['type']}")
                    grade_item.setText(1, f"{grade['points']} Pkt.")
                    grade_item.setText(2, grade['date'])
            else:
                empty_item = QTreeWidgetItem(subject_item)
                empty_item.setText(0, f"▪  Keine Noten in {current_quarter} vorhanden")
                empty_item.setForeground(0, QtGui.QBrush(QtGui.QColor(150, 150, 150)))

        overall_abi = (total_all_quarters_sum / total_all_quarters_count) if total_all_quarters_count > 0 else 0
        self.ui.statusbar.showMessage(
            f"Aktives Halbjahr: {current_quarter}   |   Gesamt-Abiturschnitt (alle Halbjahre): {overall_abi:.2f} Punkte")

        for i in range(4):
            self.treeWidget.resizeColumnToContents(i)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # WICHTIG: Verknüpft den Prozess exakt mit der .desktop-Datei (muss genauso heißen wie die .desktop-Datei ohne Endung)
    app.setDesktopFileName("notenrechner")

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())