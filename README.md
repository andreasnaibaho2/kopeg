# 🍵 Kopeg

Aplikasi web berbasis **Django** yang terhubung dengan **MongoDB** sebagai database utama. Project ini menggunakan struktur Django standar dengan tambahan koneksi ke MongoDB melalui PyMongo.

---

## 🛠️ Tech Stack

| Teknologi | Keterangan |
|-----------|------------|
| Python | Bahasa pemrograman utama |
| Django 4.2 | Framework web backend |
| MongoDB | Database NoSQL utama |
| PyMongo | Driver koneksi MongoDB untuk Python |
| Pandas | Pengolahan dan analisis data |
| SQLite | Database lokal (fallback/dev) |
| Gunicorn | WSGI server untuk deployment |
| python-dotenv | Manajemen environment variable |

---

## 📁 Struktur Project

```
kopeg/
├── kopeg/               # Aplikasi Django utama
├── mongodb_connection/  # Konfigurasi settings & koneksi MongoDB
├── assets/              # File aset statis
├── static/assets/       # File statis untuk frontend
├── media/               # File media yang diupload
├── db_connection.py     # Script koneksi database
├── manage.py            # CLI Django
├── requirements.txt     # Daftar dependensi Python
├── Pipfile              # Manajemen paket dengan Pipenv
└── db.sqlite3           # Database SQLite (development)
```

---

## ⚙️ Instalasi & Menjalankan Project

### Prasyarat

- Python 3.8+
- MongoDB (lokal atau MongoDB Atlas)
- pip atau pipenv

### 1. Clone Repository

```bash
git clone https://github.com/amamat20/kopeg.git
cd kopeg
```

### 2. Buat Virtual Environment

Menggunakan **pip**:
```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

Atau menggunakan **Pipenv**:
```bash
pipenv install
pipenv shell
```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment Variable

Buat file `.env` di root project dan isi dengan konfigurasi berikut:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
MONGO_URI=mongodb://localhost:27017/kopeg
```

> ⚠️ Jangan commit file `.env` ke repository!

### 5. Jalankan Migrasi

```bash
python manage.py migrate
```

### 6. Jalankan Development Server

```bash
python manage.py runserver
```

Akses aplikasi di: `http://127.0.0.1:8000`

---

## 🚀 Deployment

Untuk production, gunakan **Gunicorn** sebagai WSGI server:

```bash
gunicorn mongodb_connection.wsgi:application --bind 0.0.0.0:8000
```

---

## 📦 Dependensi Utama

```
Django==4.2
pymongo
pandas
dnspython
python-dotenv
gunicorn
```

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan ikuti langkah berikut:

1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b feature/nama-fitur`)
3. Commit perubahan (`git commit -m 'feat: tambah fitur baru'`)
4. Push ke branch (`git push origin feature/nama-fitur`)
5. Buat Pull Request

---

## 📄 Lisensi

Project ini bersifat open source. Silakan gunakan dan modifikasi sesuai kebutuhan.

---

> Dibuat dengan ❤️ oleh [amamat20](https://github.com/amamat20)
