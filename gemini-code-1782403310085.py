import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman
st.set_page_config(
    page_title="Dashboard Analisis Penjualan",
    page_icon="📊",
    layout="wide"
)

# Judul Aplikasi
st.title("📊 Dashboard Analisis Penjualan")
st.markdown("Aplikasi ini digunakan untuk menganalisis data penjualan produk secara interaktif.")

# Load Data
@st.cache_data
def load_data():
    # Membaca data dari file CSV yang berada di folder yang sama
    df = pd.read_csv('data_penjualan.csv')
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    return df

try:
    df = load_data()
    
    # Sidebar untuk Filter
    st.sidebar.header("Filter Data")
    
    # Filter Kategori
    kategori_list = ['Semua'] + list(df['Kategori'].unique())
    selected_kategori = st.sidebar.selectbox("Pilih Kategori:", kategori_list)
    
    # Filter Tanggal
    min_date = df['Tanggal'].min().to_pydatetime()
    max_date = df['Tanggal'].max().to_pydatetime()
    start_date, end_date = st.sidebar.slider(
        "Pilih Rentang Tanggal:",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )
    
    # Menerapkan Filter ke Dataframe
    filtered_df = df[(df['Tanggal'] >= start_date) & (df['Tanggal'] <= end_date)]
    if selected_kategori != 'Semua':
        filtered_df = filtered_df[filtered_df['Kategori'] == selected_kategori]
        
    # KPI / Metrik Utama
    col1, col2, col3 = st.columns(3)
    total_pendapatan = filtered_df['Total_Pendapatan'].sum()
    total_terjual = filtered_df['Jumlah_Terjual'].sum()
    transaksi = filtered_df.shape[0]
    
    col1.metric("Total Pendapatan", f"Rp {total_pendapatan:,}")
    col2.metric("Total Produk Terjual", f"{total_terjual:,} unit")
    col3.metric("Jumlah Transaksi", f"{transaksi:,}")
    
    st.markdown("---")
    
    # Visualisasi Grafik
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Tren Pendapatan Harian")
        df_trend = filtered_df.groupby('Tanggal')['Total_Pendapatan'].sum().reset_index()
        fig_trend = px.line(df_trend, x='Tanggal', y='Total_Pendapatan', title="Pendapatan dari Waktu ke Waktu")
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_chart2:
        st.subheader("Kontribusi Pendapatan per Kategori")
        df_cat = filtered_df.groupby('Kategori')['Total_Pendapatan'].sum().reset_index()
        fig_pie = px.pie(df_cat, values='Total_Pendapatan', names='Kategori', title="Porsi Pendapatan Kategori")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    # Tabel Data
    st.subheader("Sampel Data Penjualan (20 Baris Pertama)")
    st.dataframe(filtered_df.head(20), use_container_width=True)

except Exception as e:
    st.error(f"Gagal memuat data. Pastikan file 'data_penjualan.csv' berada di folder/repositori yang sama dengan app.py. Error: {e}")