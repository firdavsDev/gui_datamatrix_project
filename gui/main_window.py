import os
import sqlite3
import xml.etree.ElementTree as ET

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from database.db_operations import (
    get_box_types,
    get_products,
    save_box_data,
)
from utils.pdf_generator import generate_pdf


class DataMatrixEncoder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KarantinUz - DataMatrix Encoder")
        self.resize(800, 600)
        self.center()
        self.pdf_path = None
        self.xml_path = None
        self.initUI()

    def center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Chap taraf: Input maydonlari
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # Qadoqlash korxona nomi
        self.packaging_company_label = QLabel("Qadoqlash korxona nomi:")
        self.packaging_company_input = QLineEdit()
        left_layout.addWidget(self.packaging_company_label)
        left_layout.addWidget(self.packaging_company_input)

        # Eksport qiluvchi korxona nomi
        self.export_company_label = QLabel("Eksport qiluvchi korxona nomi:")
        self.export_company_input = QLineEdit()
        left_layout.addWidget(self.export_company_label)
        left_layout.addWidget(self.export_company_input)

        # Quti turi (ComboBox)
        self.box_type_label = QLabel("Quti turi:")
        self.box_type_input = QComboBox()
        box_types = get_box_types()
        for box_type in box_types:
            self.box_type_input.addItem(box_type)
        left_layout.addWidget(self.box_type_label)
        left_layout.addWidget(self.box_type_input)

        # Quti o‘lchamlari
        self.width_label = QLabel("Quti eni (sm):")
        self.width_input = QSpinBox()
        self.width_input.setRange(1, 1000)
        self.width_input.setValue(10)
        left_layout.addWidget(self.width_label)
        left_layout.addWidget(self.width_input)

        self.height_label = QLabel("Quti bo‘yi (sm):")
        self.height_input = QSpinBox()
        self.height_input.setRange(1, 1000)
        self.height_input.setValue(10)
        left_layout.addWidget(self.height_label)
        left_layout.addWidget(self.height_input)

        # Mahsulot turi (ComboBox)
        self.product_label = QLabel("Mahsulot turi:")
        self.product_input = QComboBox()
        products = get_products()
        for product in products:
            self.product_input.addItem(product)
        left_layout.addWidget(self.product_label)
        left_layout.addWidget(self.product_input)

        # Quti soni
        self.box_count_label = QLabel("Quti soni (10,000 dan kam):")
        self.box_count_input = QSpinBox()
        self.box_count_input.setRange(1, 9999)
        self.box_count_input.setValue(1)
        left_layout.addWidget(self.box_count_label)
        left_layout.addWidget(self.box_count_input)

        # Save & Generate tugmasi
        self.generate_button = QPushButton("Save & Generate")
        self.generate_button.clicked.connect(self.save_and_generate)
        left_layout.addWidget(self.generate_button)

        # O‘ng taraf: Xabar oynasi va link
        self.message_label = QLabel(
            "PDF generatsiya qilish uchun ma’lumotlarni kiriting."
        )
        self.message_label.setAlignment(Qt.AlignCenter)

        # Contact with Admin linki
        self.contact_link = QLabel(
            '<a href="https://t.me/davronbek_dev">Contact with Admin</a>'
        )
        self.contact_link.setOpenExternalLinks(True)
        self.contact_link.setAlignment(Qt.AlignCenter)

        # Download tugmalari
        button_layout = QHBoxLayout()
        self.download_pdf_button = QPushButton("Download as PDF")
        self.download_pdf_button.clicked.connect(self.download_pdf)
        self.download_pdf_button.setEnabled(False)
        self.download_xml_button = QPushButton("Download as XML")
        self.download_xml_button.clicked.connect(self.download_xml)
        self.download_xml_button.setEnabled(False)
        button_layout.addWidget(self.download_pdf_button)
        button_layout.addWidget(self.download_xml_button)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.message_label)
        right_layout.addWidget(self.contact_link)
        right_layout.addLayout(button_layout)

        # Main layoutga qo‘shish
        main_layout.addWidget(left_widget)
        main_layout.addLayout(right_layout)

    def save_and_generate(self):
        # Inputlarni olish
        packaging_company = self.packaging_company_input.text()
        export_company = self.export_company_input.text()
        box_type = self.box_type_input.currentText()
        width = self.width_input.value()
        height = self.height_input.value()
        product = self.product_input.currentText()
        box_count = self.box_count_input.value()

        # Validatsiya
        if not packaging_company or not export_company:
            QMessageBox.warning(
                self, "Error", "Iltimos, barcha maydonlarni to‘ldiring!"
            )
            return
        if box_count > 10000:
            QMessageBox.warning(
                self, "Error", "Quti soni 10,000 dan kam bo‘lishi kerak!"
            )
            return

        # Bazaga saqlash
        conn, cursor, box_id = save_box_data(
            packaging_company,
            export_company,
            box_type,
            width,
            height,
            product,
            box_count,
        )

        # PDF generatsiya qilish
        pdf_path = "output_datamatrix.pdf"
        generate_pdf(pdf_path, box_count, box_id, conn, cursor)

        # XML generatsiya qilish
        self.generate_xml(
            box_id,
            packaging_company,
            export_company,
            box_type,
            width,
            height,
            product,
            box_count,
        )

        # Xabar ko‘rsatish
        self.pdf_path = pdf_path
        self.download_pdf_button.setEnabled(True)
        self.download_xml_button.setEnabled(True)
        self.message_label.setText(
            "PDF va XML tayyor! Yuklab olish uchun tugmalarni bosing."
        )

    def generate_xml(
        self,
        box_id,
        packaging_company,
        export_company,
        box_type,
        width,
        height,
        product,
        box_count,
    ):
        # XML root elementi
        root = ET.Element("BoxData")

        # Box ma’lumotlari
        box_info = ET.SubElement(root, "BoxInfo")
        ET.SubElement(box_info, "PackagingCompany").text = packaging_company
        ET.SubElement(box_info, "ExportCompany").text = export_company
        ET.SubElement(box_info, "BoxType").text = box_type
        ET.SubElement(box_info, "Width").text = str(width)
        ET.SubElement(box_info, "Height").text = str(height)
        ET.SubElement(box_info, "Product").text = product
        ET.SubElement(box_info, "BoxCount").text = str(box_count)

        # DataMatrix kodlari
        codes = ET.SubElement(root, "DataMatrixCodes")
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT unique_id FROM datamatrix_codes WHERE box_id = ?", (box_id,)
        )
        datamatrix_codes = cursor.fetchall()
        for code in datamatrix_codes:
            code_elem = ET.SubElement(codes, "Code")
            code_elem.text = code[0]
        conn.close()

        # XML faylga saqlash
        tree = ET.ElementTree(root)
        self.xml_path = "output_datamatrix.xml"
        tree.write(self.xml_path, encoding="utf-8", xml_declaration=True)

    def download_pdf(self):
        if self.pdf_path:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save PDF", "", "PDF Files (*.pdf)"
            )
            if file_path:
                os.rename(self.pdf_path, file_path)
                self.pdf_path = None
                self.download_pdf_button.setEnabled(False)
                if not self.xml_path:
                    self.message_label.setText(
                        "PDF yuklab olindi. Yangi PDF generatsiya qiling."
                    )
                    self.download_xml_button.setEnabled(False)

    def download_xml(self):
        if self.xml_path:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save XML", "", "XML Files (*.xml)"
            )
            if file_path:
                os.rename(self.xml_path, file_path)
                self.xml_path = None
                self.download_xml_button.setEnabled(False)
                if not self.pdf_path:
                    self.message_label.setText(
                        "XML yuklab olindi. Yangi fayllar generatsiya qiling."
                    )
                    self.download_pdf_button.setEnabled(False)
