<!DOCTYPE html>
<html>
<head>
    <title>Rental Mobil Otomatis</title>
    <style>
        .card { border: 1px solid #ddd; padding: 15px; margin: 10px; display: inline-block; width: 200px; }
        .tersedia { color: green; font-weight: bold; }
        .disewa { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Daftar Mobil Kami</h1>
    {% for m in mobil %}
        <div class="card">
            <h3>{{ m.nama }}</h3>
            <p>Rp {{ m.harga_per_hari }} / hari</p>
            <p>Status: 
                <span class="{{ 'tersedia' if m.status == 'Tersedia' else 'disewa' }}">
                    {{ m.status }}
                </span>
            </p>
            {% if m.status == 'Tersedia' %}
                <a href="/sewa/{{ m.id }}"><button>Sewa Sekarang</button></a>
            {% else %}
                <button disabled>Tidak Tersedia</button>
            {% endif %}
        </div>
    {% endfor %}
    <br><hr>
    <a href="/admin">Masuk ke Halaman Admin</a>
</body>
</html>
