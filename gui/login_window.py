from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from database.db_operations import check_user_credentials


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KarantinUz - Kirish")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.resize(500, 350)  # Logo uchun balandlikni oshirdik
        self.center()
        self.initUI()

    def center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def initUI(self):
        main_layout = QVBoxLayout()

        # Logo qo‘shish
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("logo.png")
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(
                150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            logo_label.setPixmap(logo_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
        else:
            logo_label.setText("Logo topilmadi!")
        main_layout.addWidget(logo_label)

        # Form layout
        layout = QFormLayout()

        # Login kiritish maydoni
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Login")
        layout.addRow("Login:", self.login_input)

        # Parol kiritish maydoni
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addRow("Password:", self.password_input)

        # Kirish tugmasi
        self.login_button = QPushButton("Kirish")
        self.login_button.clicked.connect(self.check_credentials)
        layout.addWidget(self.login_button)

        # Markazlashtirish uchun widget va layout
        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.addStretch()
        central_layout.addLayout(layout)
        central_layout.addStretch()

        main_layout.addWidget(central_widget)
        self.setLayout(main_layout)

    def check_credentials(self):
        login = self.login_input.text()
        password = self.password_input.text()

        if check_user_credentials(login, password):
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Noto‘g‘ri login yoki parol!")
