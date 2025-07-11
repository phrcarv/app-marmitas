import streamlit as st
import pandas as pd
import math
from fpdf import FPDF
import base64
from io import BytesIO

st.set_page_config(page_title="Marmitas Inteligentes", layout="centered")
st.title("🍱 Planejador de Marmitas Inteligente")

st.markdown("Preencha os dados abaixo para calcular as quantidades e gerar sua lista de compras automatizada.")

# Entrada do usuário
col1, col2 = st.columns(2)
dias = col1.number_input("Quantos dias de marmita?", min_value=1, max_value=30, value=7)

proteinas_disponiveis = [
    "Músculo cozido", "Moela de frango cozida", "Filé de frango grelhado",
    "Contra-filé grelhado", "Patinho grelhado", "Sobrecoxa de frango assada",
    "Lombo de porco assado", "Pernil de porco assado", "Acém cozido"
]

fatores_coccao = {
    "Arroz cozido": 2.7,
    "Feijão cozido": 2.0,
    "Vegetais tipo A": 1.0,
    "Músculo cozido": 0.65,
    "Moela de frango cozida": 0.55,
    "Filé de frango grelhado": 0.70,
    "Contra-filé grelhado": 0.60,
    "Patinho grelhado": 0.65,
    "Sobrecoxa de frango assada": 0.75,
    "Lombo de porco assado": 0.70,
    "Pernil de porco assado": 0.72,
    "Acém cozido": 0.62
}

st.subheader("🍚 Quantidades por refeição (em gramas)")
col1, col2 = st.columns(2)
arroz_p1 = col1.number_input("Arroz - Pessoa 1", value=100)
arroz_p2 = col2.number_input("Arroz - Pessoa 2", value=80)
feijao_p1 = col1.number_input("Feijão - Pessoa 1", value=80)
feijao_p2 = col2.number_input("Feijão - Pessoa 2", value=60)
vegetal_p1 = col1.number_input("Vegetais - Pessoa 1", value=100)
vegetal_p2 = col2.number_input("Vegetais - Pessoa 2", value=100)

st.subheader("🥩 Escolha a proteína e defina as quantidades")
proteina1 = st.selectbox("Proteína 1", proteinas_disponiveis, index=0)
proteina2 = st.selectbox("Proteína 2", proteinas_disponiveis, index=1)

col1, col2 = st.columns(2)
prot1_p1 = col1.number_input("Proteína 1 - Pessoa 1", value=120)
prot1_p2 = col2.number_input("Proteína 1 - Pessoa 2", value=100)
prot2_p1 = col1.number_input("Proteína 2 - Pessoa 1", value=180)
prot2_p2 = col2.number_input("Proteína 2 - Pessoa 2", value=160)

st.subheader("💰 Preço por kg (R$)")
col1, col2 = st.columns(2)
preco_arroz = col1.number_input("Arroz (kg)", value=5.0)
preco_feijao = col2.number_input("Feijão (kg)", value=7.0)
preco_vegetal = col1.number_input("Vegetais (kg)", value=4.0)
preco_prot1 = col2.number_input(f"{proteina1} (kg)", value=28.0)
preco_prot2 = col1.number_input(f"{proteina2} (kg)", value=30.0)

# Cálculo
def calcular_total(nome, p1, p2, fator, preco):
    total_cozido = (p1 + p2) * dias
    total_cru = math.ceil(total_cozido / fator)
    total_kg = round(total_cru / 1000, 2)
    custo = round(total_kg * preco, 2)
    return total_cru, total_kg, custo

itens = [
    ("Arroz cozido", arroz_p1, arroz_p2, preco_arroz),
    ("Feijão cozido", feijao_p1, feijao_p2, preco_feijao),
    ("Vegetais tipo A", vegetal_p1, vegetal_p2, preco_vegetal),
    (proteina1, prot1_p1, prot1_p2, preco_prot1),
    (proteina2, prot2_p1, prot2_p2, preco_prot2)
]

lista = []
total_geral = 0
for nome, p1, p2, preco in itens:
    fator = fatores_coccao[nome]
    cru, kg, custo = calcular_total(nome, p1, p2, fator, preco)
    total_geral += custo
    lista.append([nome, cru, kg, preco, custo])

df = pd.DataFrame(lista, columns=["Item", "Total cru (g)", "Qtd (kg)", "Preço/kg (R$)", "Custo estimado (R$)"])
st.subheader("🛒 Lista de Compras")
st.dataframe(df, use_container_width=True)
st.markdown(f"**💵 Total estimado: R$ {total_geral:.2f}**")

# Geração de PDF
def gerar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Lista de Compras - Marmitas", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    for row in lista:
        pdf.cell(0, 10, f"{row[0]}: {row[2]} kg - R$ {row[4]:.2f}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Total estimado: R$ {total_geral:.2f}", ln=True)

    buffer = BytesIO()
    pdf.output(buffer)
    pdf_bytes = buffer.getvalue()
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="lista_marmitas.pdf">📄 Baixar PDF</a>'
    return href

st.markdown("---")
if st.button("📥 Gerar PDF da Lista"):
    st.markdown(gerar_pdf(), unsafe_allow_html=True)
