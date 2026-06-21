# 🚢 Prediksi Keselamatan Penumpang Kapal — Data Mining App

Aplikasi web sederhana untuk eksplorasi data dan prediksi klasifikasi menggunakan
**Python**, **Scikit-learn**, dan **Streamlit**.

## 📁 Struktur Folder

```
data-mining-app/
├── data/
│   └── dataset.csv       # Dataset mentah
├── app.py                # Aplikasi web Streamlit
├── model.py               # Script untuk training model machine learning
├── model.pkl               # Model yang sudah dilatih (dihasilkan oleh model.py)
├── requirements.txt        # Daftar library yang dibutuhkan
└── README.md                # Dokumentasi ini
```

## 🧠 Tentang Project

Project ini menggunakan algoritma **Random Forest Classifier** untuk memprediksi
apakah seorang penumpang kapal akan **selamat** atau **tidak selamat**, berdasarkan
fitur-fitur berikut:

| Fitur | Keterangan |
|---|---|
| Pclass | Kelas tiket (1 = atas, 2 = menengah, 3 = ekonomi) |
| Sex | Jenis kelamin |
| Age | Usia |
| SibSp | Jumlah saudara/pasangan yang ikut |
| Parch | Jumlah orang tua/anak yang ikut |
| Fare | Harga tiket |
| Embarked | Pelabuhan keberangkatan (S/C/Q) |

## 🚀 Cara Menjalankan di Komputer Lokal

1. **Clone repository ini**
   ```bash
   git clone https://github.com/USERNAME-ANDA/data-mining-app.git
   cd data-mining-app
   ```

2. **Buat virtual environment (opsional tapi disarankan)**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Mac/Linux
   venv\Scripts\activate         # Windows
   ```

3. **Install semua library yang dibutuhkan**
   ```bash
   pip install -r requirements.txt
   ```

4. **Latih model (hanya perlu dijalankan sekali)**
   ```bash
   python model.py
   ```
   Ini akan menghasilkan file `model.pkl`.

5. **Jalankan aplikasi Streamlit**
   ```bash
   streamlit run app.py
   ```
   Aplikasi akan terbuka otomatis di browser pada `http://localhost:8501`.

## 🌐 Deploy ke Streamlit Community Cloud (Gratis)

1. Push semua file ke repository GitHub (termasuk `model.pkl`).
2. Buka [https://share.streamlit.io](https://share.streamlit.io) dan login dengan akun GitHub.
3. Klik **New app**, pilih repository ini, dan pilih file utama: `app.py`.
4. Klik **Deploy**. Tunggu beberapa menit, aplikasi akan online dengan URL publik.

## 📊 Hasil Model

Model Random Forest pada project ini mencapai akurasi sekitar **74%** pada data uji
(akan bervariasi tergantung dataset yang digunakan).

## 🔄 Mengganti dengan Dataset Anda Sendiri

1. Ganti file `data/dataset.csv` dengan CSV Anda.
2. Sesuaikan nama kolom target dan fitur di dalam `model.py` dan `app.py`.
3. Jalankan ulang `python model.py` untuk melatih ulang model.

## 🛠️ Teknologi yang Digunakan

- Python 3
- Pandas & NumPy — pengolahan data
- Scikit-learn — machine learning
- Matplotlib & Seaborn — visualisasi data
- Streamlit — aplikasi web interaktif
