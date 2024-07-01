import pickle
import streamlit as st
import pandas as pd
import zipfile
from io import BytesIO
import os
import tempfile
import numpy as np

# Load model from a zip file
filename = 'prediksi_harga_rumah_smg.zip'
with zipfile.ZipFile(filename, 'r') as zip_ref:
    file_list = zip_ref.namelist()
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_ref.extractall(temp_dir)
        for file_name in file_list:
            file_path = os.path.join(temp_dir, file_name)
            with open(file_path, 'rb') as f:
                model_RF = pickle.load(f)

# Membuat sidebar
test = st.sidebar.radio("Menu", ["Beranda", "Data", "Labelling", "Prediksi", "Kontak"])

# Halaman Beranda
if test == "Beranda":
    st.header("Halo Selamat Datang Semuanya :wave:")
    st.markdown("#### Ini merupakan website yang dapat memprediksi harga rumah di Kota Jakarta Selatan sesuai dengan kriteria yang diinginkan oleh calon pembeli.")
    st.image('jakarta_selatan.png')
    st.markdown("#### Dengan adanya website ini, diharapkan dapat membantu para calon pembeli dalam menentukan harga rumah yang sesuai dan memenuhi kriteria rumah impiannya.")
    st.markdown("#### Jangan lupa untuk membuka 'Labelling' untuk mengetahui konversi tipe data ya :blush:")
    st.markdown("#### Selamat mencoba! :wave:")

# Halaman Data
if test == "Data":
    st.header("Data")
    st.write("Berikut merupakan data yang digunakan dalam prediksi harga rumah di Kota Jakarta Selatan.") 
    data = pd.read_csv("df_cleaning_web.csv")
    st.write(data)
    st.write("Sumber Data : Rumah123.com (Kota Jakarta Selatan) per Maret 2024")
    st.markdown("""
    ###### Catatan untuk jenis_rumah:
    - **rumah**: rumah biasa
    - **rumah featured**: rumah unggulan
    - **rumah premier**: rumah mewah
    """)


import streamlit as st

# Halaman Labelling
if test == "Labelling":
    st.subheader("Labelling")
    st.markdown("##### Untuk variabel 'Jenis Rumah' dan 'Lokasi' merupakan variabel kategorik sehingga harus dikonversi ke dalam variabel numerik agar dapat di prediksi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("###### Variabel jenis rumah")
        st.text("0 = jenis rumah biasa")
        st.text("1 = jenis rumah featured (unggulan)")
        st.text("2 = jenis rumah premier (mewah)")

    with col2:
        st.markdown("###### Variabel lokasi")
        st.text("1 = Kebayoran Lama, Jakarta Selatan")
        st.text("2 = Pancoran, Jakarta Selatan")
        st.text("3 = Setiabudi, Jakarta Selatan")
        st.text("4 = Kebayoran Baru, Jakarta Selatan")
        st.text("5 = Pasar Minggu, Jakarta Selatan")
        st.text("6 = Cilandak, Jakarta Selatan")
        st.text("7 = Pesanggrahan, Jakarta Selatan")
        st.text("8 = Mampang Prapatan, Jakarta Selatan")
        st.text("9 = Jagakarsa, Jakarta Selatan")
        st.text("10 = Tebet, Jakarta Selatan")



# Fungsi prediksi harga
def predict_house_price(Jenis_Rumah, Lokasi, KT, KM, Garasi, LT, LB):
    # Memasukkan data
    input_data = [[Jenis_Rumah, Lokasi, KT, KM, Garasi, LT, LB]]
    # Konversi list ke array numpy
    input_data_array = np.array(input_data)
    # Lakukan prediksi menggunakan model RandomForestRegressor
    prediction = model_RF.predict(input_data_array)
    # Konversi prediksi ke dalam bentuk miliar rupiah
    prediction_in_billions = prediction * 1_000_000_000
    # Membulatkan hasil prediksi dengan menghapus bagian desimal
    prediction_rounded = int(prediction_in_billions[0])
    # Format hasil prediksi dengan pemisah ribuan dan tambah "Rp."
    prediction_formatted = f"Rp. {prediction_rounded:,}".replace(",", ".")
    return prediction_formatted

# Halaman Prediksi
if test == "Prediksi":
    st.subheader("Prediksi harga rumah di Kota Semarang")
    
    # Membuat kolom prediksi
    col1, col2 = st.columns(2)

    with col1:
        Jenis_Rumah = st.selectbox("Jenis Rumah", [0, 1, 2])
    with col2:
        Lokasi = st.selectbox("Lokasi", [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    with col1:
        KT = st.number_input('Input Jumlah Kamar Tidur', min_value=2, max_value=9)
    with col2:
        KM = st.number_input('Input Jumlah Kamar Mandi', min_value=1, max_value=10)
    with col1:
        Garasi = st.number_input('Input Garasi (menampung berapa mobil)', min_value=1, max_value=10)
    with col2:
        LT = st.number_input('Input Luas Tanah (m2)', min_value=28)
    with col1:
        LB = st.number_input('Input Luas Bangunan (m2)', min_value=29)

    predict = ''

    if st.button("Prediksi Harga Rumah"):
        predict = predict_house_price(Jenis_Rumah, Lokasi, KT, KM, Garasi, LT, LB)
        st.markdown(f"Berikut merupakan prediksi harga rumah sesuai dengan kriteria yang anda inginkan :<br><h2>{predict}</h2>", unsafe_allow_html=True)

# Halaman Kontak

if test == "Kontak":
    st.subheader("Hai, mari terhubung dengan Tim kami! :wave:")

    st.markdown("""
    **Nama**    : Prabowo Danny Wicaksono 
    **Email**   : [Prabowo Danny Wicaksono@gmail.com](mailto:chaerul.tahir@gmail.com)
    """)
    
    st.markdown("""
    **Nama**    : Septiadi
    **Email**   : [septiadi@gmail.com](mailto:chaerul.tahir@gmail.com)
    """)
    
    st.markdown("""
    **Nama**    : Asep Rusdiana 
    **Email**   : [Asep Rusdiana@gmail.com](mailto:chaerul.tahir@gmail.com)
    """)

    st.markdown("""
    **Nama**    : Muh. Chaerul
    **Email**   : [Muh. Chaerul@gmail.com](mailto:chaerul.tahir@gmail.com)
    """)
