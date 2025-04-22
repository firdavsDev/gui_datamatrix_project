import os
import random

from database.db_operations import save_datamatrix_code
from PIL import Image
from pylibdmtx.pylibdmtx import encode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_pdf(pdf_path, box_count, box_id, conn, cursor):
    c = canvas.Canvas(pdf_path, pagesize=A4)
    page_width, page_height = A4

    for i in range(box_count):
        # Noyob ID generatsiyasi (9 xonali raqam)
        unique_id = str(random.randint(100000000, 999999999))

        # Bazaga saqlash
        save_datamatrix_code(conn, cursor, box_id, unique_id)

        # DataMatrix kodi yaratish
        encoded = encode(unique_id.encode("utf-8"))
        img = Image.frombytes("RGB", (encoded.width, encoded.height), encoded.pixels)
        img = img.resize((150, 150), Image.Resampling.LANCZOS)

        # PDF sahifasiga joylashtirish (markazda)
        img.save("temp.png")
        x = (page_width - 150 * 2.83465) / 2
        y = (page_height - 150 * 2.83465) / 2
        c.drawImage("temp.png", x, y, 150 * 2.83465, 150 * 2.83465)
        c.showPage()

    c.save()
    os.remove("temp.png")
