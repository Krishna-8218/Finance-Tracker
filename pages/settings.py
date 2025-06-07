from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class SettingsPage(QWidget):
    def __init__(self, switch_callback, apply_theme_callback):
        super().__init__()

        self.apply_theme_callback = apply_theme_callback  # Function to apply the selected theme
        
        # Layout setup
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        # Inside SettingsPage's __init__ method
        save_button = QPushButton("Save Budgets")
        save_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        save_button.clicked.connect(self.save_budgets)
        layout.addWidget(save_button)

        # 🏷️ Title
        title = QLabel("🎨 Choose Your Theme")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #FFFFFF;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 🌑 Dark Mode Button
        dark_mode_btn = QPushButton("Dark Mode")
        dark_mode_btn.setStyleSheet("background-color: #222222; color: #FFFFFF; font-size: 16px; padding: 10px;")
        dark_mode_btn.clicked.connect(lambda: self.apply_theme("dark"))
        layout.addWidget(dark_mode_btn)

        # 🌕 Light Mode Button
        light_mode_btn = QPushButton("Light Mode")
        light_mode_btn.setStyleSheet("background-color: #FFFFFF; color: #222222; font-size: 16px; padding: 10px;")
        light_mode_btn.clicked.connect(lambda: self.apply_theme("light"))
        layout.addWidget(light_mode_btn)

        # 🌈 Gradient Theme Button
        gradient_btn = QPushButton("Gradient Theme")
        gradient_btn.setStyleSheet("background: linear-gradient(to right, #FF5733, #FFC300); color: #FFFFFF; font-size: 16px; padding: 10px;")
        gradient_btn.clicked.connect(lambda: self.apply_theme("gradient"))
        layout.addWidget(gradient_btn)

        # 🔙 Back to Dashboard Button
        back_btn = QPushButton("Back to Dashboard")
        back_btn.setStyleSheet("background-color: #666666; color: #FFFFFF; font-size: 16px; padding: 10px; border-radius: 5px;")
        back_btn.clicked.connect(lambda: switch_callback("Dashboard"))
        layout.addWidget(back_btn)

        # Apply layout
        self.setLayout(layout)
        
    def save_budgets(self):
        new_budgets = {}
        for category, field in self.budget_inputs.items():
            try:
                amount = float(field.text())
                new_budgets[category] = amount
            except ValueError:
                pass

        # ✅ Access the main window
        main_window = self.parent().parent().parent()  # adjust if your structure is different

        # ✅ Save budgets in memory and JSON
        main_window.budgets = new_budgets
        


    def apply_theme(self, theme):
        """Apply the selected theme across the application."""
        self.apply_theme_callback(theme)  # Call the main function to update UI