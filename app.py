
import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="VALIDATA® | Formulario Predictivo", layout="centered")

st.title("Formulario Predictivo VALIDATA®")
st.markdown("Completa la información del trámite de forma profesional y segura.")

with st.form("formulario_validata"):
    nombre = st.text_input("Nombre completo")
    dni = st.text_input("DNI")
    correo = st.text_input("Correo electrónico")
    telefono = st.text_input("Teléfono")
    provincia = st.selectbox("Provincia", ["Buenos Aires", "CABA", "Córdoba", "Santa Fe", "Otra"])
    tramite = st.selectbox("Tipo de trámite", ["Firma digital", "Legalización", "Carga de documentos", "Otro"])
    sector = st.selectbox("Sector", ["Salud", "Jurídico", "Educativo", "Otro"])
    consulta = st.text_area("¿Cuál es tu necesidad puntual?")
    archivo = st.file_uploader("Subí tu documento (opcional)")
    acepta = st.checkbox("Acepto la política de privacidad")

    submitted = st.form_submit_button("Enviar")

    if submitted:
        if not (nombre and dni and correo and acepta):
            st.error("⚠️ Debes completar todos los campos obligatorios y aceptar la política.")
        else:
            try:
                scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
                creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
                client = gspread.authorize(creds)
                sheet = client.open("Consultas VALIDATA").sheet1

                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data = [fecha, nombre, dni, correo, telefono, provincia, tramite, sector, consulta, "Sí" if archivo else "No", "Sí" if acepta else "No"]
                sheet.append_row(data)

                st.success("✅ Consulta enviada correctamente. ¡Gracias por confiar en VALIDATA®!")
            except Exception as e:
                st.error(f"❌ Error al guardar los datos: {e}")
