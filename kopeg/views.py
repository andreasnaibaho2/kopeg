from django.shortcuts import render, redirect
from django.http import HttpResponse
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.core.paginator import Paginator
import csv, io, os
from datetime import datetime
import pandas as pd
from bson.decimal128 import Decimal128
from io import StringIO
from django.urls import reverse
from collections import defaultdict

# Koneksi ke MongoDB lokal
client = MongoClient('mongodb+srv://bayu000111222:bayu123@testcluster.o7txczn.mongodb.net/')
db = client['db_kopeg']  # nama database kamu

# Koleksi
pembelian_collection = db['pembelian_array']
penjualan_collection = db['penjualan_array']
pembelian = list(db['pembelian_perbulan'].find())

retur_collection = db['retur_array']

# Halaman awal
def index(request):
    return HttpResponse("<h1>Aplikasi Koperasi (Kopeg) Terhubung ke MongoDB!</h1>")

# -------------------------------
# PEMBELIAN
# -------------------------------
def get_all_pembelian(request):
    query = request.GET.get('q', '')
    min_harga = request.GET.get('min_harga', '')
    filters = {}

    if query:
        filters['$or'] = [
            {"Nama_Item": {"$regex": query, "$options": "i"}},
            {"Jenis": {"$regex": query, "$options": "i"}},
            {"Bulan": {"$regex": query, "$options": "i"}},
            {"Tahun": {"$regex": query, "$options": "i"}},
        ]

    if min_harga:
        try:
            min_harga = int(min_harga)
            filters["Total_Harga"] = {"$gt": min_harga}
        except ValueError:
            pass  # kalau input bukan angka, abaikan saja
        
    data = list(pembelian_collection.find(filters))
    for item in data:
        item['id'] = str(item['_id'])
        del item['_id']
        
    # Pagination
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_data = pembelian_collection.count_documents({})
    filtered_count = len(data)

    context = {
        'pembelian': page_obj,
        'total_data': total_data,
        'filtered_count': filtered_count,
        'query': query,
        'min_harga': min_harga,
        'page_obj' : page_obj
    }
    return render(request, 'pembelian_list.html', context)

# ============================
# CREATE
# ============================
def add_pembelian(request):
    if request.method == 'POST':
        new_data = {
            "Kode_Item": request.POST['Kode_Item'],
            "Nama_Item": request.POST['Nama_Item'],
            "Jenis": request.POST['Jenis'],
            "Jumlah": int(request.POST['Jumlah']),
            "Satuan": request.POST['Satuan'],
            "Total_Harga": int(request.POST['Total_Harga']),
            "Bulan": request.POST['Bulan'],
            "Tahun": request.POST['Tahun'],
        }
        pembelian_collection.insert_one(new_data)
        return redirect('get_all_pembelian')
    return render(request, 'pembelian_add.html')

# ============================
# UPDATE
# ============================
def edit_pembelian(request, pembelian_id):
    pembelian = pembelian_collection.find_one({'_id': ObjectId(pembelian_id)})
    if not pembelian:
        return HttpResponse("Data tidak ditemukan.")

    if request.method == 'POST':
        updated_data = {
            "Kode_Item": request.POST['Kode_Item'],
            "Nama_Item": request.POST['Nama_Item'],
            "Jenis": request.POST['Jenis'],
            "Jumlah": int(request.POST['Jumlah']),
            "Satuan": request.POST['Satuan'],
            "Total_Harga": int(request.POST['Total_Harga']),
            "Bulan": request.POST['Bulan'],
            "Tahun": request.POST['Tahun'],
        }
        pembelian_collection.update_one({'_id': ObjectId(pembelian_id)}, {'$set': updated_data})
        return redirect('get_all_pembelian')

    pembelian['id'] = str(pembelian['_id'])
    return render(request, 'pembelian_edit.html', {'pembelian': pembelian})

# ============================
# DELETE
# ============================
def delete_pembelian(request, pembelian_id):
    # Hapus data
    pembelian_collection.delete_one({'_id': ObjectId(pembelian_id)})

    # Ambil nomor halaman dari query string
    current_page = request.GET.get('page', '1')

    # Redirect balik ke halaman semula
    return redirect(f"{reverse('get_all_pembelian')}?page={current_page}")

# -------------------------------
# PENJUALAN
# -------------------------------
def get_all_penjualan(request):
    query = request.GET.get('q', '')
    min_harga = request.GET.get('min_harga', '')
    filters = {}

    if query:
        filters['$or'] = [
            {"Nama_Item": {"$regex": query, "$options": "i"}},
            {"Jenis": {"$regex": query, "$options": "i"}},
            {"Bulan": {"$regex": query, "$options": "i"}},
            {"Tahun": {"$regex": query, "$options": "i"}},
        ]

    if min_harga:
        try:
            min_harga = int(min_harga)
            filters["Total_Harga"] = {"$gt": min_harga}
        except ValueError:
            pass

    data = list(penjualan_collection.find(filters))
    for item in data:
        item['id'] = str(item['_id'])
        del item['_id']

    paginator = Paginator(data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_data = penjualan_collection.count_documents({})
    filtered_count = len(data)

    context = {
        'penjualan': page_obj,
        'total_data': total_data,
        'filtered_count': filtered_count,
        'query': query,
        'min_harga': min_harga,
        'page_obj': page_obj,
    }
    return render(request, 'penjualan_list.html', context)

# ============================
# CREATE
# ============================
def add_penjualan(request):
    if request.method == 'POST':
        new_data = {
            "Kode_Item": request.POST['Kode_Item'],
            "Nama_Item": request.POST['Nama_Item'],
            "Jenis": request.POST['Jenis'],
            "Jumlah": int(request.POST['Jumlah']),
            "Satuan": request.POST['Satuan'],
            "Total_Harga": int(request.POST['Total_Harga']),
            "Bulan": request.POST['Bulan'],
            "Tahun": request.POST['Tahun'],
        }
        penjualan_collection.insert_one(new_data)
        return redirect('get_all_penjualan')
    return render(request, 'penjualan_add.html')

# ============================
# UPDATE
# ============================
def edit_penjualan(request, penjualan_id):
    penjualan = penjualan_collection.find_one({'_id': ObjectId(penjualan_id)})
    if not penjualan:
        return HttpResponse("Data tidak ditemukan.")

    if request.method == 'POST':
        updated_data = {
            "Kode_Item": request.POST['Kode_Item'],
            "Nama_Item": request.POST['Nama_Item'],
            "Jenis": request.POST['Jenis'],
            "Jumlah": int(request.POST['Jumlah']),
            "Satuan": request.POST['Satuan'],
            "Total_Harga": int(request.POST['Total_Harga']),
            "Bulan": request.POST['Bulan'],
            "Tahun": request.POST['Tahun'],
        }
        penjualan_collection.update_one({'_id': ObjectId(penjualan_id)}, {'$set': updated_data})
        return redirect('get_all_penjualan')

    penjualan['id'] = str(penjualan['_id'])
    return render(request, 'penjualan_edit.html', {'penjualan': penjualan})

# ============================
# DELETE
# ============================
def delete_penjualan(request, penjualan_id):
    penjualan_collection.delete_one({'_id': ObjectId(penjualan_id)})
    current_page = request.GET.get('page', '1')
    return redirect(f"{reverse('get_all_penjualan')}?page={current_page}")

# -------------------------------
# RETUR
# -------------------------------
def get_all_retur(request):
    query = request.GET.get('q', '')
    min_harga = request.GET.get('min_harga', '')
    filters = {}

    # 🔹 Fitur pencarian
    if query:
        filters['$or'] = [
            {"Nama_Item": {"$regex": query, "$options": "i"}},
            {"Kode_Item": {"$regex": query, "$options": "i"}},
            {"Bulan": {"$regex": query, "$options": "i"}},
            {"Tahun": {"$regex": query, "$options": "i"}},
        ]

    # 🔹 Filter harga minimum
    if min_harga:
        try:
            min_harga = int(min_harga)
            filters["Total_Harga"] = {"$gt": min_harga}
        except ValueError:
            pass

    data = list(retur_collection.find(filters))
    for item in data:
        if "Pot. %" in item:
            item["Potongan"] = item["Pot. %"]
            del item["Pot. %"]
        item["id"] = str(item["_id"])
        del item["_id"]

    # 🔹 Pagination
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_data = retur_collection.count_documents({})
    filtered_count = len(data)

    context = {
        "retur": page_obj,
        "total_data": total_data,
        "filtered_count": filtered_count,
        "query": query,
        "min_harga": min_harga,
        "page_obj": page_obj,
    }
    return render(request, "retur_list.html", context)


# ============================
# CREATE
# ============================
def add_retur(request):
    if request.method == "POST":
        new_data = {
            "Kode_Item": request.POST.get("Kode_Item"),
            "Nama_Item": request.POST.get("Nama_Item"),
            "Jml": int(request.POST.get("Jml", 0)),
            "Satuan": request.POST.get("Satuan"),
            "Harga": int(request.POST.get("Harga", 0)),
            "Pot. %": float(request.POST.get("Potongan", 0)),
            "Total_Harga": int(request.POST.get("Total_Harga", 0)),
            "Bulan": request.POST.get("Bulan"),
            "Tahun": request.POST.get("Tahun"),
        }
        retur_collection.insert_one(new_data)
        return redirect("get_all_retur")

    return render(request, "retur_add.html")


# ============================
# UPDATE
# ============================
def edit_retur(request, retur_id):
    retur = retur_collection.find_one({"_id": ObjectId(retur_id)})
    if not retur:
        return HttpResponse("Data tidak ditemukan.")

    if request.method == "POST":
        updated_data = {
            "Kode_Item": request.POST.get("Kode_Item"),
            "Nama_Item": request.POST.get("Nama_Item"),
            "Jml": int(request.POST.get("Jml", 0)),
            "Satuan": request.POST.get("Satuan"),
            "Harga": int(request.POST.get("Harga", 0)),
            "Pot. %": float(request.POST.get("Potongan", 0)),
            "Total_Harga": int(request.POST.get("Total_Harga", 0)),
            "Bulan": request.POST.get("Bulan"),
            "Tahun": request.POST.get("Tahun"),
        }
        retur_collection.update_one({"_id": ObjectId(retur_id)}, {"$set": updated_data})
        return redirect("get_all_retur")

    # ubah nama key Pot. % agar bisa ditampilkan di form edit
    if "Pot. %" in retur:
        retur["Potongan"] = retur["Pot. %"]
        del retur["Pot. %"]

    retur["id"] = str(retur["_id"])
    return render(request, "retur_edit.html", {"retur": retur})


# ============================
# DELETE
# ============================
def delete_retur(request, retur_id):
    # Hapus data
    retur_collection.delete_one({"_id": ObjectId(retur_id)})

    # Ambil nomor halaman dari query string agar bisa kembali ke halaman sebelumnya
    current_page = request.GET.get("page", "1")

    # Redirect balik ke halaman semula
    return redirect(f"{reverse('get_all_retur')}?page={current_page}")


def upload_perbulan(request):
    message = ''
    bulan_terpilih = None
    tahun_terpilih = None

    daftar_bulan = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    daftar_tahun = ["2023", "2024", "2025"]

    if request.method == 'POST':
        bulan_terpilih = request.POST.get('bulan')
        tahun_terpilih = request.POST.get('tahun')

        def baca_csv_aman(file_obj):
            """Baca CSV dengan deteksi delimiter otomatis (',' atau ';')."""
            try:
                sample = file_obj.read(1024).decode('utf-8')
                file_obj.seek(0)
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                df = pd.read_csv(file_obj, delimiter=delimiter)
            except Exception:
                file_obj.seek(0)
                df = pd.read_csv(file_obj, sep=';')
            return df

        # ---------------- PEMBELIAN ----------------
        pembelian_file = request.FILES.get('pembelian_csv')
        if pembelian_file:
            df = baca_csv_aman(pembelian_file)
            df['Bulan'] = bulan_terpilih
            df['Tahun'] = tahun_terpilih
            data = df.to_dict('records')
            db['pembelian_perbulan'].insert_many(data)
            message += f"✅ {len(data)} data pembelian berhasil disimpan.<br>"

        # ---------------- PENJUALAN ----------------
        penjualan_file = request.FILES.get('penjualan_csv')
        if penjualan_file:
            df = baca_csv_aman(penjualan_file)
            df['Bulan'] = bulan_terpilih
            df['Tahun'] = tahun_terpilih
            data = df.to_dict('records')
            db['penjualan_perbulan'].insert_many(data)
            message += f"✅ {len(data)} data penjualan berhasil disimpan.<br>"

        # ---------------- RETUR ----------------
        # ---------------- RETUR ----------------
        retur_file = request.FILES.get('retur_file')
        if retur_file:
            if retur_file.name.endswith('.csv'):
                df = baca_csv_aman(retur_file)
            else:
                df = pd.read_excel(retur_file)

            # 🔹 Hapus kolom "Unnamed" otomatis
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            # 🔹 Pastikan kolom nama bersih tanpa spasi tambahan
            df.columns = df.columns.str.strip()

            df['Bulan'] = bulan_terpilih
            df['Tahun'] = tahun_terpilih
            data = df.to_dict('records')
            db['retur_perbulan'].insert_many(data)
            message += f"✅ {len(data)} data retur berhasil disimpan.<br>"

        # ---------------- STOK OPNAME ----------------
        stok_file = request.FILES.get('stok_file')
        if stok_file:
            df = pd.read_excel(stok_file, header=None)
            header_row_index = None
            for i, row in df.iterrows():
                if any(str(cell).strip().lower() == "kode barcode" for cell in row):
                    header_row_index = i
                    break

            if header_row_index is not None:
                df.columns = df.iloc[header_row_index]
                df = df[header_row_index + 1:]
            else:
                df.columns = ["Kode Barcode", "Stok Fisik", "Nama Barang"]

            df = df.dropna(subset=["Stok Fisik"])
            df["Stok Fisik"] = pd.to_numeric(df["Stok Fisik"], errors="coerce").fillna(0)
            df["Bulan"] = bulan_terpilih
            df["Tahun"] = tahun_terpilih

            data = df.to_dict(orient="records")
            db["stok_perbulan"].insert_many(data)
            message += f"✅ {len(data)} data stok opname berhasil disimpan.<br>"

    context = {
        'message': message,
        'daftar_bulan': daftar_bulan,
        'daftar_tahun': daftar_tahun,
        'bulan_terpilih': bulan_terpilih,
        'tahun_terpilih': tahun_terpilih,
    }
    return render(request, 'upload_perbulan.html', context)


def dashboard(request):
    message = ''
    daftar_bulan = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    daftar_tahun = ["2023", "2024", "2025"]

    # 🔹 Fungsi bantu agar konversi angka aman
    def safe_float(value):
        try:
            if isinstance(value, str):
                # Hilangkan titik, koma, spasi, dan ubah ke float
                value = value.replace('.', '').replace(',', '').strip()
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    # 🔹 Jika tombol hapus ditekan
    if request.method == 'POST' and 'hapus_bulan' in request.POST:
        bulan_hapus = request.POST.get('hapus_bulan')
        tahun_hapus = request.POST.get('hapus_tahun')
        deleted = hapus_data_bulan(bulan_hapus, tahun_hapus)
        message = f"🗑️ {deleted} data dari {bulan_hapus} {tahun_hapus} berhasil dihapus."
        return render(request, 'dashboard.html', {
            'message': message,
            'daftar_bulan': daftar_bulan,
            'daftar_tahun': daftar_tahun,
            'bulan_terpilih': bulan_hapus,
            'tahun_terpilih': tahun_hapus
        })

    bulan_terpilih = request.GET.get('bulan')
    tahun_terpilih = request.GET.get('tahun')
    data_statistik = {}
    chart_data = {}

    if bulan_terpilih and tahun_terpilih:
        filter_query = {'Bulan': bulan_terpilih, 'Tahun': tahun_terpilih}

        # 🔹 Hitung total pembelian, penjualan, retur (dikali 1000 biar ribuan)
        total_pembelian = sum(
            safe_float(d.get('Total Harga', 0))
            for d in db['pembelian_perbulan'].find(filter_query)
        )
        total_penjualan = sum(
            safe_float(d.get('Total Harga', 0))
            for d in db['penjualan_perbulan'].find(filter_query)
        )
        total_retur = sum(
            safe_float(d.get('Total', 0)) * 1000
            for d in db['retur_perbulan'].find(filter_query)
        )

        # 🔹 Hitung jumlah stok fisik (bukan jumlah baris)
        stok_cursor = db['stok_perbulan'].find(filter_query)
        total_stok = 0
        for d in stok_cursor:
            try:
                total_stok += float(d.get('Stok Fisik', 0))
            except (ValueError, TypeError):
                continue

        # 🔹 Hitung keuntungan / kerugian
        keuntungan = total_penjualan - (total_pembelian + total_retur)
        status_keuangan = "Untung" if keuntungan >= 0 else "Rugi"

        data_statistik = {
            'total_pembelian': total_pembelian,
            'total_penjualan': total_penjualan,
            'total_retur': total_retur,
            'total_stok': total_stok,
            'keuntungan': keuntungan,
            'status_keuangan': status_keuangan
        }

        chart_data = {
            'labels': ['Pembelian', 'Penjualan', 'Retur'],
            'values': [total_pembelian, total_penjualan, total_retur]
        }

    context = {
        'daftar_bulan': daftar_bulan,
        'daftar_tahun': daftar_tahun,
        'bulan_terpilih': bulan_terpilih,
        'tahun_terpilih': tahun_terpilih,
        'data_statistik': data_statistik,
        'chart_data': chart_data,
        'message': message
    }

    return render(request, 'dashboard.html', context)


def hapus_data_bulan(bulan, tahun):
    collections = [
        'pembelian_perbulan',
        'penjualan_perbulan',
        'retur_perbulan',
        'stok_perbulan'
    ]
    total_deleted = 0

    for col in collections:
        result = db[col].delete_many({'Bulan': bulan, 'Tahun': tahun})
        total_deleted += result.deleted_count

    return total_deleted


def export_data_csv(request):
    """Gabungkan semua data bulanan ke satu file CSV"""
    collections = {
        "Pembelian": "pembelian_perbulan",
        "Penjualan": "penjualan_perbulan",
        "Retur": "retur_perbulan",
        "Stok": "stok_perbulan"
    }

    all_dataframes = []

    for label, col_name in collections.items():
        cursor = db[col_name].find()
        df = pd.DataFrame(list(cursor))

        if not df.empty:
            df["Jenis_Data"] = label
            # Bersihkan kolom _id
            if "_id" in df.columns:
                df = df.drop(columns=["_id"])
            all_dataframes.append(df)

    if not all_dataframes:
        return HttpResponse("⚠️ Tidak ada data untuk diekspor.", content_type="text/plain")

    df_all = pd.concat(all_dataframes, ignore_index=True)

    # Bersihkan nilai #N/A, ubah NaN jadi kosong
    df_all = df_all.replace(["#N/A", "NaN", None, float('nan')], "")

    # Simpan ke buffer CSV
    buffer = StringIO()
    df_all.to_csv(buffer, index=False)
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data_kopeg_gabungan.csv"'
    return response

def dashboard_pembelian(request):
    daftar_bulan = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    daftar_tahun = ["2023", "2024", "2025"]

    bulan_terpilih = request.GET.get('bulan')
    tahun_terpilih = request.GET.get('tahun')
    data_pembelian = []
    total_pembelian = 0

    # Fungsi bantu agar aman konversi
    def safe_float(value):
        try:
            if isinstance(value, str):
                value = value.replace('.', '').replace(',', '').strip()
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    if bulan_terpilih and tahun_terpilih:
        filter_query = {'Bulan': bulan_terpilih, 'Tahun': tahun_terpilih}
        pembelian_cursor = db['pembelian_perbulan'].find(filter_query)

        data_pembelian = []
        for d in pembelian_cursor:
            # ambil hanya kolom yang dibutuhkan
            data_pembelian.append({
                '_id': str(d.get('_id', '')),
                'Kode_Item': d.get('Kode Item', ''),
                'Nama_Item': d.get('Nama Item', ''),
                'Jenis': d.get('Jenis', ''),
                'Jumlah': d.get('Jumlah', ''),
                'Satuan': d.get('Satuan', ''),
                'Total_Harga': safe_float(d.get('Total Harga', 0)),
                'Bulan': d.get('Bulan', ''),
                'Tahun': d.get('Tahun', '')
            })

        # Hitung total pembelian
        total_pembelian = sum(p['Total_Harga'] for p in data_pembelian)

    context = {
        'daftar_bulan': daftar_bulan,
        'daftar_tahun': daftar_tahun,
        'bulan_terpilih': bulan_terpilih,
        'tahun_terpilih': tahun_terpilih,
        'data_pembelian': data_pembelian,
        'total_pembelian': total_pembelian,
    }
    return render(request, 'dashboard_pembelian.html', context)

def dashboard_penjualan(request):
    daftar_bulan = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    daftar_tahun = ["2023", "2024", "2025"]

    bulan_terpilih = request.GET.get('bulan')
    tahun_terpilih = request.GET.get('tahun')
    data_penjualan = []
    total_penjualan = 0

    def safe_float(value):
        try:
            if isinstance(value, str):
                value = value.replace('.', '').replace(',', '').strip()
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    if bulan_terpilih and tahun_terpilih:
        filter_query = {'Bulan': bulan_terpilih, 'Tahun': tahun_terpilih}
        penjualan_cursor = db['penjualan_perbulan'].find(filter_query)

        data_penjualan = []
        for d in penjualan_cursor:
            data_penjualan.append({
                '_id': str(d.get('_id', '')),
                'Kode_Item': d.get('Kode Item', ''),
                'Nama_Item': d.get('Nama Item', ''),
                'Jenis': d.get('Jenis', ''),
                'Jumlah': d.get('Jumlah', ''),
                'Satuan': d.get('Satuan', ''),
                'Total_Harga': safe_float(d.get('Total Harga', 0)),
                'Bulan': d.get('Bulan', ''),
                'Tahun': d.get('Tahun', '')
            })

        total_penjualan = sum(p['Total_Harga'] for p in data_penjualan)

    context = {
        'daftar_bulan': daftar_bulan,
        'daftar_tahun': daftar_tahun,
        'bulan_terpilih': bulan_terpilih,
        'tahun_terpilih': tahun_terpilih,
        'data_penjualan': data_penjualan,
        'total_penjualan': total_penjualan,
    }
    return render(request, 'dashboard_penjualan.html', context)

# =========================================================
# 📦 DASHBOARD RETUR
# =========================================================
def dashboard_retur(request):
    daftar_bulan = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    daftar_tahun = ["2023", "2024", "2025"]

    bulan_terpilih = request.GET.get('bulan')
    tahun_terpilih = request.GET.get('tahun')
    data_retur = []
    total_retur = 0

    def safe_float(value):
        """Konversi ke float dengan aman, abaikan koma dan titik."""
        try:
            if isinstance(value, str):
                value = value.replace('.', '').replace(',', '').strip()
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    if bulan_terpilih and tahun_terpilih:
        filter_query = {'Bulan': bulan_terpilih, 'Tahun': tahun_terpilih}
        retur_cursor = db['retur_perbulan'].find(filter_query)

        for d in retur_cursor:
            # Tangani berbagai variasi nama kolom
            no = d.get('No') or d.get('No.') or d.get('Nomor', '')
            kode_item = d.get('Kode Item') or d.get('Kd. Item') or d.get('Kode Barang', '')
            nama_item = d.get('Nama Item') or d.get('Nama Barang', '')
            jumlah = d.get('Jml') or d.get('Jumlah', 0)
            satuan = d.get('Satuan', '')
            harga = safe_float(d.get('Harga', 0)) * 1000
            potongan = safe_float(d.get('Pot. %', 0))
            total_harga = (
                safe_float(d.get('Total Harga', 0))
                or safe_float(d.get('Total', 0))
            ) * 1000  # 🔹 dikali 1000 di sini

            data_retur.append({
                '_id': str(d.get('_id', '')),
                'No': no,
                'Kode_Item': kode_item,
                'Nama_Item': nama_item,
                'Jml': jumlah,
                'Satuan': satuan,
                'Harga': harga,
                'Potongan': potongan,
                'Total_Harga': total_harga,
                'Bulan': d.get('Bulan', ''),
                'Tahun': d.get('Tahun', '')
            })

        total_retur = sum(r['Total_Harga'] for r in data_retur)

    context = {
        'daftar_bulan': daftar_bulan,
        'daftar_tahun': daftar_tahun,
        'bulan_terpilih': bulan_terpilih,
        'tahun_terpilih': tahun_terpilih,
        'data_retur': data_retur,
        'total_retur': total_retur,
    }
    return render(request, 'dashboard_retur.html', context)

# =========================================================
# 📊 DASHBOARD STOK OPNAME
# =========================================================
def dashboard_stok(request):
    daftar_bulan = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    daftar_tahun = ["2023", "2024", "2025"]

    bulan_terpilih = request.GET.get('bulan')
    tahun_terpilih = request.GET.get('tahun')
    data_stok = []
    total_stok = 0

    def safe_float(value):
        try:
            if isinstance(value, str):
                value = value.replace('.', '').replace(',', '').strip()
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    if bulan_terpilih and tahun_terpilih:
        filter_query = {'Bulan': bulan_terpilih, 'Tahun': tahun_terpilih}
        stok_cursor = db['stok_perbulan'].find(filter_query)

        for d in stok_cursor:
            data_stok.append({
                '_id': str(d.get('_id', '')),
                'Kode_Barcode': d.get('Kode Barcode', ''),
                'Nama_Barang': d.get('Nama Barang', ''),
                'Stok_Fisik': safe_float(d.get('Stok Fisik', 0)),
                'Bulan': d.get('Bulan', ''),
                'Tahun': d.get('Tahun', '')
            })

        total_stok = sum(s['Stok_Fisik'] for s in data_stok)

    context = {
        'daftar_bulan': daftar_bulan,
        'daftar_tahun': daftar_tahun,
        'bulan_terpilih': bulan_terpilih,
        'tahun_terpilih': tahun_terpilih,
        'data_stok': data_stok,
        'total_stok': total_stok,
    }
    return render(request, 'dashboard_stok.html', context)



def dashboard_utama(request):
    pembelian_collection = db['pembelian_array']
    penjualan_collection = db['penjualan_array']
    retur_collection = db['retur_array']

    # 🔹 Hitung total keseluruhan
    total_pembelian = sum(item.get("Total_Harga", 0) for item in pembelian_collection.find())
    total_penjualan = sum(item.get("Total_Harga", 0) for item in penjualan_collection.find())
    total_retur = sum(item.get("Total_Harga", 0) for item in retur_collection.find())
    total_keuntungan = total_penjualan - total_pembelian - total_retur

    # 🔹 Buat data per bulan
    data_per_bulan = defaultdict(lambda: {"pembelian": 0, "penjualan": 0, "retur": 0})
    for item in pembelian_collection.find():
        bulan = item.get("Bulan", "").upper()
        data_per_bulan[bulan]["pembelian"] += item.get("Total_Harga", 0)
    for item in penjualan_collection.find():
        bulan = item.get("Bulan", "").upper()
        data_per_bulan[bulan]["penjualan"] += item.get("Total_Harga", 0)
    for item in retur_collection.find():
        bulan = item.get("Bulan", "").upper()
        data_per_bulan[bulan]["retur"] += item.get("Total_Harga", 0)

    # 🔹 Hitung keuntungan per bulan
    chart_data = []
    for bulan, data in data_per_bulan.items():
        keuntungan = data["penjualan"] - data["pembelian"] - data["retur"]
        chart_data.append({
            "bulan": bulan.capitalize(),
            "pembelian": data["pembelian"],
            "penjualan": data["penjualan"],
            "retur": data["retur"],
            "keuntungan": keuntungan
        })

    # Urutkan bulan secara berurutan (kalau kamu pakai nama bulan)
    urutan_bulan = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    chart_data.sort(key=lambda x: urutan_bulan.index(x["bulan"]) if x["bulan"] in urutan_bulan else 99)

    context = {
        "total_pembelian": total_pembelian,
        "total_penjualan": total_penjualan,
        "total_retur": total_retur,
        "total_keuntungan": total_keuntungan,
        "chart_data": chart_data,  # 🔹 Kirim ke template
    }

    return render(request, "dashboard_utama.html", context)

def prediksi_stok(request):
    # Ambil data dari MongoDB
    penjualan_data = list(db['penjualan_array'].find({}, {'_id': 0}))
    
    if not penjualan_data:
        return render(request, 'prediksi.html', {
            'message': '⚠️ Belum ada data penjualan untuk dianalisis.'
        })

    # Konversi ke DataFrame
    df = pd.DataFrame(penjualan_data)
    df['Jumlah'] = pd.to_numeric(df['Jumlah'], errors='coerce').fillna(0)
    
    # Kelompokkan berdasarkan Nama Item dan urutkan berdasarkan Bulan
    df = df.groupby(['Tahun', 'Bulan', 'Nama_Item'], as_index=False)['Jumlah'].sum()

    # Urutkan bulan secara benar (bukan alfabet)
    bulan_order = ["JANUARI","FEBRUARI","MARET","APRIL","MEI","JUNI","JULI","AGUSTUS","SEPTEMBER","OKTOBER","NOVEMBER","DESEMBER"]
    df['Bulan'] = pd.Categorical(df['Bulan'], categories=bulan_order, ordered=True)
    df = df.sort_values(['Nama_Item', 'Tahun', 'Bulan'])

    # Hitung moving average (rata-rata 3 bulan terakhir)
    prediksi_df = df.groupby('Nama_Item')['Jumlah'].apply(lambda x: round(x.rolling(window=3, min_periods=1).mean().iloc[-1])).reset_index()
    prediksi_df.columns = ['Nama_Item', 'Prediksi_Stok']

    # Hitung total stok keseluruhan
    total_prediksi = int(prediksi_df['Prediksi_Stok'].sum())

    context = {
        'prediksi': prediksi_df.to_dict('records'),
        'total_prediksi': total_prediksi
    }
    return render(request, 'prediksi.html', context)

def index(request):
    return render(request, 'index.html')

def dashboard_perbandingan(request):
    daftar_bulan = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    daftar_tahun = ["2023", "2024", "2025"]

    bulan = request.GET.get("bulan")
    tahun = request.GET.get("tahun")
    hasil = []
    chart_data = {}

    if bulan and tahun:
        filter_query = {"Bulan": bulan, "Tahun": tahun}

        # Ambil data dari setiap koleksi
        pembelian = list(db["pembelian_perbulan"].find(filter_query))
        penjualan = list(db["penjualan_perbulan"].find(filter_query))
        retur = list(db["retur_perbulan"].find(filter_query))
        opname = list(db["stok_perbulan"].find(filter_query))

        # Konversi ke DataFrame
        df_pembelian = pd.DataFrame(pembelian)
        df_penjualan = pd.DataFrame(penjualan)
        df_retur = pd.DataFrame(retur)
        df_opname = pd.DataFrame(opname)

        # 🔹 Standarisasi nama kolom agar seragam
        rename_map = {
            "Nama Item": "Nama_Item",
            "Nama Barang": "Nama_Item",
            "Nama": "Nama_Item",
            "Nama": "Nama_Item"
        }
        for df in [df_pembelian, df_penjualan, df_retur, df_opname]:
            df.rename(columns=rename_map, inplace=True)

        # 🔹 Pastikan kolom utama ada
        for df, kolom in [(df_pembelian, "Jumlah"), (df_penjualan, "Jumlah"), (df_opname, "Stok Fisik")]:
            if kolom not in df.columns:
                df[kolom] = 0

        if "Jml" in df_retur.columns:
            df_retur["Jumlah"] = df_retur["Jml"]
        else:
            df_retur["Jumlah"] = 0

        # 🔹 Hitung stok sistem (pembelian - penjualan + retur)
        pembelian_sum = df_pembelian.groupby("Nama_Item")["Jumlah"].sum() if not df_pembelian.empty else pd.Series()
        penjualan_sum = df_penjualan.groupby("Nama_Item")["Jumlah"].sum() if not df_penjualan.empty else pd.Series()
        retur_sum = df_retur.groupby("Nama_Item")["Jumlah"].sum() if not df_retur.empty else pd.Series()

        stok_sistem = (pembelian_sum - penjualan_sum + retur_sum).fillna(0)

        # 🔹 Gabungkan dengan stok opname
        df_opname = df_opname.rename(columns={"Stok Fisik": "Stok_Fisik"})
        opname_data = df_opname[["Nama_Item", "Stok_Fisik"]] if "Nama_Item" in df_opname.columns else pd.DataFrame(columns=["Nama_Item", "Stok_Fisik"])

        df_gabungan = pd.DataFrame({
            "Nama_Item": stok_sistem.index,
            "Stok_Sistem": stok_sistem.values
        })

        df_gabungan = df_gabungan.merge(opname_data, on="Nama_Item", how="outer").fillna(0)

        # 🔹 Hitung selisih
        df_gabungan["Selisih"] = df_gabungan["Stok_Fisik"] - df_gabungan["Stok_Sistem"]
        df_gabungan["Status"] = df_gabungan["Selisih"].apply(
            lambda x: "Sesuai" if x == 0 else ("Kurang" if x < 0 else "Lebih")
        )

        hasil = df_gabungan.to_dict("records")

        # 🔹 Untuk grafik
        chart_data = {
            "labels": df_gabungan["Nama_Item"].tolist(),
            "stok_sistem": df_gabungan["Stok_Sistem"].tolist(),
            "stok_opname": df_gabungan["Stok_Fisik"].tolist(),
        }

    context = {
        "daftar_bulan": daftar_bulan,
        "daftar_tahun": daftar_tahun,
        "bulan_terpilih": bulan,
        "tahun_terpilih": tahun,
        "hasil": hasil,
        "chart_data": chart_data,
    }
    return render(request, "dashboard_perbandingan.html", context)
