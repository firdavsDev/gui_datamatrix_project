# KarantinUz - Qadoqlash System

Bu loyiha qadoqlash jarayonlarini boshqarish uchun mo‘ljallangan dastur bo‘lib, DataMatrix kodlarini generatsiya qiladi, PDF va XML fayllar sifatida eksport qiladi. Dastur SQLite bazasidan foydalanadi va PyQt5 yordamida foydalanuvchi interfeysi (GUI) bilan ishlaydi.

## Loyiha tuzilmasi
```
datamatrix_project/
│
├── main.py                 # Asosiy ishga tushirish fayli
├── database/
│   ├── __init__.py         # database paketini ishga tushirish uchun
│   ├── db_init.py          # SQLite baza va jadvallarni yaratish
│   └── db_operations.py    # Baza bilan ishlash funksiyalari (saqlash, o‘qish)
├── gui/
│   ├── __init__.py         # gui paketini ishga tushirish uchun
│   ├── login_window.py     # Kirish oynasi
│   └── main_window.py      # Asosiy oyna (DataMatrixEncoder)
├── utils/
│   ├── __init__.py         # utils paketini ishga tushirish uchun
│   └── pdf_generator.py    # PDF generatsiya qilish funksiyalari
├── logo.png                # Login oynasi uchun logo
├── logo.ico                # Dastur ikonka fayli (Windows .exe uchun)
├── requirements.txt        # Kerakli kutubxonalar ro‘yxati
├── .gitignore              # Git versiya boshqaruvida e’tiborga olinmaydigan fayllar
└── README.md               # Loyiha haqida ma’lumot
```

## O‘rnatish

### 1. Python o‘rnatish
Loyiha Python 3.8 yoki undan yuqori versiyasini talab qiladi. Python’ni rasmiy saytdan o‘rnating: [python.org](https://www.python.org/downloads/).

### 2. Virtual muhit yaratish
```bash
python -m venv venv
source venv/bin/activate  # Windows uchun: venv\Scripts\activate
```

### 3. Kerakli kutubxonalar o‘rnatish
`requirements.txt` fayli yordamida barcha kerakli kutubxonalar o‘rnatiladi:
```bash
pip install -r requirements.txt
```

### 4. Logo va ikonka fayllarini joylashtirish
- `logo.png` faylini loyiha jildiga joylashtiring (login oynasi uchun).
- `logo.ico` faylini loyiha jildiga joylashtiring (Windows `.exe` uchun).

## Ishga tushirish

### Kod orqali ishga tushirish
```bash
cd datamatrix_project
python main.py
```
- Dastur login oynasi bilan ochiladi.
- Login: `admin`, Parol: `admin` bilan kirishingiz mumkin.

### .exe orqali ishga tushirish (Windows)
1. `.exe` faylini yaratish uchun `PyInstaller` o‘rnating:
   ```bash
   pip install pyinstaller
   ```
2. `.exe` faylini generatsiya qiling:
   ```bash
   pyinstaller --name "KarantinUz - Qadoqlash System" --icon logo.ico --onefile main.py
   ```
3. `dist/` jildida yaratilgan `KarantinUz - Qadoqlash System.exe` faylini ishga tushiring.

## Foydalanish
1. **Login oynasi**:
   - Default login: `admin`, parol: `admin`.
2. **Asosiy oyna**:
   - Qadoqlash va eksport qiluvchi korxona nomlarini kiriting.
   - Quti turi, o‘lchamlari, mahsulot turi va quti sonini tanlang.
   - "Save & Generate" tugmasi orqali PDF va XML fayllarni generatsiya qiling.
   - "Download as PDF" yoki "Download as XML" tugmalari orqali fayllarni yuklab oling.
3. **Contact with Admin**:
   - Telegram linki orqali admin bilan bog‘lanish mumkin: [Contact with Admin](https://t.me/davronbek_dev).

## Xususiyatlar
- **DataMatrix kod generatsiyasi**: Har bir quti uchun noyob 9 xonali kodlar yaratiladi.
- **PDF eksport**: Har bir sahifada markazda DataMatrix kodi bo‘lgan PDF fayl yaratiladi.
- **XML eksport**: Quti ma’lumotlari va DataMatrix kodlarini o‘z ichiga olgan XML fayl yaratiladi.
- **SQLite baza**: Ma’lumotlar SQLite bazasida saqlanadi.

## Talablar
- Python 3.8 yoki undan yuqori.
- Windows operatsion tizimi (`.exe` versiyasi uchun).
- `logo.png` va `logo.ico` fayllari.

## Muammolar bo‘lsa
- Agar logo ko‘rinmasa, `logo.png` faylining loyiha jildida ekanligini tekshiring.
- Agar `.exe` fayl ishlamasa, PyInstaller’ga qo‘shimcha sozlamalar qo‘shish kerak bo‘lishi mumkin:
  ```bash
  pyinstaller --name "KarantinUz - Qadoqlash System" --icon logo.ico --onefile --hidden-import pylibdmtx --hidden-import reportlab main.py
  ```

## Kontakt
Muammolar yuzaga kelsa, admin bilan bog‘laning: [Telegram](https://t.me/davronbek_dev).

## Muallif
DavronbekDev
