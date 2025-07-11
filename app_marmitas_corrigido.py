
import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf import FPDF
import math

st.set_page_config(page_title="Calculadora de Marmitas", layout="centered")

st.title("🍱 Calculadora de Marmitas Congeladas")

st.markdown("Preencha as informações abaixo para calcular quanto comprar de cada alimento:")

col1, col2 = st.columns(2)

with col1:
    dias = st.number_input("Quantidade de dias:", min_value=1, value=7)

with col2:
    pessoas = st.number_input("Quantidade de pessoas:", min_value=1, value=2)

st.markdown("---")

st.subheader("🥦 Porção por pessoa (alimento já cozido)")

col1, col2, col3 = st.columns(3)
with col1:
    arroz_cozido = st.number_input("Arroz (g)", min_value=0, value=100)
with col2:
    feijao_cozido = st.number_input("Feijão (g)", min_value=0, value=80)
with col3:
    legumes_cozido = st.number_input("Legumes (g)", min_value=0, value=100)

st.subheader("🍗 Proteína")

proteinas = {
    "Frango desfiado": 0.65,
    "Carne moída": 0.75,
    "Peito de frango em cubos": 0.70,
    "Patinho em cubos": 0.75,
    "Ovo cozido": 1.00,
    "Tofu": 0.90,
    "Peixe": 0.75
}

proteina_escolhida = st.selectbox("Escolha a proteína:", list(proteinas.keys()))
quantidade_proteina = st.number_input("Quantidade de proteína por pessoa (g)", min_value=0, value=120)

st.markdown("---")

# Fatores de cocção
fatores = {
    "Arroz": 2.5,
    "Feijão": 2.8,
    "Legumes": 1.2,
    "Proteína": proteinas[proteina_escolhida]
}

# Cálculo total por item
def calcular_quantidade_necessaria(por_pessoa, fator, dias, pessoas):
    total_cozido = por_pessoa * dias * pessoas
    total_cru = total_cozido / fator
    return total_cozido, math.ceil(total_cru)

resultados = {
    "Arroz": calcular_quantidade_necessaria(arroz_cozido, fatores["Arroz"], dias, pessoas),
    "Feijão": calcular_quantidade_necessaria(feijao_cozido, fatores["Feijão"], dias, pessoas),
    "Legumes": calcular_quantidade_necessaria(legumes_cozido, fatores["Legumes"], dias, pessoas),
    proteina_escolhida: calcular_quantidade_necessaria(quantidade_proteina, fatores["Proteína"], dias, pessoas)
}

df_resultado = pd.DataFrame([
    {
        "Item": item,
        "Total necessário (g) cozido": round(val[0]),
        "Comprar cru (g)": val[1]
    } for item, val in resultados.items()
])

st.subheader("📊 Resultado:")

st.dataframe(df_resultado, use_container_width=True)

# Função para gerar o PDF
def gerar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Lista de Compras para Marmitas", ln=True, align="C")
    pdf.ln(10)
    for index, row in df_resultado.iterrows():
        texto = f"{row['Item']}: Comprar {row['Comprar cru (g)']}g (rende {row['Total necessário (g) cozido']}g)"
        pdf.cell(200, 10, txt=texto, ln=True)
    buffer = BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()

st.markdown("---")
pdf_file = gerar_pdf()
st.download_button(
    label="📥 Baixar PDF da Lista",
    data=pdf_file,
    file_name="lista_compras.pdf",
    mime="application/pdf"
)
