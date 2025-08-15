# ==============================================================================
# 1. IMPORT DELLE LIBRERIE NECESSARIE
# ==============================================================================
import streamlit as st
import base64
import os
# NOTA: NON importiamo più 'html' da streamlit.components

# ==============================================================================
# 2. IMPOSTAZIONI E STILI
# ==============================================================================
st.set_page_config(
    page_title="Archivio Linee Guida AI",
    page_icon="🤖",
    layout="wide"
)

# --- NUOVA SEZIONE PER LO STILE ---
# Iniezione di CSS per centrare il titolo e rimuovere lo spazio in alto
st.markdown("""
    <style>
        /* Seleziona l'elemento del titolo principale */
        h1 {
            text-align: center; /* Centra il testo */
            padding-top: 0rem; /* Rimuove lo spazio extra sopra */
        }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. CODICE DEL CHATBOT
# ==============================================================================
BOTPRESS_SCRIPT = """
<script src="https://cdn.botpress.cloud/webchat/v3.2/inject.js"></script>
<script>
  window.botpress.init({
      "botId": "58341229-69e9-461a-9cdc-72b2561974d1",
      "clientId": "15df004f-3be1-4765-9ce7-219091c75c53",
      "configuration": {
        "version": "v1",
        "botName": "Assistente Clinico",
        "botDescription": "Posso aiutarti a trovare informazioni nelle linee guida.",
        "color": "#3276EA"
      }
  });
</script>
"""
# --- METODO DI INIEZIONE CORRETTO ---
# Usiamo st.markdown per inserire lo script direttamente nel corpo della pagina
st.markdown(BOTPRESS_SCRIPT, unsafe_allow_html=True)


# ==============================================================================
# 4. FUNZIONI DI SUPPORTO
# ==============================================================================
def show_pdf(file_path):
    try:
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Errore: File non trovato a questo percorso: {file_path}")
    except Exception as e:
        st.error(f"Si è verificato un errore imprevisto: {e}")

# ==============================================================================
# 5. CONFIGURAZIONE DEI DATI
# ==============================================================================
PDF_DIRECTORY = "linee_guida"
TOPICS = {
    "Cardiomyopathies": "Cardiomyopathies.pdf",
    "Atrial Fibrillation": "Atrial_fibrillation.pdf",
    "Arterial and Aortic Diseases": "Arterial_and_aortic_diseases.pdf"
}

# ==============================================================================
# 6. UI E LOGICA PRINCIPALE
# ==============================================================================
st.title("Archivio Intelligente di Linee Guida con Assistente AI") # Titolo ora centrato dal CSS
st.markdown("---")

st.sidebar.title("📚 Indice Argomenti")
st.sidebar.markdown("Scegli un documento o usa l'assistente virtuale in basso a destra.")

topic_options = ["--- Seleziona un argomento ---"] + list(TOPICS.keys())
selected_topic = st.sidebar.selectbox("Linee Guida Disponibili:", topic_options)

if selected_topic == "--- Seleziona un argomento ---":
    st.info("**Benvenuto!** Usa il menu a sinistra per leggere un documento oppure clicca sull'icona della chat per fare una domanda specifica.")
else:
    st.header(f"📄 Linee Guida: {selected_topic}")
    pdf_filename = TOPICS.get(selected_topic)
    if pdf_filename:
        pdf_path = os.path.join(PDF_DIRECTORY, pdf_filename)
        show_pdf(pdf_path)

st.sidebar.markdown("---")
st.sidebar.write("App creata per la consultazione rapida.")
