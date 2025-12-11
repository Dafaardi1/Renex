import streamlit as st

st.title("Hitung Luas Persegi Panjang")

panjang = st.number_input ("masukan nilai panjang", 0)
lebar= st.number_input ("masukkan nilai lebar")
hitung= st.button("hitung luas")
