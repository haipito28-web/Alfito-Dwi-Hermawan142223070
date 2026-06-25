import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Dashboard Keuangan Pribadi",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Dashboard Keuangan Pribadi")
st.markdown("Kelola dan pantau pemasukan serta pengeluaran kamu dengan mudah.")

# =========================
# UPLOAD / LOAD DATA
# =========================
st.sidebar.header("📂 Sumber Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload file CSV kamu sendiri (opsional)",
    type=["csv"],
    help="Kolom yang dibutuhkan: Tanggal, Kategori, Jenis, Deskripsi, Jumlah"
)

@st.cache_data
def load_default_data():
    return pd.read_csv("data_keuangan.csv")

def load_uploaded_data(file):
    return pd.read_csv(file)

if uploaded_file is not None:
    try:
        df = load_uploaded_data(uploaded_file)
        st.sidebar.success("File berhasil diupload!")
    except Exception as e:
        st.sidebar.error(f"Gagal membaca file: {e}")
        df = load_default_data()
else:
    df = load_default_data()
    st.sidebar.info("Menggunakan data contoh (data_keuangan.csv).")

# Validasi kolom wajib
required_cols = {"Tanggal", "Kategori", "Jenis", "Deskripsi", "Jumlah"}
if not required_cols.issubset(df.columns):
    st.error(
        f"Format CSV tidak sesuai. Kolom yang dibutuhkan: {', '.join(required_cols)}"
    )
    st.stop()

# Bersihkan & siapkan data
df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")
df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors="coerce")
df = df.dropna(subset=["Tanggal", "Jumlah"])
df["Bulan"] = df["Tanggal"].dt.to_period("M").astype(str)

# =========================
# FILTER (SIDEBAR)
# =========================
st.sidebar.header("🔍 Filter Data")

min_date = df["Tanggal"].min().date()
max_date = df["Tanggal"].max().date()

date_range = st.sidebar.date_input(
    "Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

jenis_options = sorted(df["Jenis"].dropna().unique().tolist())
jenis_filter = st.sidebar.multiselect(
    "Jenis Transaksi", options=jenis_options, default=jenis_options
)

kategori_options = sorted(df["Kategori"].dropna().unique().tolist())
kategori_filter = st.sidebar.multiselect(
    "Kategori", options=kategori_options, default=kategori_options
)

# Terapkan filter
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

mask = (
    (df["Tanggal"].dt.date >= start_date)
    & (df["Tanggal"].dt.date <= end_date)
    & (df["Jenis"].isin(jenis_filter))
    & (df["Kategori"].isin(kategori_filter))
)
filtered_df = df[mask].copy()

if filtered_df.empty:
    st.warning("Tidak ada data yang cocok dengan filter yang dipilih.")
    st.stop()

# =========================
# RINGKASAN (METRICS)
# =========================
total_pemasukan = filtered_df.loc[filtered_df["Jenis"] == "Pemasukan", "Jumlah"].sum()
total_pengeluaran = filtered_df.loc[filtered_df["Jenis"] == "Pengeluaran", "Jumlah"].sum()
saldo = total_pemasukan - total_pengeluaran

col1, col2, col3 = st.columns(3)
col1.metric("Total Pemasukan", f"Rp {total_pemasukan:,.0f}")
col2.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
col3.metric("Saldo Bersih", f"Rp {saldo:,.0f}", delta=f"Rp {saldo:,.0f}")

st.markdown("---")

# =========================
# VISUALISASI
# =========================
tab1, tab2, tab3 = st.tabs(["📈 Tren Bulanan", "🥧 Komposisi Kategori", "📋 Tabel Data"])

with tab1:
    st.subheader("Tren Pemasukan vs Pengeluaran per Bulan")
    monthly = (
        filtered_df.groupby(["Bulan", "Jenis"])["Jumlah"]
        .sum()
        .reset_index()
        .sort_values("Bulan")
    )
    fig_line = px.bar(
        monthly,
        x="Bulan",
        y="Jumlah",
        color="Jenis",
        barmode="group",
        text_auto=".2s",
        color_discrete_map={"Pemasukan": "#2E8B57", "Pengeluaran": "#DC143C"}
    )
    fig_line.update_layout(yaxis_title="Jumlah (Rp)", xaxis_title="Bulan")
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    st.subheader("Komposisi Pengeluaran per Kategori")
    expense_df = filtered_df[filtered_df["Jenis"] == "Pengeluaran"]
    if expense_df.empty:
        st.info("Tidak ada data pengeluaran pada filter ini.")
    else:
        by_category = (
            expense_df.groupby("Kategori")["Jumlah"].sum().reset_index().sort_values("Jumlah", ascending=False)
        )
        col_a, col_b = st.columns(2)
        with col_a:
            fig_pie = px.pie(
                by_category, names="Kategori", values="Jumlah", hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        with col_b:
            fig_bar = px.bar(
                by_category, x="Jumlah", y="Kategori", orientation="h",
                text_auto=".2s", color="Kategori"
            )
            fig_bar.update_layout(showlegend=False, xaxis_title="Jumlah (Rp)")
            st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    st.subheader("Tabel Transaksi")
    st.dataframe(
        filtered_df.sort_values("Tanggal", ascending=False).reset_index(drop=True),
        use_container_width=True
    )

    csv_export = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download data terfilter (CSV)",
        data=csv_export,
        file_name=f"keuangan_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

st.markdown("---")
st.caption("Dibuat dengan ❤️ menggunakan Streamlit | Format CSV: Tanggal, Kategori, Jenis, Deskripsi, Jumlah")
