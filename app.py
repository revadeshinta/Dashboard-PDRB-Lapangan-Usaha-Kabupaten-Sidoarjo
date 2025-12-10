import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Dashboard PDRB Sidoarjo",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("pdrb_data_long_format.csv")
    df = df.sort_values(["Tahun", "Quarter_Order"])
    return df

df = load_data()

# =========================
# HEADER + KETERANGAN
# =========================
st.markdown("""
<h2 style='text-align: center; color:#0E4D92;'>📊 Dashboard PDRB Menurut Lapangan Usaha</h2>
<p style='text-align: center;'>
Kabupaten Sidoarjo • ADHB | ADHK | YoY | Q-to-Q | C-to-C
</p>
""", unsafe_allow_html=True)

# Keterangan singkat di bawah judul
st.markdown("""
<div style='text-align: center; font-size: 14px; margin-bottom: 20px;'>
Dashboard ini menampilkan perkembangan Produk Domestik Regional Bruto (PDRB) menurut lapangan usaha
Kabupaten Sidoarjo. Data bersumber dari Badan Pusat Statistik (BPS) Kabupaten Sidoarjo dan telah diolah
untuk keperluan visualisasi dan analisis sederhana.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =========================
# SIDEBAR FILTER + TENTANG DATA
# =========================
st.sidebar.header("🔍 Filter Data")
pilih_metrik = st.sidebar.selectbox(
    "Pilih metrik",
    df["Metrik"].unique().tolist(),
    index=2  # misal default: Y-on-Y (%)
)
pilih_sektor = st.sidebar.multiselect(
    "Pilih sektor",
    options=df["LAPANGAN USAHA"].unique().tolist(),
    default=df["LAPANGAN USAHA"].unique().tolist()
)

with st.sidebar.expander("ℹ️ Tentang Data"):
    st.write(
        """
        **Jenis data**: PDRB menurut Lapangan Usaha  
        **Wilayah**: Kabupaten Sidoarjo  
        **Sumber**: BPS Kabupaten Sidoarjo  

        **Penjelasan Metrik:**
        - **ADHB (Atas Dasar Harga Berlaku)**  
          Menggunakan harga pada tahun berjalan → mencerminkan nilai nominal.
          Terpengaruh oleh perubahan volume dan inflasi.

        - **ADHK (Atas Dasar Harga Konstan 2010)**  
          Menggunakan harga tetap pada tahun dasar (2010) → mencerminkan pertumbuhan riil.
          Tidak terpengaruh inflasi. Tahun dasar dapat berubah (2010, 2015, dst).

        - **Y-on-Y (Year-on-Year)**  
          Pertumbuhan dibanding triwulan sama pada tahun sebelumnya.

        - **Q-to-Q (Quarter-to-Quarter)**  
          Pertumbuhan dibanding triwulan sebelumnya (tahun berjalan).

        - **C-to-C (Cumulative-to-Cumulative)**  
          Pertumbuhan kumulatif dibanding periode sama tahun sebelumnya.

        **Catatan Penting:**
        - ADHK **harus** mencantumkan tahun dasar (contoh: 2010)  
          karena menghitung harga tetap dengan menghilangkan inflasi.
        - ADHB **tidak perlu** tahun dasar karena menggunakan harga berjalan.

        **Satuan:**
        - ADHB & ADHK: Rupiah (Miliar/Triliun)
        - YoY, Q-to-Q, C-to-C: Persentase (%)
        """
    )


# =========================
# FILTER DATA
# =========================
filtered = df[
    (df["Metrik"] == pilih_metrik) &
    (df["LAPANGAN USAHA"].isin(pilih_sektor))
]

# =========================
# RINGKASAN TERKINI
# =========================
st.markdown("### 📌 Ringkasan Terkini")

if not filtered.empty:
    latest_year = filtered["Tahun"].max()
    latest_q = filtered[filtered["Tahun"] == latest_year]["Quarter_Order"].max()
    latest = filtered[
        (filtered["Tahun"] == latest_year) &
        (filtered["Quarter_Order"] == latest_q)
    ]

    col1, col2, col3 = st.columns(3)
    col1.metric("Periode Terbaru", f"{latest_year} - Triwulan {latest_q}")
    col2.metric("Jumlah Sektor", len(latest))
    col3.metric("Nilai Median", round(latest["Nilai"].median(), 2))
else:
    st.warning("Data untuk kombinasi filter tersebut tidak tersedia.")

# =========================
# GRAFIK TREN
# =========================
st.markdown(f"### 📈 Tren {pilih_metrik}")

if not filtered.empty:
    # urutan label waktu biar nggak acak
    time_order = (
        filtered
        .sort_values(["Tahun", "Quarter_Order"])
        [["Tahun", "Quarter_Order", "Time_Label"]]
        .drop_duplicates()["Time_Label"]
        .tolist()
    )

    chart = alt.Chart(filtered).mark_line(point=True).encode(
        x=alt.X(
            'Time_Label:N',
            sort=time_order,
            title='Periode (Tahun–Triwulan)'
        ),
        y=alt.Y('Nilai:Q', title='Nilai'),
        color=alt.Color('LAPANGAN USAHA:N', title='Lapangan Usaha'),
        tooltip=['Time_Label', 'LAPANGAN USAHA', 'Metrik', 'Nilai']
    ).properties(
        width='container',
        height=400
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

    # =========================
    # NARASI ANALISIS SINGKAT (DINAMIS)
    # =========================
    time_points = (
        filtered
        .sort_values(["Tahun", "Quarter_Order"])
        [["Tahun", "Quarter_Order", "Time_Label"]]
        .drop_duplicates()
    )

    if len(time_points) >= 2:
        last_tp = time_points.iloc[-1]
        prev_tp = time_points.iloc[-2]

        last_label = str(last_tp["Time_Label"])
        prev_label = str(prev_tp["Time_Label"])

        latest_vals = filtered[
            (filtered["Tahun"] == last_tp["Tahun"]) &
            (filtered["Quarter_Order"] == last_tp["Quarter_Order"])
        ]
        prev_vals = filtered[
            (filtered["Tahun"] == prev_tp["Tahun"]) &
            (filtered["Quarter_Order"] == prev_tp["Quarter_Order"])
        ]

        # samakan sektor yang ada di kedua periode
        common_sectors = sorted(
            set(latest_vals["LAPANGAN USAHA"]) &
            set(prev_vals["LAPANGAN USAHA"])
        )

        if common_sectors:
            latest_vals = latest_vals[latest_vals["LAPANGAN USAHA"].isin(common_sectors)]
            prev_vals = prev_vals[prev_vals["LAPANGAN USAHA"].isin(common_sectors)]

            latest_series = latest_vals.set_index("LAPANGAN USAHA")["Nilai"]
            prev_series = prev_vals.set_index("LAPANGAN USAHA")["Nilai"]

            change = latest_series - prev_series

            avg_latest = latest_series.mean()
            max_up_sector = change.idxmax()
            max_up_val = change.loc[max_up_sector]
            max_down_sector = change.idxmin()
            max_down_val = change.loc[max_down_sector]

            sektor_dipilih = ", ".join(sorted(filtered["LAPANGAN USAHA"].unique()))

            penjelasan = f"""
**Penjelasan**

Pada grafik di atas ditampilkan tren **{pilih_metrik}** PDRB menurut lapangan usaha
untuk sektor **{sektor_dipilih}** di Kabupaten Sidoarjo.

Pada periode **{last_label}**, rata-rata nilai **{pilih_metrik}** tercatat sekitar **{avg_latest:.2f}**.
Dibandingkan dengan periode sebelumnya (**{prev_label}**):

- Sektor dengan **kenaikan tertinggi**: **{max_up_sector}** (perubahan **{max_up_val:+.2f}**)
- Sektor dengan **penurunan terdalam**: **{max_down_sector}** (perubahan **{max_down_val:+.2f}**)

Note: Narasi ini otomatis menyesuaikan setiap kali  metrik atau pilihan sektor di sidebar diubah.
"""
            st.markdown(penjelasan)
        else:
            st.markdown(
                f"**Narasi singkat:** Grafik menunjukkan perkembangan **{pilih_metrik}** pada periode **{last_label}**, namun tidak tersedia pembanding langsung dengan periode sebelumnya untuk sektor yang dipilih."
            )
    else:
        st.markdown(
            f"**Narasi singkat:** Grafik menampilkan tren **{pilih_metrik}** untuk sektor terpilih, tetapi jumlah periode masih terbatas sehingga analisis perubahan antar waktu belum optimal."
        )

else:
    st.info("Silakan ubah filter untuk menampilkan grafik.")

# =========================
# TABEL DATA DETAIL
# =========================
with st.expander("📊 Lihat Tabel Data Detail"):
    if not filtered.empty:
        st.dataframe(filtered.style.format({"Nilai": "{:.2f}"}))
    else:
        st.write("Tidak ada data untuk kombinasi filter yang dipilih.")

# =========================
# FOOTER
# =========================
st.caption(
    "Sumber: Badan Pusat Statistik (BPS) Kabupaten Sidoarjo. Data diolah oleh Reva Deshinta Isyana untuk menjadi mini proyek magang.""Sumber: Badan Pusat Statistik (BPS) Kabupaten Sidoarjo. Data diolah oleh Reva Deshinta Isyana, mahasiswa S-1 Sains Data Universitas Negeri Surabaya, untuk menjadi mini proyek magang."
)
