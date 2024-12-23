from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QFileDialog
import json

from src.environment_manager import EnvironmentManager


class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setObjectName("settingsWidget")

        # Variables to track mouse movement for dragging the window
        self.mouse_pos = QPoint()

        # Create Layout
        layout = QVBoxLayout()

        # Username field
        self.username_label = QLabel("Username:")
        self.username_edit = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)

        # Game directory field
        self.game_dir_label = QLabel("Game Directory:")
        self.game_dir_edit = QLineEdit()
        self.game_dir_button = QPushButton("Browse")
        self.game_dir_button.clicked.connect(self.browse_game_directory)
        layout.addWidget(self.game_dir_label)
        layout.addWidget(self.game_dir_edit)
        layout.addWidget(self.game_dir_button)

        # Theme color selection
        self.theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "System"])
        layout.addWidget(self.theme_label)
        layout.addWidget(self.theme_combo)

        # Language selection
        self.language_label = QLabel("Language:")
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English"])
        layout.addWidget(self.language_label)
        layout.addWidget(self.language_combo)

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)  # Simply close without saving
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

        # Load existing settings from JSON after UI elements are created
        self.config = EnvironmentManager()
        self.load_settings()

    def browse_game_directory(self):
        """Handle browsing for game directory"""
        folder = QFileDialog.getExistingDirectory(self, "Select Game Directory")
        if folder:
            self.game_dir_edit.setText(folder)

    def load_settings(self):
        """Load settings from JSON file and populate the fields."""
        env_manager = EnvironmentManager(f'resources/user_config.json')
        settings = env_manager.load_data()

        # Check if the settings exist, and if so, populate the fields
        if settings:
            # Update the UI fields with the loaded settings
            self.username_edit.setText(settings.get("username", ""))
            self.game_dir_edit.setText(settings.get("game_directory", ""))
            self.theme_combo.setCurrentText(settings.get("theme", ""))
            self.language_combo.setCurrentText(settings.get("language", ""))
        else:
            print("No settings found in the JSON file.")

    def save_settings(self):
        """Save settings to JSON file"""
        username = self.username_edit.text()
        game_directory = self.game_dir_edit.text()
        theme = self.theme_combo.currentText()
        language = self.language_combo.currentText()

        # Save the settings
        self.config.set('username', username)
        self.config.set('game_directory', game_directory)
        self.config.set('theme', theme)
        self.config.set('language', language)

        settings = {
            "username": username,
            "game_directory": game_directory,
            "theme": theme,
            "language": language,
        }

        # Save the merged settings back to JSON
        EnvironmentManager(f'resources/user_config.json').save_data(settings)

        print("Settings saved successfully.")

        # Close the widget
        self.close()

    def mousePressEvent(self, event):
        """Track the mouse position when the user clicks on the window"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        """Allow dragging the window when the mouse moves"""
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.mouse_pos
            self.move(self.pos() + delta)
            self.mouse_pos = event.globalPosition().toPoint()