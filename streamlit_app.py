from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

# ==========================================
# 1. ABSTRACT CLASS & INHERITANCE (Kendaraan)
# ==========================================

class Kendaraan(ABC):
    def __init__(self, id_kendaraan, merk, nopol, harga_sewa):
        self.id = id_kendaraan
        self.merk = merk
        self.nopol = nopol
        self.harga_sewa = harga_sewa
        self.is_available = True  # Default available

    def get_status(self):
        return self.is_available

    def get_harga(self):
        return self.harga_sewa

    @abstractmethod
    def info_spesifik(self):
        pass

# --- Child Classes ---

class Hatchback(Kendaraan):
    def __init__(self, id_kendaraan, merk, nopol, harga_sewa, kapasitas_bagasi):
        super().__init__(id_kendaraan, merk, nopol, harga_sewa)
        self.kapasitas_bagasi = kapasitas_bagasi

    def info_spesifik(self):
        return f"Kapasitas Bagasi: {self.kapasitas_bagasi} Liter"

class Sedan(Kendaraan):
    def __init__(self, id_kendaraan, merk, nopol, harga_sewa, tingkat_kenyamanan):
        super().__init__(id_kendaraan, merk, nopol, harga_sewa)
        self.tingkat_kenyamanan = tingkat_kenyamanan # Misal: "High", "Medium"

    def info_spesifik(self):
        return f"Kenyamanan: {self.tingkat_kenyamanan}"

class SUV(Kendaraan):
    def __init__(self, id_kendaraan, merk, nopol, harga_sewa, four_wheel_drive):
        super().__init__(id_kendaraan, merk, nopol, harga_sewa)
        self.four_wheel_drive = four_wheel_drive # Boolean

    def info_spesifik(self):
        return f"4WD: {'Ya' if self.four_wheel_drive else 'Tidak'}"


# ==========================================
# 2. ENTITY CLASSES (User & Pembayaran)
# ==========================================

class User:
    def __init__(self, user_id, nama, email, password):
        self.user_id = user_id
        self.nama = nama
        self.email = email
        self.password = password

    def get_profile(self):
        return f"User: {self.nama} ({self.email})"

class Pembayaran:
    def __init__(self, pay_id, jumlah):
        self.pay_id = pay_id
        self.jumlah = jumlah
        self.tgl_bayar = datetime.now()
        self.status_sukses = False

    def verifikasi(self):
        # Simulasi verifikasi pembayaran
        self.status_sukses = True
        print(f"Pembayaran {self.pay_id} sebesar Rp{self.jumlah} TERVERIFIKASI.")
        return True


# ==========================================
# 3. CORE LOGIC (Booking & Managers)
# ==========================================

class Booking:
    def __init__(self, booking_id, user: User, kendaraan: Kendaraan, durasi_hari):
        self.booking_id = booking_id
        self.user = user
        self.kendaraan = kendaraan
        self.tgl_sewa = datetime.now()
        self.durasi_hari = durasi_hari
        self.total_biaya = self.hitung_total()
        self.status_booking = "Pending"
        self.pembayaran = None  # Akan diisi nanti

    def hitung_total(self):
        return self.durasi_hari * self.kendaraan.get_harga()

class InventoryManager:
    def __init__(self):
        self.daftar_mobil: List[Kendaraan] = []

    def tambah_unit(self, kendaraan: Kendaraan):
        self.daftar_mobil.append(kendaraan)
        print(f"[Inventory] Unit baru ditambahkan: {kendaraan.merk} ({type(kendaraan).__name__})")

    def cek_ketersediaan(self, id_kendaraan):
        for mobil in self.daftar_mobil:
            if mobil.id == id_kendaraan:
                return mobil.is_available
        return False

    def update_stok(self, id_kendaraan, status):
        for mobil in self.daftar_mobil:
            if mobil.id == id_kendaraan:
                mobil.is_available = status
                print(f"[Inventory] Status {mobil.merk} diubah menjadi: {'Available' if status else 'Booked'}")

# ==========================================
# 4. SERVICE LAYER (BookingService)
# ==========================================

class BookingService:
    def __init__(self, inventory_manager: InventoryManager):
        self.inventory = inventory_manager

    def buat_pesanan(self, user: User, id_kendaraan, durasi):
        # 1. Cek Ketersediaan
        if not self.inventory.cek_ketersediaan(id_kendaraan):
            print("Maaf, mobil tidak tersedia.")
            return None

        # 2. Ambil Objek Mobil
        kendaraan_terpilih = next((m for m in self.inventory.daftar_mobil if m.id == id_kendaraan), None)
        
        # 3. Buat Object Booking
        booking_baru = Booking(
            booking_id=f"B-{datetime.now().strftime('%H%M%S')}",
            user=user,
            kendaraan=kendaraan_terpilih,
            durasi_hari=durasi
        )
        
        # 4. Update Stok jadi tidak available sementara
        self.inventory.update_stok(id_kendaraan, False)
        
        print(f"Booking Dibuat! Total: Rp {booking_baru.total_biaya}")
        return booking_baru

    def proses_pembayaran(self, booking: Booking, metode):
        # Buat objek pembayaran
        pembayaran_baru = Pembayaran(f"PAY-{booking.booking_id}", booking.total_biaya)
        
        # Lakukan verifikasi
        if pembayaran_baru.verifikasi():
            booking.pembayaran = pembayaran_baru
            booking.status_booking = "Confirmed"
            print("Pesanan Selesai & Dikonfirmasi.")
            return pembayaran_baru
        else:
            print("Pembayaran Gagal.")
            return None

# ==========================================
# CONTOH PENGGUNAAN (MAIN)
# ==========================================

if __name__ == "__main__":
    # 1. Setup Sistem & Inventory
    inventory = InventoryManager()
    service = BookingService(inventory)

    # 2. Tambah Mobil ke Inventory (Polymorphism: List menyimpan berbagai tipe mobil)
    mobil1 = SUV("M01", "Pajero Sport", "B 1234 CD", 800000, True)
    mobil2 = Sedan("M02", "Honda Civic", "B 5678 EF", 600000, "High")
    mobil3 = Hatchback("M03", "Honda Brio", "B 9012 GH", 300000, 250)

    inventory.tambah_unit(mobil1)
    inventory.tambah_unit(mobil2)
    inventory.tambah_unit(mobil3)

    print("-" * 30)

    # 3. User Melakukan Booking
    user1 = User("U001", "Budi Santoso", "budi@email.com", "rahasia123")
    
    # User ingin sewa Pajero (ID: M01) selama 3 hari
    booking_saya = service.buat_pesanan(user1, "M01", 3)

    if booking_saya:
        print(f"\nDetail Pesanan:")
        print(f"Penyewa: {booking_saya.user.nama}")
        print(f"Mobil: {booking_saya.kendaraan.merk} ({booking_saya.kendaraan.info_spesifik()})")
        print(f"Total Bayar: Rp {booking_saya.total_biaya}")
        
        print("\n--- Proses Pembayaran ---")
        service.proses_pembayaran(booking_saya, "Transfer Bank")
