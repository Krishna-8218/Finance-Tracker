import csv
import json
import pandas as pd
from datetime import datetime
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QDateEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt, QDate

class AddExpensePage(QWidget):
    def __init__(self, switch_callback):
        super().__init__()

        # Page Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Add Expense")
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

        # Amount Field
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("e.g., 2000")
        self.amount_input.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
            border: 1px solid #666666;
            border-radius: 5px;
            color: #FFFFFF;
            background-color: #222222;
        """)
        layout.addWidget(QLabel("Enter Amount (₹):", styleSheet="font-size: 16px; font-weight: bold; color: #FFFFFF;"))
        layout.addWidget(self.amount_input)

        # Date Field
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
            border: 1px solid #666666;
            border-radius: 5px;
            color: #FFFFFF;
            background-color: #222222;
        """)
        layout.addWidget(QLabel("Select Date:", styleSheet="font-size: 16px; font-weight: bold; color: #FFFFFF;"))
        layout.addWidget(self.date_input)

        # Category Field
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("e.g., Food, Transport, Entertainment")
        self.category_input.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
            border: 1px solid #666666;
            border-radius: 5px;
            color: #FFFFFF;
            background-color: #222222;
        """)
        layout.addWidget(QLabel("Expense Category:", styleSheet="font-size: 16px; font-weight: bold; color: #FFFFFF;"))
        layout.addWidget(self.category_input)

        # Add Button
        add_button = QPushButton("Add Expense")
        add_button.setStyleSheet("""
            background-color: #444444;
            color: #FFFFFF;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
            border: none;
            border-radius: 5px;
        """)
        add_button.clicked.connect(self.handle_add_expense)
        layout.addWidget(add_button)

        # Back Button
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

        self.setLayout(layout)

    def handle_add_expense(self):
        amount = self.amount_input.text()
        date = self.date_input.date()
        category = self.category_input.text()

        if amount and category:
            transaction = [-float(amount), date.toString("yyyy-MM-dd"), category]
            self.save_to_csv(transaction)
            self.show_success_popup()
            print(f"Added Expense: {transaction}")
            self.check_budget_and_notify()

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
        msg_box.setText("Expense successfully added!")
        msg_box.setStyleSheet("""
            font-size: 14px;
            color: #FFFFFF;
            background-color: #333333;
        """)
        msg_box.exec()

    def check_budget_and_notify(self):
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)

            budgets = settings.get("budgets", {})
            if not budgets:
                return

            df = pd.read_csv("transactions.csv")
            df["Date"] = pd.to_datetime(df["Date"])

            now = datetime.now()
            df = df[(df["Date"].dt.month == now.month) & (df["Date"].dt.year == now.year)]

            messages = []

            for category, budget in budgets.items():
                spent = df[df["Category"] == category]["Amount"].sum()

                if spent >= budget:
                    messages.append(f"⚠️ You have **exceeded** your budget for '{category}'!\nSpent: ₹{abs(spent)}, Limit: ₹{budget}")
                elif spent >= 0.8 * budget:
                    messages.append(f"🔔 You've spent **over 80%** of your budget for '{category}'.\nSpent: ₹{abs(spent)}, Limit: ₹{budget}")

            if messages:
                QMessageBox.warning(self, "Budget Warning", "\n\n".join(messages))

        except Exception as e:
            print(f"[Budget Check Error] {e}")
