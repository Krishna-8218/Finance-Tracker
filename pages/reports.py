import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ReportsPage(QWidget):
    def __init__(self, switch_callback):
        super().__init__()

        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # 🏷️ Title
        title = QLabel("📊 Spending Reports")
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

        # 🔽 Chart Type Selection (Drop-down menu)
        self.chart_selector = QComboBox()
        self.chart_selector.addItems(["Pie Chart - Categories", "Weekly Spending", "Monthly Breakdown", "Monthly Comparison"])
        self.chart_selector.setStyleSheet("font-size: 16px; padding: 8px; border-radius: 5px;")
        self.chart_selector.currentIndexChanged.connect(self.update_chart)  # ✅ Auto-update on selection change
        layout.addWidget(self.chart_selector)

        # 📉 Chart Area
        self.figure = Figure(figsize=(5, 4))

        self.canvas = FigureCanvas(self.figure)  # Slightly wider chart
        layout.addWidget(self.canvas)

        # Initialize pie and bar charts
        self.pie_chart = FigureCanvas(Figure(figsize=(4, 3)))
        self.bar_chart = FigureCanvas(Figure(figsize=(4, 3)))

        # Add axes for pie and bar charts
        self.pie_chart.axes = self.pie_chart.figure.add_subplot(111)
        self.bar_chart.axes = self.bar_chart.figure.add_subplot(111)

        # 🔙 Back to Dashboard Button
        back_btn = QPushButton("Back to Dashboard")
        back_btn.setStyleSheet("""
            background-color: #666666;
            color: #FFFFFF;
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
        """)
        back_btn.clicked.connect(lambda: switch_callback("Dashboard"))
        layout.addWidget(back_btn)

        # Apply layout
        self.setLayout(layout)

        # Generate initial chart
        self.update_chart()

    def update_chart(self):
        """Reads transaction data and updates the selected chart inside the GUI."""
        try:
            # Load transactions
            df = pd.read_csv("transactions.csv", header=None, names=["Amount", "Date", "Category"])
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
            df["Date"] = pd.to_datetime(df["Date"])

            # Get selected chart type
            selected_chart = self.chart_selector.currentText()
            self.canvas.figure.clear()
            ax = self.canvas.figure.add_subplot(111)

            if selected_chart == "Pie Chart - Categories":
                # Aggregate expenses by category
                expenses = df[df["Amount"] < 0]
                category_totals = expenses.groupby("Category")["Amount"].sum().abs()

                # Generate color map
                unique_categories = category_totals.index
                colors = plt.cm.tab10.colors[:len(unique_categories)]  # Assign dynamic colors

                # Create pie chart with enhanced labels
                category_totals.plot(kind="pie", autopct="%1.1f%%", startangle=90, ax=ax, colors=colors)
                ax.set_title("Spending by Category")
                ax.set_ylabel("")  # Hide y-label

            elif selected_chart == "Weekly Spending":
                # Group expenses by week
                expenses = df[df["Amount"] < 0]
                expenses["Week"] = expenses["Date"].dt.to_period("W")
                weekly_totals = expenses.groupby("Week")["Amount"].sum().abs()

                # Improved bar chart with labels
                weekly_totals.plot(kind="bar", color="blue", ax=ax)
                ax.set_title("Weekly Spending Trend")
                ax.set_xlabel("Week")
                ax.set_ylabel("Total Spent (₹)")
                ax.grid(True, linestyle="--", alpha=0.6)

                # Add data labels for better readability
                for i, v in enumerate(weekly_totals):
                    ax.text(i, v + 200, f"₹{int(v)}", ha="center", fontsize=10, fontweight="bold")

            elif selected_chart == "Monthly Breakdown":
                # Group expenses by month
                expenses = df[df["Amount"] < 0]
                expenses["Month"] = expenses["Date"].dt.to_period("M")
                monthly_totals = expenses.groupby(["Month", "Category"])["Amount"].sum().abs().unstack()

                # Stacked bar chart with category-wise spending
                monthly_totals.plot(kind="bar", stacked=True, ax=ax, cmap="coolwarm")
                ax.set_title("Monthly Spending Breakdown")
                ax.set_xlabel("Month")
                ax.set_ylabel("Total Spent (₹)")
                ax.legend(title="Category", bbox_to_anchor=(1.05, 1), loc="upper left")

            elif selected_chart == "Monthly Comparison":
                # Compare total spending across months + add trend line
                expenses = df[df["Amount"] < 0]
                expenses["Month"] = expenses["Date"].dt.to_period("M")
                monthly_totals = expenses.groupby("Month")["Amount"].sum().abs()

                monthly_totals.plot(kind="bar", color="red", ax=ax)
                ax.set_title("Month-to-Month Spending Comparison")
                ax.set_xlabel("Month")
                ax.set_ylabel("Total Spent (₹)")

                # Add trend line (Linear Fit)
                x = np.arange(len(monthly_totals))
                y = monthly_totals.values
                m, b = np.polyfit(x, y, 1)  # Linear regression
                ax.plot(x, m*x + b, color="blue", linestyle="dashed", linewidth=2)

            # Refresh Canvas
            self.canvas.draw()

        except Exception as e:
            print(f"Error generating chart: {e}")
            
    def update_charts(self, categorized_totals, category_counts):
        """Updates the pie chart and bar chart using AI-enhanced categories"""
        from matplotlib import pyplot as plt

        # Clear previous charts
        self.pie_chart.axes.clear()
        self.bar_chart.axes.clear()

        # Pie chart (category-wise expense breakdown)
        if categorized_totals:
            labels = list(categorized_totals.keys())
            sizes = list(categorized_totals.values())
            self.pie_chart.axes.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            self.pie_chart.axes.set_title("Expenses by Category (AI-based)")
        else:
            self.pie_chart.axes.text(0.5, 0.5, "No Data", horizontalalignment='center', verticalalignment='center')

        # Bar chart (category frequency)
        if category_counts:
            labels = list(category_counts.keys())
            counts = list(category_counts.values())
            self.bar_chart.axes.bar(labels, counts, color='skyblue')
            self.bar_chart.axes.set_title("Number of Transactions per Category")
            self.bar_chart.axes.set_ylabel("Count")
            self.bar_chart.axes.set_xlabel("Category")
        else:
            self.bar_chart.axes.text(0.5, 0.5, "No Data", horizontalalignment='center', verticalalignment='center')

        # Redraw charts
        self.pie_chart.draw()
        self.bar_chart.draw()
