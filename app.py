import streamlit as st
import openai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator FI III Terpadu", page_icon="💊", layout="centered")

st.title("💊 Kalkulator Universal & Database Makro FI III")
st.subheader("Sistem Keputusan Klinis Apoteker Terintegrasi Bluesminds API")
st.write("---")

# --- DATABASE EKSTENSIF FARMAKOPE INDONESIA EDISI III ---
# Menyimpan Dosis Lazim (DL) dan Dosis Maksimum (DM) Dewasa (dalam mg)
DATABASE_FI3 = {
    "Acetaminophenum (Parasetamol)": {
        "dl_sekali": 500.0, "dl_sehari": 2000.0, "dm_sekali": 0.0, "dm_sehari": 0.0, "info": "Analgetikum & Antipiretikum"
    },
    "Acetarsolum (Asetarsol)": {
        "dl_sekali": 250.0, "dl_sehari": 1000.0, "dm_sekali": 250.0, "dm_sehari": 1000.0, "info": "Antiamebiasis, Antiprotozoa"
    },
    "Acidum Acetylsalicylicum (Asetosal/Aspirin)": {
        "dl_sekali": 500.0, "dl_sehari": 1500.0, "dm_sekali": 1000.0, "dm_sehari": 8000.0, "info": "Analgetikum, Antipiretikum, Antireumatikum"
    },
    "Acidum Nicotinicum (Asam Nikotinat)": {
        "dl_sekali": 50.0, "dl_sehari": 200.0, "dm_sekali": 200.0, "dm_sehari": 800.0, "info": "Komponen Vitamin B Kompleks"
    },
    "Aethylmorphini Hydrochloridum (Dionin)": {
        "dl_sekali": 5.0, "dl_sehari": 15.0, "dm_sekali": 30.0, "dm_sehari": 100.0, "info": "Antitusivum, Narkotika"
    },
    "Aminophyllinum (Aminofilin)": {
        "dl_sekali": 200.0, "dl_sehari": 600.0, "dm_sekali": 500.0, "dm_sehari": 1500.0, "info": "Bronkodilator. Indeks terapi sempit."
    },
    "Amitriptylini Hydrochloridum (Amitriptilin)": {
        "dl_sekali": 25.0, "dl_sehari": 75.0, "dm_sekali": 30.0, "dm_sehari": 300.0, "info": "Antidepresan Trisiklik"
    },
    "Ammonii Bromidum (Amonium Bromida)": {
        "dl_sekali": 500.0, "dl_sehari": 1500.0, "dm_sekali": 1000.0, "dm_sehari": 3000.0, "info": "Sedativum"
    },
    "Amobarbitalum (Amobarbital)": {
        "dl_sekali": 50.0, "dl_sehari": 150.0, "dm_sekali": 300.0, "dm_sehari": 600.0, "info": "Hipnotikum & Sedativum"
    },
    "Ampicillinum (Ampisilin)": {
        "dl_sekali": 250.0, "dl_sehari": 1000.0, "dm_sekali": 0.0, "dm_sehari": 0.0, "info": "Antibiotikum Penisilin broad-spectrum"
    },
    "Atropini Sulfas (Atropin Sulfat)": {
        "dl_sekali": 0.25, "dl_sehari": 1.0, "dm_sekali": 1.0, "dm_sehari": 3.0, "info": "Parasimpatolitik/Antikolinergik ekstrem"
    },
    "Barbitalum (Barbital)": {
        "dl_sekali": 250.0, "dl_sehari": 500.0, "dm_sekali": 500.0, "dm_sehari": 1000.0, "info": "Hipnotikum & Sedativum"
    },
    "Chlorpheniramini Maleas (CTM)": {
        "dl_sekali": 2.0, "dl_sehari": 8.0, "dm_sekali": 0.0, "dm_sehari": 40.0, "info": "Antihistaminikum generasi pertama"
    },
    "Chlorpromazini Hydrochloridum (CPZ)": {
        "dl_sekali": 25.0, "dl_sehari": 75.0, "dm_sekali": 250.0, "dm_sehari": 1000.0, "info": "Antipsikotikum / Neuroleptikum"
    },
    "Chlortetranyclini Hydrochloridum (Klortetrasiklin)": {
        "dl_sekali": 250.0, "dl_sehari": 1000.0, "dm_sekali": 0.0, "dm_sehari": 0.0, "info": "Antibiotikum Tetrasiklin"
    },
    "Codeini Phosphas (Kodein Fosfat)": {
        "dl_sekali": 10.0, "dl_sehari": 30.0, "dm_sekali": 60.0, "dm_sehari": 300.0, "info": "Antitusivum & Analgetikum, Narkotika"
    },
    "Coffeinum (Kafein)": {
        "dl_sekali": 100.0, "dl_sehari": 300.0, "dm_sekali": 500.0, "dm_sehari": 1500.0, "info": "Stimulan Sistem Saraf Pusat"
    },
    "Diazepamum (Diazepam)": {
        "dl_sekali": 2.0, "dl_sehari": 10.0, "dm_sekali": 0.0, "dm_sehari": 40.0, "info": "Anksiolitikum & Antikonvulsan"
    },
    "Digoxinum (Digokin)": {
        "dl_sekali": 0.25, "dl_sehari": 1.0, "dm_sekali": 1.0, "dm_sehari": 2.0, "info": "Kardiotonikum. Sangat toksik!"
    },
    "Ephedrini Hydrochloridum (Efedrin HCl)": {
        "dl_sekali": 10.0, "dl_sehari": 30.0, "dm_sekali": 50.0, "dm_sehari": 150.0, "info": "Simpatomimetikum / Bronkodilator"
    },
    "Erythromycinum (Eritromisin)": {
        "dl_sekali": 250.0, "dl_sehari": 1000.0, "dm_sekali": 500.0, "dm_sehari": 2000.0, "info": "Antibiotikum Makrolida"
    },
    "Guaifenesinum (GG / Glyceryl Guaiacolate)": {
        "dl_sekali": 100.0, "dl_sehari": 400.0, "dm_sekali": 0.0, "dm_sehari": 0.0, "info": "Ekspektoransia"
    },
    "Isoniazidum (INH / Isoniazid)": {
        "dl_sekali": 100.0, "dl_sehari": 300.0, "dm_sekali": 10.0, "dm_sehari": 10.0, "info": "Antituberkulosis (OAT)"
    },
    "Morphini Hydrochloridum (Morfin HCl)": {
        "dl_sekali": 5.0, "dl_sehari": 15.0, "dm_sekali": 20.0, "dm_sehari": 60.0, "info": "Analgetikum Narkotik Kuat"
    },
    "Papaverini Hydrochloridum (Papaverin HCl)": {
        "dl_sekali": 40.0, "dl_sehari": 120.0, "dm_sekali": 200.0, "dm_sehari": 600.0, "info": "Spasmolitikum otot polos"
    },
    "Phenobarbitalum (Fenobarbital/Luminal)": {
        "dl_sekali": 15.0, "dl_sehari": 45.0, "dm_sekali": 300.0, "dm_sehari": 600.0, "info": "Antikonvulsan & Sedativum berat"
    },
    "Prednisonum (Prednison)": {
        "dl_sekali": 5.0, "dl_sehari": 15.0, "dm_sekali": 0.0, "dm_sehari": 0.0, "info": "Glukokortikoid / Antiinflamasi Steroid"
    },
    "Sulfadiazinum (Sulfadiazin)": {
        "dl_sekali": 500.0, "dl_sehari": 2000.0, "dm_sekali": 1000.0, "dm_sehari": 8000.0, "info": "Antibiotikum Kemoterapeutik"
    },
    "Theophyllinum (Teofilin)": {
        "dl_sekali": 100.0, "dl_sehari": 300.0, "dm_sekali": 500.0, "dm_sehari": 1500.0, "info": "Bronkodilator Antiasma"
    },
    "Custom Obat (Ketik Manual)": {
        "dl_sekali": 0.0, "dl_sehari": 0.0, "dm_sekali": 0.0, "dm_sehari": 0.0, "info": "Pengaturan manual"
    }
}

# --- BAR SAMPING (SIDEBAR) ---
st.sidebar.header("🔑 Kredensial Bluesminds")
api_key_input = st.sidebar.text_input("Masukkan API Key Bluesminds Anda:", type="password")
model_ai = st.sidebar.selectbox("Pilih Model AI Jaringan:", ["gpt-4o", "claude-3-5-sonnet", "deepseek-chat"])

# --- PANEL UTAMA INPUT KLINIS ---
kategori_pasien = st.radio("Kategori Pasien:", ["Anak-Anak (Pediatri)", "Dewasa"], horizontal=True)

# Komponen Dropdown dengan Fitur Ketik & Cari Otomatis
pilihan_obat = st.selectbox("Pilih / Ketik Zat Aktif (Referensi Farmakope III):", list(DATABASE_FI3.keys()))
data_obat = DATABASE_FI3[pilihan_obat]

if pilihan_obat == "Custom Obat (Ketik Manual)":
    nama_obat = st.text_input("Masukkan Nama Obat:")
    dl_sekali_acuan = st.number_input("Dosis Lazim Sekali Dewasa (mg):", min_value=0.0, value=500.0)
    dl_sehari_acuan = st.number_input("Dosis Lazim Sehari Dewasa (mg):", min_value=0.0, value=1500.0)
    dm_sekali_acuan = st.number_input("Dosis Maksimum Sekali Dewasa (mg):", min_value=0.0, value=0.0)
    dm_sehari_acuan = st.number_input("Dosis Maksimum Sehari Dewasa (mg):", min_value=0.0, value=0.0)
else:
    nama_obat = pilihan_obat
    dl_sekali_acuan = data_obat["dl_sekali"]
    dl_sehari_acuan = data_obat["dl_sehari"]
    dm_sekali_acuan = data_obat["dm_sekali"]
    dm_sehari_acuan = data_obat["dm_sehari"]
    st.info(f"📋 **Golongan/Khasiat:** {data_obat['info']}")

# Aturan Penakaran Pasien
col_bb, col_freq = st.columns(2)
with col_bb:
    bb_pasien = st.number_input("Berat Badan Pasien (kg):", min_value=1.0, value=15.0 if kategori_pasien == "Anak-Anak (Pediatri)" else 60.0, step=0.5)
with col_freq:
    frekuensi = st.number_input("Frekuensi Pemberian (kali sehari):", min_value=1, max_value=6, value=3)

st.write("---")

# --- TOMBOL PROSES EKSEKUSI ---
if st.button("🚀 Hitung Posologi & Analisis AI"):
    st.success("✅ Perhitungan Selesai")
    
    final_sekali = 0.0
    final_sehari = 0.0
    
    if kategori_pasien == "Anak-Anak (Pediatri)":
        # Rumus Clark Klinis
        faktor_clark = bb_pasien / 68.0
        final_sekali = faktor_clark * dl_sekali_acuan
        final_sehari = final_sekali * frekuensi
        
        st.markdown(f"### 📊 Hasil Perhitungan Anak: {nama_obat}")
        st.write(f"**Proporsi Berat (Metode Clark):** {bb_pasien} kg / 68 = **{faktor_clark:.4f}**")
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric(label="Dosis Sekali Minum Anak", value=f"{final_sekali:.3f} mg")
        with c2:
            st.metric(label="Total Dosis Sehari Anak", value=f"{final_sehari:.3f} mg")
            
        # Pengecekan Persentase DM Anak jika ada di database
        if dm_sekali_acuan > 0 or dm_sehari_acuan > 0:
            st.markdown("#### 🚨 Kontrol Keamanan Dosis Maksimum (DM Anak):")
            dm_anak_sekali = faktor_clark * dm_sekali_acuan
            dm_anak_sehari = faktor_clark * dm_sehari_acuan
            
            persen_sekali = (final_sekali / dm_anak_sekali) * 100 if dm_anak_sekali > 0 else 0
            persen_sehari = (final_sehari / dm_anak_sehari) * 100 if dm_anak_sehari > 0 else 0
            
            st.write(f"⚠️ Batas DM Sekali Anak: {dm_anak_sekali:.3f} mg (Pemakaian saat ini: **{persen_sekali:.1f}%**)")
            st.write(f"⚠️ Batas DM Sehari Anak: {dm_anak_sehari:.3f} mg (Pemakaian saat ini: **{persen_sehari:.1f}%**)")
            
            if persen_sekali > 100 or persen_sehari > 100:
                st.error("🚨 DOSIS TOKSIK! Melebihi batas aman Farmakope Indonesia III.")
            else:
                st.success("🟢 Aman terhadap ambang batas indeks maksimum FI III.")
    else:
        # Perhitungan Pasien Dewasa
        st.markdown(f"### 📊 Hasil Perhitungan Dewasa: {nama_obat}")
        final_sekali = dl_sekali_acuan
        final_sehari = final_sekali * frekuensi
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric(label="Dosis Sekali Minum Dewasa", value=f"{final_sekali:.2f} mg")
        with c2:
            st.metric(label="Total Dosis Sehari Dewasa", value=f"{final_sehari:.2f} mg")
            
        if dm_sekali_acuan > 0 or dm_sehari_acuan > 0:
            st.markdown("#### 🚨 Kontrol Keamanan Dosis Maksimum (DM Dewasa):")
