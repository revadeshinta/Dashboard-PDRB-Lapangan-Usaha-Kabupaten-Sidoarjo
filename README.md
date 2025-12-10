# 📊 Dashboard PDRB Menurut Lapangan Usaha Kabupaten Sidoarjo

Dashboard ini menampilkan perkembangan **Produk Domestik Regional Bruto (PDRB)** menurut **Lapangan Usaha** di Kabupaten Sidoarjo, dengan visualisasi interaktif berbasis **Streamlit**.

Data bersumber dari **Badan Pusat Statistik (BPS) Kabupaten Sidoarjo** dan telah diolah untuk keperluan visualisasi dan analisis sederhana untuk menyelesaikan mini proyek magang dari kampus.

---

## 🚀 Fitur Dashboard

- Filter interaktif:
  - Pilih metrik: **ADHB**, **ADHK**, **YoY**, **Q-to-Q**, **C-to-C**
  - Pilih sektor lapangan usaha: Primer, Sekunder, Tersier, dll.
- Visualisasi tren per periode (Tahun & Triwulan)
- Ringkasan nilai terbaru (cards metrics)
- Narasi analisis **dinamis** berdasarkan filter yang dipilih
- Tabel data detail yang dapat dieksplorasi pengguna
- Informasi edukatif mengenai masing-masing metrik ekonomi

---

## 📚 Penjelasan Metrik

| Metrik | Deskripsi |
|--------|-----------|
| **ADHB** | Nilai tambah barang/jasa berdasarkan **harga berlaku** pada tahun berjalan (nominal). |
| **ADHK** | Nilai tambah barang/jasa berdasarkan **harga konstan** pada tahun dasar (riil, tanpa inflasi). |
| **Y-on-Y** | Pertumbuhan dibanding **triwulan yang sama** pada tahun sebelumnya. |
| **Q-to-Q** | Pertumbuhan dibanding **triwulan sebelumnya** (dalam tahun berjalan). |
| **C-to-C** | Pertumbuhan kumulatif dibanding **kumulatif periode sama** di tahun sebelumnya. |

---

## 🛠️ Teknologi yang digunakan

- **Python**
- **Streamlit**
- **Pandas**
- **Altair**

---

## 📁 Struktur Folder

```text
Dashboard-PDRB-Lapangan-Usaha-Kabupaten-Sidoarjo/
├── app.py
├── pdrb_data_long_format.csv
└── requirements.txt
```

---

## ▶️ Cara Menjalankan Secara Lokal

Pastikan sudah menginstall Python 3.8+  
Kemudian jalankan perintah berikut:

```bash
pip install -r requirements.txt
streamlit run app.py
```
Aplikasi akan berjalan di:
👉 http://localhost:8501/

