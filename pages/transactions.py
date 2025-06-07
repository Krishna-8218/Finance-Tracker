import csv
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class TransactionsPage(QWidget):
    def __init__(self, switch_callback):
        super().__init__()
        self.init_ui(switch_callback)

    def init_ui(self, switch_callback):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 🏷️ Title with Enhanced Styling
        title = QLabel("Transactions")
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

        # 📊 Transaction Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Amount (₹)", "Description", "Category"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setStyleSheet("""
            QHeaderView::section {
                background-color: #444444;
                color: #FFFFFF;
                font-size: 16px;
                font-weight: bold;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #666666;
            }
            QTableWidget {
                background-color: #222222;
                color: #FFFFFF;
                font-size: 14px;
                border: 1px solid #444444;
            }
            QTableWidget::item {
                border-bottom: 1px solid #666666;
            }
        """)
        layout.addWidget(self.table)

        # 🔙 Back Button
        back_btn = QPushButton("Back to Dashboard")
        back_btn.setStyleSheet("""
            background-color: #444444;
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
        self.update_table()

    def categorize_expense(self, description):
        """Assigns an expense category based on keywords."""
        rules = {
            "Food": ["pizza", "burger", "restaurant", "cafe", "restaurant food","groceries","snacks","icecream"],
            "Transport": ["uber ride", "bus", "train", "taxi", "fuel","ola ride","uber"],
            "Entertainment": ["netflix", "cinema", "movie", "concert", "game","checking out","trip"],
            "Shopping": ["amazon", "mall", "clothing", "electronics","flipkart headphones","groceries"],
            "Utilities": ["electricity", "water", "internet", "gas", "rent","laundry"],
            "Stationary":["pen","notebooks","printer paper","internet subscription"]
        }

        description = description.lower()  # Convert text to lowercase for matching
        for category, keywords in rules.items():
            if any(keyword in description for keyword in keywords):
                return category  # Return matched category

        return "Other"  # Default if no match found

    def update_table(self):
        """Reads transactions, assigns categories only if needed, and updates the UI."""
        self.table.setRowCount(0)  # Clear existing rows
        
        updated_rows = []
        try:
            print("Reading transactions.csv...")
            with open("transactions.csv", "r") as file:
                reader = csv.reader(file)
                for row_data in reader:
                    if len(row_data) != 3:
                        continue  # skip bad rows
                        
                    amount, date, third = row_data

                    # 🧠 Detect if 'third' is a known category
                    known_categories = {
                        "food", "transport", "entertainment", "shopping", "utilities", "stationary", "income", "other"
                    }
                    
                    third_lower = third.strip().lower()
                    if third_lower in known_categories:
                        category = third.capitalize()
                        description = category  # optional: you can set empty string if you don't have one
                    else:
                        description = third
                        category = self.categorize_expense(description)
                        
                    updated_rows.append([amount, date, category]) 
                    row = self.table.rowCount()
                    self.table.insertRow(row)


                    # ➕ Amount with coloring
                    item_amount = QTableWidgetItem(amount)
                    item_amount.setTextAlignment(Qt.AlignCenter)
                    item_amount.setForeground(QColor("red") if float(amount) < 0 else QColor("green"))
                    self.table.setItem(row, 0, item_amount)

                    # ➕ Description (if it's an actual description)
                    item_description = QTableWidgetItem(description)
                    item_description.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(row, 1, item_description)

                    # ➕ Category (from either source)
                    item_category = QTableWidgetItem(category)
                    item_category.setTextAlignment(Qt.AlignCenter)
                    item_category.setForeground(QColor("cyan"))
                    self.table.setItem(row, 2, item_category)
            with open("transactions.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)

        except FileNotFoundError:
            print("No transactions found. CSV file does not exist.")
