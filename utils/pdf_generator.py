import os
import time

from PIL import Image
from pylibdmtx.pylibdmtx import encode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_pdf(pdf_path, unique_ids):
    c = canvas.Canvas(pdf_path, pagesize=A4)
    page_width, page_height = A4

    for i, unique_id in enumerate(unique_ids):
        # Har bir iteratsiyada noyob vaqtinchalik fayl nomi
        temp_file = f"temp_{i}_{int(time.time() * 1000)}.png"

        # DataMatrix kodi yaratish
        encoded = encode(unique_id.encode("utf-8"))
        if encoded is None:
            print(f"Error: DataMatrix kodi yaratilmadi, unique_id: {unique_id}")
            continue

        img = Image.frombytes("RGB", (encoded.width, encoded.height), encoded.pixels)
        img = img.resize((150, 150), Image.Resampling.LANCZOS)

        # Vaqtinchalik faylga saqlash
        img.save(temp_file)

        # PDF sahifasiga joylashtirish (markazda)
        x = (page_width - 150 * 2.83465) / 2
        y = (page_height - 150 * 2.83465) / 2
        c.drawImage(temp_file, x, y, 150 * 2.83465, 150 * 2.83465)
        c.showPage()

        # Vaqtinchalik faylni o‘chirish
        os.remove(temp_file)

    c.save()
    print(f"PDF fayli yaratildi: {pdf_path}")
