from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# --- DATABASE SEDERHANA (Simulasi Data) ---
# Dalam aplikasi nyata, ini diganti dengan koneksi MySQL/PostgreSQL
mobil_db = [
    {'id': 1, 'nama': 'Toyota Avanza', 'harga_per_hari': 300000, 'status': 'Tersedia', 'gambar': 'avanza.jpg'},
    {'id': 2, 'nama': 'Honda Brio', 'harga_per_hari': 250000, 'status': 'Tersedia', 'gambar': 'brio.jpg'},
    {'id': 3, 'nama': 'Mitsubishi Pajero', 'harga_per_hari': 800000, 'status': 'Disewa', 'gambar': 'pajero.jpg'}
]

transaksi_db = []

# --- ROUTE & LOGIKA ---

@app.route('/')
def index():
    # Menampilkan hanya mobil yang tersedia di halaman utama
    return render_template('index.html', mobil=mobil_db)

@app.route('/sewa/<int:mobil_id>', methods=['GET', 'POST'])
def sewa(mobil_id):
    # Cari mobil berdasarkan ID
    mobil_terpilih = next((m for m in mobil_db if m['id'] == mobil_id), None)
    
    if request.method == 'POST':
        nama_penyewa = request.form['nama']
        tgl_mulai = request.form['tgl_mulai']
        tgl_selesai = request.form['tgl_selesai']
        
        # 1. OTOMATISASI PENGHITUNGAN DURASI
        d1 = datetime.strptime(tgl_mulai, "%Y-%m-%d")
        d2 = datetime.strptime(tgl_selesai, "%Y-%m-%d")
        delta = d2 - d1
        durasi_hari = delta.days
        
        if durasi_hari <= 0:
            return "Tanggal tidak valid (minimal 1 hari)"

        # 2. OTOMATISASI PENGHITUNGAN HARGA TOTAL
        total_harga = durasi_hari * mobil_terpilih['harga_per_hari']
        
        # 3. OTOMATISASI UPDATE STATUS
        mobil_terpilih['status'] = 'Disewa'
        
        # Simpan Transaksi
        transaksi_baru = {
            'mobil': mobil_terpilih['nama'],
            'penyewa': nama_penyewa,
            'total_harga': total_harga,
            'durasi': durasi_hari
        }
        transaksi_db.append(transaksi_baru)
        
        return render_template('sukses.html', transaksi=transaksi_baru)
        
    return render_template('form_sewa.html', mobil=mobil_terpilih)

@app.route('/admin')
def admin():
    # Halaman untuk pemilik rental melihat laporan
    return render_template('admin.html', transaksi=transaksi_db, mobil=mobil_db)

if __name__ == '__main__':
    app.run(debug=True)
    
