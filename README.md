# 🛒 KOPEG — Sistem Manajemen Keuangan & Stok Toko

<p align="center">
  <img src="https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white"/>
  <img src="https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
</p>

<p align="center">
  Aplikasi web manajemen keuangan dan stok untuk toko kelontong / retail, 
  lengkap dengan dashboard analitik, prediksi stok, dan laporan bulanan.
</p>

---

## 📸 Preview Aplikasi

| Dashboard Utama | Upload Data |
|:-:|:-:|
| Ringkasan total pembelian, penjualan, retur, dan keuntungan | Upload file CSV/XLSX transaksi per bulan & tahun |

| Dashboard Bulanan | Prediksi Stok |
|:-:|:-:|
| Grafik batang & status untung/rugi per bulan | Prediksi kebutuhan stok bulan berikutnya |

---

## ✨ Fitur Utama

### 📊 Dashboard Utama
- Ringkasan total **Pembelian**, **Penjualan**, **Retur**, dan **Keuntungan**
- Grafik keuntungan per bulan (area chart interaktif)
- Pencarian produk berdasarkan nama / jenis

### 📁 Upload Data Transaksi
- Upload file **CSV/XLSX** untuk data Pembelian, Penjualan, Retur, dan Stok Opname
- Filter berdasarkan **bulan** dan **tahun**
- Proses upload batch sekaligus dalam satu form

### 📅 Dashboard Keuangan Bulanan
- Tampilan detail per bulan: Total Pembelian, Penjualan, Retur, Jumlah Item Stok
- **Status otomatis** — menampilkan apakah bulan tersebut Untung atau Rugi
- Grafik batang perbandingan nilai transaksi
- Fitur **Hapus Data** per bulan
- **Ekspor data ke CSV** langsung dari dashboard

### 📋 Tabel Perbulan
- **Pembelian Bulanan** — detail transaksi pembelian
- **Penjualan Bulanan** — detail transaksi penjualan
- **Retur Bulanan** — data retur produk
- **Stock Opname** — data stok fisik
- **Perbandingan Stok dan Stock Opname** — analisis selisih stok

### 🔮 Prediksi Stok
- Prediksi kebutuhan stok untuk **bulan berikutnya** per item
- Tampilan total kebutuhan stok keseluruhan
- Tabel detail prediksi per nama item (dalam satuan PCS)

---

## 🛠️ Tech Stack

| Layer | Teknologi |
|-------|-----------|
| **Backend** | Python, Django 4.2 |
| **Database** | MongoDB (PyMongo), SQLite |
| **Data Processing** | Pandas |
| **Frontend** | HTML, CSS, JavaScript |
| **Deployment** | Gunicorn |
| **Config** | python-dotenv |

---

## 📁 Struktur Project

```
kopeg/
├── kopeg/                   # Aplikasi Django utama (views, models, urls)
├── mongodb_connection/      # Konfigurasi settings & koneksi MongoDB
├── assets/                  # File aset statis
├── static/assets/           # CSS, JS, dan gambar frontend
├── media/                   # File media yang diupload pengguna
├── db_connection.py         # Script koneksi database MongoDB
├── manage.py                # Django CLI entry point
├── requirements.txt         # Daftar dependensi Python
├── Pipfile                  # Manajemen paket Pipenv
└── db.sqlite3               # Database SQLite (development)
```

---

## ⚙️ Instalasi & Menjalankan Project

### Prasyarat

- Python 3.8+
- MongoDB (lokal atau [MongoDB Atlas](https://www.mongodb.com/atlas))
- pip atau pipenv

### 1. Clone Repository

```bash
git clone https://github.com/amamat20/kopeg.git
cd kopeg
```

### 2. Buat Virtual Environment

**Menggunakan pip:**
```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

**Atau menggunakan Pipenv:**
```bash
pipenv install
pipenv shell
```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment Variable

Buat file `.env` di root project:

```env
SECRET_KEY=your_django_secret_key_here
DEBUG=True
MONGO_URI=mongodb://localhost:27017/kopeg
```

> ⚠️ **Jangan pernah commit file `.env` ke repository!**

### 5. Jalankan Migrasi

```bash
python manage.py migrate
```

### 6. Jalankan Server

```bash
python manage.py runserver
```

Buka browser dan akses: **`http://127.0.0.1:8000`**

---

## 🚀 Deployment (Production)

Gunakan **Gunicorn** sebagai WSGI server:

```bash
gunicorn mongodb_connection.wsgi:application --bind 0.0.0.0:8000
```

---

## 📦 Dependencies

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

1. **Fork** repository ini
2. Buat branch fitur baru
   ```bash
   git checkout -b feature/nama-fitur
   ```
3. Commit perubahan
   ```bash
   git commit -m "feat: tambah fitur baru"
   ```
4. Push ke branch
   ```bash
   git push origin feature/nama-fitur
   ```
5. Buat **Pull Request**

---

## 📄 Lisensi

Didistribusikan di bawah lisensi MIT. Lihat `LICENSE` untuk informasi lebih lanjut.

---

<p align="center">
  Dibuat dengan ❤️ oleh <a href="https://github.com/amamat20">amamat20</a>
  <br/>
  ⭐ Jangan lupa kasih bintang kalau project ini membantu!
</p>
