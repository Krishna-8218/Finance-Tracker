import json
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class Dashboard(QWidget):
    def __init__(self, switch_callback):
        super().__init__()

        # 🏷️ Layout for Dashboard
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("💵 Finance Tracker")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #FFFFFF;
            background-color: #333333;
            padding: 15px;
            border-radius: 5px;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 🔢 Financial Metrics (Income, Expense, Balance)
        glass_style = """
            background-color: rgba(255, 255, 255, 0.2); /* Glassmorphism effect */
            border-radius: 10px;
            padding: 10px;
            color: #B0B0B0;
            font-weight: bold;
        """
        self.total_income_label = QLabel("Total Income: ₹0")
        self.total_income_label.setStyleSheet(glass_style)

        self.total_expense_label = QLabel("Total Expense: ₹0")
        self.total_expense_label.setStyleSheet(glass_style)

        self.remaining_balance_label = QLabel("Remaining Balance: ₹0")
        self.remaining_balance_label.setStyleSheet(glass_style)

        layout.addWidget(self.total_income_label)
        layout.addWidget(self.total_expense_label)
        layout.addWidget(self.remaining_balance_label)

        # 🧭 Navigation Buttons
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(20)

        button_style = """
            QPushButton {
                background-color: #444444;
                color: #FFFFFF;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
                transition: background-color 0.3s ease-in-out;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """
        for name in ["Add Income", "Add Expense", "Transactions", "Reports", "Settings"]:
            btn = QPushButton(name)
            btn.setStyleSheet(button_style)
            btn.clicked.connect(lambda checked, page=name: switch_callback(page))
            nav_layout.addWidget(btn)

        layout.addLayout(nav_layout)
        self.setLayout(layout)

        # Apply the saved theme
        self.theme = self.load_theme()
        self.apply_theme()

    def load_theme(self):
        """Loads the saved theme from settings.json."""
        try:
            with open("settings.json", "r") as file:
                data = json.load(file)
                return data.get("background_color", "#FFFFFF")
        except FileNotFoundError:
            return "#FFFFFF"

    def apply_theme(self):
        """Applies the selected theme across the app."""
        self.setStyleSheet(f"background-color: {self.theme}; color: #B0B0B0;")