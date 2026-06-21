"""
app.py
------
Aplikasi web Streamlit untuk:
1. Menampilkan & mengeksplorasi dataset (EDA)
2. Memprediksi apakah seorang penumpang akan selamat atau tidak,
   menggunakan model machine learning yang sudah dilatih (model.pkl)

Cara jalankan di komputer lokal:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
# Harus dipanggil PALING ATAS, sebelum kode Streamlit lainnya.
st.set_page_config(
    page_title="Prediksi Keselamatan Penumpang",
    page_icon="🚢",
    layout="wide"
)


# ============================================================
# FUNGSI BANTUAN (dengan cache agar tidak diulang-ulang)
# ============================================================

@st.cache_data
def load_data():
    """Membaca dataset CSV. @st.cache_data membuat data disimpan di memori
    sehingga tidak perlu dibaca ulang setiap kali ada interaksi di halaman."""
    df = pd.read_csv("data/dataset.csv")
    return df


@st.cache_resource
def load_model():
    """Membaca model machine learning yang sudah dilatih dari file model.pkl.
    @st.cache_resource cocok untuk objek seperti model (bukan data tabel)."""
    with open("model.pkl", "rb") as f:
        artefak = pickle.load(f)
    return artefak


# ============================================================
# SIDEBAR — MENU NAVIGASI
# ============================================================
st.sidebar.title("🚢 Menu")
halaman = st.sidebar.radio(
    "Pilih halaman:",
    ["Beranda", "Eksplorasi Data (EDA)", "Prediksi"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Aplikasi ini dibuat sebagai contoh penerapan **Data Mining** "
    "dengan algoritma **Random Forest Classifier** untuk memprediksi "
    "keselamatan penumpang kapal."
)


# ============================================================
# HALAMAN 1: BERANDA
# ============================================================
if halaman == "Beranda":
    st.title("🚢 Prediksi Keselamatan Penumpang Kapal")
    st.markdown("""
    Selamat datang di aplikasi **Data Mining** berbasis Streamlit.

    Aplikasi ini menggunakan dataset penumpang kapal untuk membangun model
    **klasifikasi** yang memprediksi apakah seorang penumpang **selamat** atau
    **tidak selamat**, berdasarkan data seperti kelas tiket, usia, jenis kelamin,
    dan lainnya.

    ### Cara menggunakan aplikasi ini:
    1. Buka menu **Eksplorasi Data (EDA)** untuk melihat isi dataset dan visualisasinya.
    2. Buka menu **Prediksi** untuk mencoba memprediksi data penumpang baru.

    ### Tentang model:
    - Algoritma: **Random Forest Classifier**
    - Fitur yang digunakan: kelas tiket, jenis kelamin, usia, jumlah saudara/pasangan,
      jumlah orang tua/anak, harga tiket, dan pelabuhan keberangkatan.
    """)

    try:
        artefak = load_model()
        st.success(f"Model siap digunakan — Akurasi pada data uji: **{artefak['akurasi']:.2%}**")
    except FileNotFoundError:
        st.warning("File model.pkl belum ditemukan. Jalankan `python model.py` terlebih dahulu.")


# ============================================================
# HALAMAN 2: EKSPLORASI DATA (EDA)
# ============================================================
elif halaman == "Eksplorasi Data (EDA)":
    st.title("📊 Eksplorasi Data (EDA)")

    df = load_data()

    st.subheader("Tampilan Data")
    st.dataframe(df.head(10), use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Baris", df.shape[0])
    col2.metric("Jumlah Kolom", df.shape[1])
    col3.metric("Data Kosong (Total)", int(df.isnull().sum().sum()))

    st.subheader("Statistik Deskriptif")
    st.dataframe(df.describe(), use_container_width=True)

    st.subheader("Visualisasi Data")

    tab1, tab2, tab3 = st.tabs(["Distribusi Selamat/Tidak", "Usia vs Selamat", "Kelas Tiket vs Selamat"])

    with tab1:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(data=df, x="Survived", ax=ax, palette=["#d9534f", "#5cb85c"])
        ax.set_xticklabels(["Tidak Selamat", "Selamat"])
        ax.set_title("Jumlah Penumpang Selamat vs Tidak Selamat")
        st.pyplot(fig)

    with tab2:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(data=df, x="Age", hue="Survived", multiple="stack", bins=20, ax=ax)
        ax.set_title("Distribusi Usia berdasarkan Status Keselamatan")
        st.pyplot(fig)

    with tab3:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(data=df, x="Pclass", hue="Survived", ax=ax)
        ax.set_title("Kelas Tiket vs Status Keselamatan")
        st.pyplot(fig)


# ============================================================
# HALAMAN 3: PREDIKSI
# ============================================================
elif halaman == "Prediksi":
    st.title("🔮 Prediksi Keselamatan Penumpang")
    st.markdown("Masukkan data penumpang di bawah ini, lalu tekan tombol **Prediksi**.")

    try:
        artefak = load_model()
    except FileNotFoundError:
        st.error("File model.pkl belum ditemukan. Jalankan `python model.py` terlebih dahulu di terminal.")
        st.stop()

    model = artefak["model"]
    le_sex = artefak["le_sex"]
    le_embarked = artefak["le_embarked"]
    feature_names = artefak["feature_names"]

    # Form input — dikelompokkan dalam form agar tidak refresh tiap kali 1 input diubah
    with st.form("form_prediksi"):
        col1, col2 = st.columns(2)

        with col1:
            pclass = st.selectbox("Kelas Tiket (Pclass)", [1, 2, 3], index=2,
                                   help="1 = Kelas Atas, 2 = Kelas Menengah, 3 = Kelas Ekonomi")
            sex = st.selectbox("Jenis Kelamin", ["male", "female"])
            age = st.slider("Usia", min_value=0, max_value=80, value=30)
            sibsp = st.number_input("Jumlah Saudara/Pasangan ikut (SibSp)", min_value=0, max_value=10, value=0)

        with col2:
            parch = st.number_input("Jumlah Orang Tua/Anak ikut (Parch)", min_value=0, max_value=10, value=0)
            fare = st.number_input("Harga Tiket (Fare)", min_value=0.0, max_value=600.0, value=30.0)
            embarked = st.selectbox("Pelabuhan Keberangkatan (Embarked)", ["S", "C", "Q"],
                                     help="S = Southampton, C = Cherbourg, Q = Queenstown")

        tombol_submit = st.form_submit_button("🔍 Prediksi")

    if tombol_submit:
        # Susun data input menjadi urutan kolom yang SAMA seperti saat training
        sex_encoded = le_sex.transform([sex])[0]
        embarked_encoded = le_embarked.transform([embarked])[0]

        data_input = pd.DataFrame([{
            "Pclass": pclass,
            "Sex": sex_encoded,
            "Age": age,
            "SibSp": sibsp,
            "Parch": parch,
            "Fare": fare,
            "Embarked": embarked_encoded
        }])[feature_names]  # urutkan kolom sesuai saat training

        prediksi = model.predict(data_input)[0]
        probabilitas = model.predict_proba(data_input)[0]

        st.markdown("---")
        st.subheader("Hasil Prediksi")

        if prediksi == 1:
            st.success(f"✅ Penumpang diprediksi **SELAMAT** (probabilitas: {probabilitas[1]:.1%})")
        else:
            st.error(f"❌ Penumpang diprediksi **TIDAK SELAMAT** (probabilitas: {probabilitas[0]:.1%})")

        col1, col2 = st.columns(2)
        col1.metric("Probabilitas Tidak Selamat", f"{probabilitas[0]:.1%}")
        col2.metric("Probabilitas Selamat", f"{probabilitas[1]:.1%}")
