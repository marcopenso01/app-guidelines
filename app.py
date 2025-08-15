# ==============================================================================
# 1. IMPORT DELLE LIBRERIE NECESSARIE
# ==============================================================================
import streamlit as st
import base64
import os

# ==============================================================================
# 2. IMPOSTAZIONI E STILI
# ==============================================================================
st.set_page_config(
    page_title="Archivio Linee Guida AI",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
    <style>
        h1 {
            text-align: center;
            padding-top: 0rem;
        }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. UI E LOGICA PRINCIPALE (La mettiamo prima dello script)
# ==============================================================================
st.title("Archivio Intelligente di Linee Guida con Assistente AI")
st.markdown("---")

st.sidebar.title("📚 Indice Argomenti")
st.sidebar.markdown("Scegli un documento o usa l'assistente virtuale in basso a destra.")

topic_options = ["--- Seleziona un argomento ---"] + list(st.session_state.get('topics', {}).keys())
# Carichiamo i topic nello stato della sessione per evitare ricaricamenti
if 'topics' not in st.session_state:
    st.session_state.topics = {
        "Cardiomyopathies": "Cardiomyopathies.pdf",
        "Atrial Fibrillation": "Atrial_fibrillation.pdf",
        "Arterial and Aortic Diseases": "Arterial_and_aortic_diseases.pdf"
    }
PDF_DIRECTORY = "linee_guida"
TOPICS = st.session_state.topics

selected_topic = st.sidebar.selectbox("Linee Guida Disponibili:", ["--- Seleziona un argomento ---"] + list(TOPICS.keys()))

if selected_topic == "--- Seleziona un argomento ---":
    st.info("**Benvenuto!** Usa il menu a sinistra per leggere un documento oppure clicca sull'icona della chat per fare una domanda specifica.")
else:
    st.header(f"📄 Linee Guida: {selected_topic}")
    pdf_filename = TOPICS.get(selected_topic)
    if pdf_filename:
        pdf_path = os.path.join(PDF_DIRECTORY, pdf_filename)
        try:
            with open(pdf_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error(f"Errore: File non trovato a questo percorso: {pdf_path}")
        except Exception as e:
            st.error(f"Si è verificato un errore imprevisto: {e}")

st.sidebar.markdown("---")
st.sidebar.write("App creata per la consultazione rapida.")

# ==============================================================================
# 4. CODICE DEL CHATBOT (Lo mettiamo alla fine)
# ==============================================================================

# Creiamo il punto di ancoraggio invisibile per il chatbot
st.markdown('<div id="botpress-webchat-container"></div>', unsafe_allow_html=True)

# Definiamo lo script del chatbot CON il selettore corretto
BOTPRESS_SCRIPT = """
<script src="https://cdn.botpress.cloud/webchat/v3.2/inject.js"></script>
<script>
    // Attendiamo che la pagina sia completamente caricata prima di inizializzare
    window.addEventListener('load', function() {
        window.botpress.init({
            "botId": "58341229-69e9-461a-9cdc-72b2561974d1",
            "clientId": "15df004f-3be1-4765-9ce7-219091c75c53",
            
            // LA MODIFICA CHIAVE: Diciamo allo script dove agganciarsi
            "selector": "#botpress-webchat-container",

            "configuration": {
                "version": "v1",
                "botName": "Assistente Clinico",
                "botDescription": "Posso aiutarti a trovare informazioni nelle linee guida.",
                "color": "#3276EA"
            }
        });
    });
</script>
"""
# Iniettiamo lo script nella pagina
st.markdown(BOTPRESS_SCRIPT, unsafe_allow_html=True)
