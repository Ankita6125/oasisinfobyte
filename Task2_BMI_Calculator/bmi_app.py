import sys
import csv
import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QDialog, QMessageBox, QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QRect, QCoreApplication
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class CustomPopup(QDialog):
    def __init__(self, title, message):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(400, 200)
        layout = QVBoxLayout()
        label = QLabel(message)
        label.setWordWrap(True)
        label.setFont(QFont("Segoe UI", 12))
        layout.addWidget(label)
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; color: white; padding: 8px; border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(ok_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)

class BMICalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced BMI Calculator")
        self.resize(450, 650)
        self.center_window()
        self.data_file = "bmi_data.csv"
        self.initUI()

    def center_window(self):
        
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        
        font_label = QFont("Segoe UI", 12)
        font_input = QFont("Segoe UI", 11)
        font_button = QFont("Segoe UI Semibold", 12)

        
        self.name_label = QLabel("Name:")
        self.name_label.setFont(font_label)
        self.name_input = QLineEdit()
        self.name_input.setFont(font_input)

        
        self.height_label = QLabel("Height (in cm):")
        self.height_label.setFont(font_label)
        self.height_input = QLineEdit()
        self.height_input.setFont(font_input)

        
        self.weight_label = QLabel("Weight (in kg):")
        self.weight_label.setFont(font_label)
        self.weight_input = QLineEdit()
        self.weight_input.setFont(font_input)

        
        self.calc_button = QPushButton("Calculate BMI")
        self.calc_button.setFont(font_button)
        self.calc_button.clicked.connect(self.calculate_bmi)

        
        self.result_label = QLabel("")
        self.result_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.result_label.setStyleSheet("color: #333333; margin-top: 15px;")

        self.category_label = QLabel("")
        self.category_label.setFont(QFont("Segoe UI", 13))
        self.category_label.setStyleSheet("color: #555555; font-style: italic; margin-bottom: 20px;")

        
        self.show_history_btn = QPushButton("Show BMI History")
        self.show_history_btn.setFont(font_button)
        self.show_history_btn.clicked.connect(self.show_history)

        
        self.show_graph_btn = QPushButton("Show BMI Trend Graph")
        self.show_graph_btn.setFont(font_button)
        self.show_graph_btn.clicked.connect(self.show_graph)

        
        button_style = """
        QPushButton {
            background-color: #4CAF50;  /* Green */
            color: white;
            border-radius: 8px;
            padding: 12px;
            margin-top: 10px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        """

        input_style = """
        QLineEdit {
            border: 2px solid #ccc;
            border-radius: 8px;
            padding: 8px;
            font-size: 14px;
        }
        QLineEdit:focus {
            border-color: #4CAF50;
        }
        """

        self.calc_button.setStyleSheet(button_style)
        self.show_history_btn.setStyleSheet(button_style)
        self.show_graph_btn.setStyleSheet(button_style)

        self.name_input.setStyleSheet(input_style)
        self.height_input.setStyleSheet(input_style)
        self.weight_input.setStyleSheet(input_style)

        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(18)

        def create_row(label_widget, input_widget):
            h_layout = QHBoxLayout()
            h_layout.addWidget(label_widget)
            h_layout.addStretch()
            h_layout.addWidget(input_widget)
            return h_layout

        main_layout.addLayout(create_row(self.name_label, self.name_input))
        main_layout.addLayout(create_row(self.height_label, self.height_input))
        main_layout.addLayout(create_row(self.weight_label, self.weight_input))
        main_layout.addWidget(self.calc_button)
        main_layout.addWidget(self.result_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.category_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.show_history_btn)
        main_layout.addWidget(self.show_graph_btn)

        self.setLayout(main_layout)

    def calculate_bmi(self):
        try:
            name = self.name_input.text().strip()
            height_cm = float(self.height_input.text())
            weight = float(self.weight_input.text())

            
            if not name:
                self.show_custom_warning("Input Error", "Please enter your name.")
                return

            if height_cm <= 50 or height_cm >= 300:
                self.show_custom_warning("Input Error", "Please enter realistic height (50-300 cm).")
                return

            if weight <= 10 or weight >= 500:
                self.show_custom_warning("Input Error", "Please enter realistic weight (10-500 kg).")
                return

            height_m = height_cm / 100
            bmi = weight / (height_m ** 2)
            bmi = round(bmi, 2)

            category = self.get_bmi_category(bmi)

            self.result_label.setText(f"BMI: {bmi}")
            self.category_label.setText(f"Category: {category}")

            
            self.save_to_csv(name, height_cm, weight, bmi, category)

        except ValueError:
            self.show_custom_warning("Input Error", "Please enter valid numeric height and weight.")

    def get_bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def save_to_csv(self, name, height, weight, bmi, category):
        try:
            with open(self.data_file, 'a', newline='') as file:
                writer = csv.writer(file)
                
                file.seek(0, 2)  
                if file.tell() == 0:
                    writer.writerow(["Name", "Height(cm)", "Weight(kg)", "BMI", "Category", "Date"])
                date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([name, height, weight, bmi, category, date_str])
        except Exception as e:
            self.show_custom_warning("File Error", f"Could not save data:\n{e}")

    def show_custom_warning(self, title, message):
        popup = CustomPopup(title, message)
        popup.exec_()

    def show_history(self):
        try:
            with open(self.data_file, 'r') as file:
                reader = csv.reader(file)
                data = list(reader)

            if len(data) <= 1:
                self.show_custom_warning("No Data", "No BMI history found.")
                return

           
            dialog = QDialog(self)
            dialog.setWindowTitle("BMI History")
            dialog.resize(700, 400)
            layout = QVBoxLayout()

            table = QTableWidget()
            table.setRowCount(len(data) - 1)
            table.setColumnCount(len(data[0]))
            table.setHorizontalHeaderLabels(data[0])

            for row_idx, row_data in enumerate(data[1:]):
                for col_idx, val in enumerate(row_data):
                    table.setItem(row_idx, col_idx, QTableWidgetItem(val))

            layout.addWidget(table)
            dialog.setLayout(layout)
            dialog.exec_()

        except FileNotFoundError:
            self.show_custom_warning("File Error", "No data file found.")
        except Exception as e:
            self.show_custom_warning("Error", f"An error occurred:\n{e}")

    def show_graph(self):
        try:
            with open(self.data_file, 'r') as file:
                reader = csv.DictReader(file)
                dates = []
                bmis = []

                for row in reader:
                    dates.append(datetime.datetime.strptime(row["Date"], "%Y-%m-%d %H:%M:%S"))
                    bmis.append(float(row["BMI"]))

            if not dates:
                self.show_custom_warning("No Data", "No BMI data found for graph.")
                return

            
            fig, ax = plt.subplots()
            ax.plot(dates, bmis, marker='o', linestyle='-', color='teal')
            ax.set_title("BMI Trend Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("BMI")
            ax.grid(True)
            fig.autofmt_xdate()

            
            dialog = QDialog(self)
            dialog.setWindowTitle("BMI Trend Graph")
            dialog.resize(800, 500)
            layout = QVBoxLayout()

            canvas = FigureCanvas(fig)
            layout.addWidget(canvas)

            dialog.setLayout(layout)
            dialog.exec_()

        except FileNotFoundError:
            self.show_custom_warning("File Error", "No data file found.")
        except Exception as e:
            self.show_custom_warning("Error", f"An error occurred:\n{e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    bmi_app = BMICalculator()
    bmi_app.show()
    sys.exit(app.exec_())
