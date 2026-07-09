import streamlit as st
import openai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator Universal + AI Bluesminds", page_icon="💊", layout="centered")

st.title("💊 Kalkulator Dosis Universal + AI Klinis")
st.subheader("Sistem Keputusan Terintegrasi Bluesminds API")
st.write("---")

# --- AKSES API BLUESMINDS ---
# Pengguna menginput API Key Bluesminds mereka sendiri demi keamanan data
st.sidebar.header("🔑 Kredensial Bluesminds")
api_key_input = st.sidebar.text_input("Masukkan API Key Bluesminds Anda:", type="password")

# Pilihan Model AI yang tersedia di infrastruktur Bluesminds
model_ai = st.sidebar.selectbox(
    "Pilih Model AI:",
    ["gpt-4o", "claude-3-5-sonnet", "deepseek-chat", "qwen-max"]
)

# --- FORMULIR INPUT MEDIS ---
kategori_pasien = st.radio("Kategori Pasien:", ["Anak-Anak (Pediatri)", "Dewasa"], horizontal=True)

nama_obat = st.text_input("Nama Obat:", value="Amoxicillin")
bb_pasien = st.number_input("Berat Badan Pasien (kg):", min_value=1.0, value=15.0 if kategori_pasien == "Anak-Anak (Pediatri)" else 60.0, step=0.5)

# Inisialisasi variabel hasil hitungan matematika murni
dosis_hasil_mg = 0.0
langkah_teks = ""

# --- LOGIKA MATEMATIKA STRUKTUR ---
if kategori_pasien == "Anak-Anak (Pediatri)":
    st.markdown("### 🧒 Parameter Anak (Metode Clark)")
    dosis_dewasa_acuan = st.number_input("Dosis Lazim Dewasa Acuan (mg):", min_value=1.0, value=500.0)
    
    # Hitung matematika dasar (Clark)
    faktor_clark = bb_pasien / 68.0
    dosis_hasil_mg = faktor_clark * dosis_dewasa_acuan
    langkah_teks = f"Perhitungan Rumus Clark: ({bb_pasien} kg / 68) x {dosis_dewasa_acuan} mg = {dosis_hasil_mg:.2f} mg."

else:
    st.markdown("### 🧑 Parameter Dewasa")
    metode_dewasa = st.selectbox("Metode Dewasa:", ["Dosis Tetap Standard", "Berdasarkan Berat Badan (mg/kg/hari)"])
    
    if metode_dewasa == "Dosis Tetap Standard":
        dosis_hasil_mg = st.number_input("Masukkan Dosis Standard (mg):", min_value=1.0, value=500.0)
        langkah_teks = f"Menggunakan Fixed Dose Dewasa: {dosis_hasil_mg:.2f} mg."
    else:
        dosis_per_kg = st.number_input("Dosis per kgBB (mg/kg/hari):", min_value=0.1, value=15.0)
        dosis_hasil_mg = dosis_per_kg * bb_pasien
        langkah_teks = f"Perhitungan BB Dewasa: {dosis_per_kg} mg/kg x {bb_pasien} kg = {dosis_hasil_mg:.2f} mg harian."

st.write("---")

# --- TOMBOL EKSEKUSI UTAMA ---
if st.button("🚀 Hitung Dosis & Jalankan Analisis AI"):
    
    # 1. Tampilkan Hasil Matematika Terlebih Dahulu (Akurat Tanpa Halusinasi)
    st.success("✅ Kalkulasi Matematika Selesai")
    st.metric(label="Rekomendasi Hasil Dosis", value=f"{dosis_hasil_mg:.2f} mg")
    st.caption(f"**Metode Dasar:** {langkah_teks}")
    
    # 2. Panggil AI Bluesminds untuk Memberikan Opini Klinis Tambahan
    if not api_key_input:
        st.warning("⚠️ Perhitungan matematika muncul, tetapi Analisis AI kosong karena Anda belum memasukkan API Key Bluesminds di bilah samping (sidebar).")
    else:
        st.markdown("### 🤖 Analisis Klinis Otomatis (Bluesminds AI)")
        
        with st.spinner("Menghubungi AI jaringan berdaulat Bluesminds..."):
            try:
                # Mengarahkan base URL ke gateway Bluesminds
                openai.api_base = "https://bluesminds.com"
                openai.api_key = api_key_input
                
                # Mengunci perilaku AI lewat System Prompt kefarmasian
                system_prompt = (
                    "Anda adalah seorang Apoteker Klinis profesional senior. Anda bertugas mengoreksi, "
                    "memvalidasi, dan memberikan catatan klinis penyerahan obat berdasarkan hasil hitungan dosis "
                    "yang diberikan oleh user. Batasi jawaban Anda hanya pada ruang lingkup farmasi, farmakoterapi, "
                    "dan safety alert keselamatan pasien. Berikan respons dalam bahasa Indonesia yang sangat rapi."
                )
                
                user_prompt = (
                    f"Pasien kategori: {kategori_pasien}. Nama obat: {nama_obat}. "
                    f"Berat badan: {bb_pasien} kg. Hasil hitungan matematika dosis sistem: {dosis_hasil_mg:.2f} mg.\n"
                    f"Mohon berikan telaah resep klinis singkat, tanda bahaya obat (jika ada), serta edukasi saat penyerahan obat."
                )
                
                # Mengirim request ke API Gateway
                response = openai.ChatCompletion.create(
                    model=model_ai,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2 # Konsisten dan ilmiah
                )
                
                # Menampilkan output teks AI ke web app
                st.info(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Gagal terhubung ke Bluesminds API: {str(e)}")

st.write("---")
st.caption("Aplikasi ini dibuat untuk tujuan demonstrasi dan uji klinis bersama dokter. Keputusan akhir resep berada di tangan dokter anak / apoteker penanggung jawab.")
