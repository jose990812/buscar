import streamlit as st
import pandas as pd
import unicodedata
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

def normalizar(texto):
    texto = str(texto)
    texto = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("utf-8")
    return texto.lower()

def conectar_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credenciais_dict = st.secrets["google"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credenciais_dict, scope)
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_url(
        "https://docs.google.com/spreadsheets/d/1LPzNJYotNXRIvWOLtz7QlZa8sN2KNiMv_ZXf8gWyDs8/edit#gid=0"
    )
    worksheet = sheet.get_worksheet(0)
    dados = worksheet.get_all_records()
    return pd.DataFrame(dados)

def main():
    st.set_page_config(page_title="Busca de Números por Cidade", layout="centered")
    st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🔍 Busca de Números por Cidade</h1>", unsafe_allow_html=True)

    with st.spinner("Carregando dados da planilha..."):
        df = conectar_planilha()

    cidade_busca = st.text_input("Digite o nome da cidade:").strip()
    if st.button("Pesquisar"):
        if cidade_busca:
            cidade_normalizada = normalizar(cidade_busca)
            resultados = [
                linha.get("NUMERO", "")
                for _, linha in df.iterrows()
                if cidade_normalizada in normalizar(linha.get("CIDADE", ""))
            ]
            resultados = [r for r in resultados if r]
            if resultados:
                st.success(f"{len(resultados)} número(s) encontrado(s):")
                for numero in resultados:
                    st.code(numero)
                st.download_button("📥 Baixar Números", "\n".join(resultados), file_name="numeros.txt")
            else:
                st.warning("Nenhum número encontrado para essa cidade.")
        else:
            st.error("Digite o nome de uma cidade para pesquisar.")

    st.markdown("<hr><p style='text-align:center;color:gray;'>Desenvolvido por Ailton Mota © 2025</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

