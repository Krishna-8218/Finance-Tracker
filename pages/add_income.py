import csv
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QDateEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt, QDate

class AddIncomePage(QWidget):
    def __init__(self, switch_callback):
        super().__init__()

        # Page Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 🏷️ Title with Balanced Styling
        title = QLabel("Add Income")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #FFFFFF;
            background-color: #333333;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 💰 Amount Field
        amount_label = QLabel("Enter Amount (₹):")
        amount_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")
        amount_input = QLineEdit()
        amount_input.setPlaceholderText("e.g., 5000")
        amount_input.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
            border: 1px solid #666666;
            border-radius: 5px;
            color: #FFFFFF;
            background-color: #222222;
        """)
        layout.addWidget(amount_label)
        layout.addWidget(amount_input)

        # 📅 Date Field
        date_label = QLabel("Select Date:")
        date_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")
        date_input = QDateEdit()
        date_input.setDate(QDate.currentDate())
        date_input.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
            border: 1px solid #666666;
            border-radius: 5px;
            color: #FFFFFF;
            background-color: #222222;
        """)
        layout.addWidget(date_label)
        layout.addWidget(date_input)

        # 🏷️ Source of Income Field
        category_label = QLabel("Source of Income:")
        category_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")
        category_input = QLineEdit()
        category_input.setPlaceholderText("e.g., Salary, Freelance, Bonus")
        category_input.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
            border: 1px solid #666666;
            border-radius: 5px;
            color: #FFFFFF;
            background-color: #222222;
        """)
        layout.addWidget(category_label)
        layout.addWidget(category_input)

        # 💸 Add Income Button
        add_button = QPushButton("Add Income")
        add_button.setStyleSheet("""
            background-color: #444444;
            color: #FFFFFF;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
            border: none;
            border-radius: 5px;
        """)
        add_button.clicked.connect(lambda: self.add_income(amount_input.text(), date_input.date(), category_input.text()))
        layout.addWidget(add_button)

        # 🔙 Back to Dashboard Button
        back_btn = QPushButton("Back to Dashboard")
        back_btn.setStyleSheet("""
            background-color: #666666;
            color: #FFFFFF;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
            border: none;
            border-radius: 5px;
        """)
        back_btn.clicked.connect(lambda: switch_callback("Dashboard"))
        layout.addWidget(back_btn)

        # Apply Layout
        self.setLayout(layout)

    def add_income(self, amount, date, category):
        if amount and category:  # Ensure fields are filled
            transaction = [amount, date.toString("yyyy-MM-dd"), category]
            self.save_to_csv(transaction)
            self.show_success_popup()  # Show confirmation pop-up
            print(f"Added Income: {transaction}")

    def save_to_csv(self, transaction):
        try:
            with open("transactions.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(transaction)
        except Exception as e:
            print(f"Error saving to CSV: {e}")

    def show_success_popup(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Success")
        msg_box.setText("Income successfully added!")
        msg_box.setStyleSheet("""
            font-size: 14px;
            color: #FFFFFF;
            background-color: #333333;
        """)
        msg_box.exec()