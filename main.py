import sys

from database.db_init import initialize_database
from gui.login_window import LoginWindow
from gui.main_window import DataMatrixEncoder
from PyQt5.QtWidgets import QApplication, QDialog

if __name__ == "__main__":
    initialize_database()
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    if login_window.exec_() == QDialog.Accepted:
        window = DataMatrixEncoder()
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)
