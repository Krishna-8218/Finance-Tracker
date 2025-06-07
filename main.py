
import os
import json

# Set path to save budgets.json in the same folder as main.py
BUDGET_FILE = os.path.join(os.path.dirname(__file__), "budgets.json")

def load_budgets():
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "r") as file:
            return json.load(file)
    return {}

def save_budgets(budgets):
    with open(BUDGET_FILE, "w") as file:
        json.dump(budgets, file)
        
import sys
import csv
import json
import os
from datetime import datetime

# Data Processing
import pandas as pd
from joblib import dump, load

# Machine Learning
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Qt Framework
from PySide6.QtWidgets import (QApplication, QMainWindow, QStackedWidget, 
                              QMessageBox, QGraphicsOpacityEffect, QLabel)
from PySide6.QtCore import QPropertyAnimation, Qt
from PySide6.QtGui import QColor

# Application Pages
from pages.dashboard import Dashboard
from pages.add_income import AddIncomePage
from pages.add_expense import AddExpensePage
from pages.transactions import TransactionsPage
from pages.reports import ReportsPage
from pages.settings import SettingsPage



class AICategorizer:
    def __init__(self, model_path=None):
        # Default model path: ~/ai_models/expense_model.joblib
        if not model_path:
            home_dir = os.path.expanduser("~")
            model_path = os.path.join(home_dir, 'ai_models', 'expense_model.joblib')

        # Ensure the folder exists
        os.makedirs(os.path.dirname(model_path), exist_ok=True)

        self.model_path = model_path
        self.model = make_pipeline(
            CountVectorizer(ngram_range=(1, 2), stop_words='english', min_df=2),
            MultinomialNB()
        )

        # Load saved model if it exists
        self.trained = False

        if os.path.exists(self.model_path):
            self.model = load(self.model_path)
            self.trained = True
    
    def train(self, descriptions, categories):
        self.trained = True
        """Train model with evaluation"""
        if len(set(categories)) < 2:
            return 0  # Need at least 2 categories to train
            
        X_train, X_test, y_train, y_test = train_test_split(
            pd.Series(descriptions), 
            categories,
            test_size=0.2,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        dump(self.model, self.model_path)
        
        # Evaluate accuracy
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"Model trained. Accuracy: {acc:.2f}")
        return acc
    
    def predict(self, description, confidence_threshold=0.7):
        """Predict with confidence checking"""
        if not self.trained:
            print("Prediction skipped: model not trained.")
            return None
        try:
            proba = self.model.predict_proba([description])[0]
            max_prob = max(proba)
            if max_prob >= confidence_threshold:
                return self.model.classes_[proba.argmax()]
        except Exception as e:
            print(f"Prediction error: {str(e)}")
        return None


#


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finance Tracker AI")
        self.setMinimumSize(800, 600)
        
        # Initialize systems
        self.theme = self.load_theme()
        self.ai_categorizer = AICategorizer()
        self.init_ui()
        

        self.load_initial_data()
    
    def init_ui(self):
        """Initialize user interface"""
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        self.pages = {
            "Dashboard": Dashboard(self.switch_page),
            "Add Income": AddIncomePage(self.switch_page),
            "Add Expense": AddExpensePage(self.switch_page),
            "Transactions": TransactionsPage(self.switch_page),
            "Reports": ReportsPage(self.switch_page),
            "Settings": SettingsPage(self.switch_page, self.apply_theme)
        }
        
        for page in self.pages.values():
            self.stack.addWidget(page)
        
        self.apply_theme(self.theme)
        self.stack.setCurrentWidget(self.pages["Dashboard"])
    
    def load_initial_data(self):
        """Load data and train AI model"""
        try:
            # Read transactions with proper headers
            """Train model with predefined sample data only"""
            # Sample training data
            training_data = [
                ("pizza", "Food"),
                ("flipkart headphones", "Shopping"),
                ("ola ride", "Transport"),
                ("uber ride", "Transport"),
                ("salary", "Income"),
                ("pen", "Stationery"),
                ("checking out", "Other"),
                ("trip", "Travel"),
                ("notebooks", "Stationery"),
                ("coffee", "Food"),
                ("movie ticket", "Entertainment"),
                ("restaurant food", "Food"),
                ("laundry", "Utilities"),
                ("groceries", "Food"),
                ("internet subscription", "Utilities"),
                ("flipkart order", "Shopping"),
                ("burger", "Food"),
                ("icecream", "Food"),
                ("haircut", "Personal Care"),
                ("printer paper", "Stationery"),
                ("snacks", "Food"),
            ]

            descriptions = [item[0] for item in training_data]
            categories = [item[1] for item in training_data]

            
            self.ai_categorizer.train(descriptions, categories)
                
        except (FileNotFoundError, pd.errors.EmptyDataError) as e:
            print(f"Initial data loading: {str(e)}")
            
        try:
            df = pd.read_csv('transactions.csv', 
                            header=None,
                            names=['amount', 'date', 'description'],
                            dtype={'amount': float, 'description': str})
            
            if not df.empty:
                # Drop rows with missing description
                df = df.dropna(subset=['description'])

                # Step 3: Predict categories using AI
                df['predicted_category'] = df['description'].apply(self.ai_categorizer.predict)


                # Store for chart/reporting
                self.predicted_df = df

                # Optional: Print predictions
                print("\nPredicted categories for transactions:")
                print(df[['description', 'predicted_category']].to_string(index=False))
        
        except Exception as e:
            print(f"Error loading transaction data: {e}")
            self.predicted_df = pd.DataFrame(columns=['amount', 'date', 'description', 'predicted_category'])
    
    def categorize_expense(self, description):
        
        if pd.notna(description) and str(description).strip():
            ai_category = self.ai_categorizer.predict(description, confidence_threshold=0.75)
            if ai_category:
                return ai_category
        return self.rule_based_categorize(description)
        
    def rule_based_categorize(self, description):
        """Original rule-based system"""
        rules = {
            "Food": ["pizza", "burger", "restaurant", "cafe", "restaurant food","groceries","snacks","icecream","coffee"],
            "Transport": ["uber ride", "bus", "train", "taxi", "fuel","ola ride","uber"],
            "Entertainment": ["netflix", "cinema", "movie", "concert", "game","checking out","trip"],
            "Shopping": ["amazon", "mall", "clothing", "electronics","flipkart headphones","groceries","flipkart order"],
            "Utilities": ["electricity", "water", "internet", "gas", "rent","laundry"],
            "Stationary":["pen","notebooks","printer paper","internet subscription"]
        }
        
        if pd.isna(description):
            return "Other"
            
        description = str(description).lower()
        for category, keywords in rules.items():
            if any(keyword in description for keyword in keywords):
                return category
        return "Other"
    
    def update_summary(self):
        """Updates financial metrics with AI-enhanced categories and prints predicted categories"""
        total_income = 0
        total_expense = 0
        categorized_totals = {}
        category_counts = {}

        print("\nPredicted categories for transactions:")

        try:
            with open("transactions.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 3:  # Skip malformed rows (expecting amount, date, description)
                        continue

                    try:
                        amount = float(row[0])
                        description = row[2]  # 3rd column is description
                        category = self.categorize_expense(description)  # AI-based categorization

                        # Print each predicted category
                        print(f"'{description}' => {category}")

                        if amount > 0:
                            total_income += amount
                        else:
                            total_expense += abs(amount)

                        if category not in categorized_totals:
                            categorized_totals[category] = 0
                            category_counts[category] = 0

                        categorized_totals[category] += abs(amount)
                        category_counts[category] += 1

                    except (ValueError, IndexError):
                        continue

        except FileNotFoundError:
            print("transactions.csv not found. Defaulting totals to 0.")

        # Update Dashboard UI
        dashboard = self.pages["Dashboard"]
        dashboard.total_income_label.setText(f"Total Income: ₹{total_income:.2f}")
        dashboard.total_expense_label.setText(f"Total Expense: ₹{total_expense:.2f}")
        dashboard.remaining_balance_label.setText(f"Remaining Balance: ₹{total_income - total_expense:.2f}")

        # Update Reports chart with categorized data
        self.pages["Reports"].update_charts(categorized_totals, category_counts)

        self.budgets = load_budgets()
        
    #
    
    
    def switch_page(self, page_name):
        """Handles navigation with smooth transitions."""
        self.animate_page_switch(self.pages[page_name])

        if page_name == "Dashboard":
            self.update_summary()
        elif page_name == "Transactions":
            self.pages["Transactions"].update_table()
        elif page_name == "Reports":
            self.update_summary()

    def animate_page_switch(self, new_page):
        """Creates a fade transition effect when switching pages."""
        opacity_effect = QGraphicsOpacityEffect()
        self.stack.setGraphicsEffect(opacity_effect)

        animation = QPropertyAnimation(opacity_effect, b"opacity")
        animation.setDuration(300)
        animation.setStartValue(0.1)
        animation.setEndValue(1.0)
        animation.start()

        self.stack.setCurrentWidget(new_page)
    
    def load_theme(self):
        """Loads the saved background color."""
        try:
            with open("settings.json", "r") as file:
                data = json.load(file)
                return data.get("background_color", "#FFFFFF")
        except FileNotFoundError:
            return "#FFFFFF"

    def save_theme(self, color_hex):
        """Saves the selected background color."""
        with open("settings.json", "w") as file:
            json.dump({"background_color": color_hex}, file)

    def apply_theme(self, color_hex):
        """Applies the user-selected background color."""
        self.theme = color_hex
        self.save_theme(color_hex)
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {color_hex};
                color: #333333;
            }}
            QLabel {{
                color: #333333;
            }}
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
