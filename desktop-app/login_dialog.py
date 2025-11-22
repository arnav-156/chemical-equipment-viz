"""
Login Dialog for Chemical Equipment Visualizer
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QTabWidget, QWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from api_client import APIClient


class LoginDialog(QDialog):
    login_successful = pyqtSignal(dict)  # Emits user data on successful login
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.user_data = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Visualizer - Login')
        self.setFixedSize(400, 350)
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('🧪 Chemical Equipment Visualizer')
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Tab widget for Login/Register
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_login_tab(), 'Login')
        self.tabs.addTab(self.create_register_tab(), 'Register')
        layout.addWidget(self.tabs)
        
        self.setLayout(layout)
    
    def create_login_tab(self):
        """Create login tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Username
        layout.addWidget(QLabel('Username:'))
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText('Enter username')
        layout.addWidget(self.login_username)
        
        # Password
        layout.addWidget(QLabel('Password:'))
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setPlaceholderText('Enter password')
        self.login_password.returnPressed.connect(self.handle_login)
        layout.addWidget(self.login_password)
        
        # Login button
        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.handle_login)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
        """)
        layout.addWidget(login_btn)
        
        # Test credentials
        test_creds = QLabel('Test Credentials:\nUsername: testuser\nPassword: testpass123')
        test_creds.setStyleSheet('color: #666; font-size: 11px; margin-top: 10px;')
        test_creds.setAlignment(Qt.AlignCenter)
        layout.addWidget(test_creds)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_register_tab(self):
        """Create register tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Username
        layout.addWidget(QLabel('Username:'))
        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText('Choose username')
        layout.addWidget(self.reg_username)
        
        # Email
        layout.addWidget(QLabel('Email (optional):'))
        self.reg_email = QLineEdit()
        self.reg_email.setPlaceholderText('your@email.com')
        layout.addWidget(self.reg_email)
        
        # Password
        layout.addWidget(QLabel('Password:'))
        self.reg_password = QLineEdit()
        self.reg_password.setEchoMode(QLineEdit.Password)
        self.reg_password.setPlaceholderText('At least 6 characters')
        layout.addWidget(self.reg_password)
        
        # Confirm Password
        layout.addWidget(QLabel('Confirm Password:'))
        self.reg_confirm = QLineEdit()
        self.reg_confirm.setEchoMode(QLineEdit.Password)
        self.reg_confirm.setPlaceholderText('Re-enter password')
        self.reg_confirm.returnPressed.connect(self.handle_register)
        layout.addWidget(self.reg_confirm)
        
        # Register button
        register_btn = QPushButton('Register')
        register_btn.clicked.connect(self.handle_register)
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(register_btn)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def handle_login(self):
        """Handle login button click"""
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password')
            return
        
        try:
            data = self.api_client.login(username, password)
            self.user_data = data
            self.login_successful.emit(data)
            self.accept()
        except requests.exceptions.RequestException as e:
            error_msg = 'Login failed. Please check your credentials.'
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('error', error_msg)
                except:
                    pass
            QMessageBox.critical(self, 'Login Failed', error_msg)
    
    def handle_register(self):
        """Handle register button click"""
        username = self.reg_username.text().strip()
        email = self.reg_email.text().strip()
        password = self.reg_password.text()
        confirm = self.reg_confirm.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Username and password are required')
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, 'Error', 'Password must be at least 6 characters')
            return
        
        if password != confirm:
            QMessageBox.warning(self, 'Error', 'Passwords do not match')
            return
        
        try:
            data = self.api_client.register(username, password, email)
            self.user_data = data
            self.login_successful.emit(data)
            self.accept()
        except requests.exceptions.RequestException as e:
            error_msg = 'Registration failed. Please try again.'
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('error', error_msg)
                except:
                    pass
            QMessageBox.critical(self, 'Registration Failed', error_msg)


import requests
