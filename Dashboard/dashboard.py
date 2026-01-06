import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ======================
# KONFIGURASI HALAMAN
# ======================
st.set_page_config(
    page_title="E-Commerce Dashboard",
    layout="wide"
)

st.title("📊 E-Commerce Dashboard")
st.markdown(
    """
    Dashboard ini menyajikan hasil analisis **tren penjualan dari waktu ke waktu**
    serta **distribusi pelanggan berdasarkan wilayah**.
    """
)

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, "main_data.csv")
    
    df = pd.read_csv(data_path)

    return df

df = load_data()

# ======================
# PREVIEW DATA
# ======================
with st.expander("🔍 Lihat Contoh Data"):
    st.dataframe(df.head())

# ======================
# TREN PENJUALAN BULANAN
# ======================
st.subheader("📈 Tren Penjualan Bulanan")

monthly_sales = (
    df.groupby("order_month")["revenue"]
      .sum()
      .reset_index()
)

fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(monthly_sales["order_month"], monthly_sales["revenue"])
ax1.set_xlabel("Bulan")
ax1.set_ylabel("Total Revenue")
ax1.set_title("Tren Penjualan Bulanan")
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig1)

# ======================
# DISTRIBUSI PELANGGAN PER WILAYAH (IMPROVED)
# ======================
st.subheader("🗺️ Top 10 Wilayah dengan Jumlah Order Terbanyak")

state_count = (
    df["customer_city"]
    .value_counts()
    .head(10)
    .sort_values(ascending=True)  # penting untuk horizontal bar
)

fig, ax = plt.subplots(figsize=(10, 5))

bars = ax.barh(
    state_count.index,
    state_count.values
)

ax.set_xlabel("Jumlah Order")
ax.set_ylabel("City")
ax.set_title("Top 10 Wilayah dengan Jumlah Order Terbanyak")

# Tambahkan label angka di ujung bar
for bar in bars:
    width = bar.get_width()
    ax.text(
        width + (state_count.max() * 0.01),
        bar.get_y() + bar.get_height() / 2,
        f"{int(width):,}",
        va="center"
    )

plt.tight_layout()
st.pyplot(fig)
# ======================
# INSIGHT SINGKAT
# ======================
st.markdown(
    """
    ### 📌 Insight Utama
    - Penjualan menunjukkan fluktuasi dari waktu ke waktu dengan kecenderungan meningkat
      pada periode tertentu.
    - Transaksi e-commerce terkonsentrasi pada beberapa state utama.
    - Informasi ini dapat dimanfaatkan untuk mendukung strategi pemasaran dan distribusi.
    """
)
