"""
Chemical Equipment Visualizer - Desktop Application
Main entry point
"""
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from api_client import APIClient
from login_dialog import LoginDialog
from main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Chemical Equipment Visualizer')
    app.setOrganizationName('Chemical Equipment Viz')
    
    # Create API client
    api_client = APIClient()
    
    # Show login dialog
    login_dialog = LoginDialog(api_client)
    
    if login_dialog.exec_() == LoginDialog.Accepted:
        # Login successful, show main window
        main_window = MainWindow(api_client, login_dialog.user_data)
        main_window.show()
        
        sys.exit(app.exec_())
    else:
        # Login cancelled
        sys.exit(0)


if __name__ == '__main__':
    main()
