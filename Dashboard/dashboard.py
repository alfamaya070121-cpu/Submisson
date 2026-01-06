import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    df = pd.read_csv("dashboard/main_data.csv")
    
    # Pastikan kolom tanggal bertipe datetime
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    
    # Buat kolom bulan
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    
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
# DISTRIBUSI PELANGGAN PER WILAYAH
# ======================
st.subheader("🗺️ Distribusi Pelanggan Berdasarkan State")

state_count = (
    df["customer_state"]
    .value_counts()
    .head(10)
    .reset_index()
)
state_count.columns = ["State", "Jumlah Order"]

fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.bar(state_count["State"], state_count["Jumlah Order"])
ax2.set_xlabel("State")
ax2.set_ylabel("Jumlah Order")
ax2.set_title("Top 10 State dengan Jumlah Order Terbanyak")

st.pyplot(fig2)

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
