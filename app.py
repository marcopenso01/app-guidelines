# ==============================================================================
# 1. IMPORT DELLE LIBRERIE NECESSARIE
# ==============================================================================
import streamlit as st
import base64
import os

# ==============================================================================
# 2. IMPOSTAZIONI DELLA PAGINA STREAMLIT
# ==============================================================================
# Queste impostazioni vengono applicate a tutta l'app (titolo nel tab del browser, icona, layout)
st.set_page_config(
    page_title="Archivio Linee Guida",
    page_icon="⚕️",  # Puoi usare un'emoji o un URL di un'icona
    layout="wide"  # "wide" usa più spazio orizzontale, ideale per i PDF
)

# ==============================================================================
# 3. FUNZIONI DI SUPPORTO
# ==============================================================================

def show_pdf(file_path):
    """
    Mostra un file PDF all'interno dell'app Streamlit.
    Il trucco consiste nel leggere il file in modalità binaria, codificarlo in base64
    e inserirlo in un tag <iframe> HTML.
    """
    try:
        with open(file_path, "rb") as f:
            # Legge il file e lo codifica in base64
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        # Crea l'HTML per l'iframe che mostrerà il PDF
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        
        # Mostra l'HTML nell'app
        st.markdown(pdf_display, unsafe_allow_html=True)
    
    except FileNotFoundError:
        st.error(f"Errore: File non trovato a questo percorso: {file_path}")
        st.warning("Assicurati che il nome del file nel dizionario 'TOPICS' e nella cartella 'linee_guida' corrisponda esattamente.")
    except Exception as e:
        st.error(f"Si è verificato un errore imprevisto durante il caricamento del PDF: {e}")

# ==============================================================================
# 4. CONFIGURAZIONE DEI DATI (I TUOI PDF)
# ==============================================================================

# Definisci il nome della cartella che contiene i documenti
PDF_DIRECTORY = "linee_guida"

# Crea un dizionario per mappare i nomi dei topic che l'utente vedrà
# con i nomi dei file PDF corrispondenti.
# IMPORTANTE: I nomi dei file devono essere ESATTAMENTE gli stessi
# di quelli presenti nella cartella 'linee_guida'.
TOPICS = {
    TOPICS = {
    "Cardiomyopathies": "Cardiomyopathies.pdf",
    "Atrial Fibrillation": "Atrial_fibrillation.pdf",
    "Arterial and Aortic Diseases": "Arterial_and_aortic_diseases.pdf"          # Esempio aggiuntivo
    # ---> Aggiungi qui altre righe per ogni nuova linea guida <---
}

# ==============================================================================
# 5. COSTRUZIONE DELL'INTERFACCIA UTENTE (UI) E LOGICA PRINCIPALE
# ==============================================================================

# Titolo principale dell'applicazione
st.title("⚕️ Archivio Intelligente di Linee Guida Cliniche")
st.markdown("---") # Una linea orizzontale per separare

# --- BARRA LATERALE PER LA NAVIGAZIONE ---
st.sidebar.title("📚 Indice Argomenti")
st.sidebar.markdown("Scegli un argomento per visualizzare il documento.")

# Creiamo la lista di opzioni per il menu a tendina
# Iniziamo con un'opzione di default per guidare l'utente
topic_options = ["--- Seleziona un argomento ---"] + list(TOPICS.keys())

# Creiamo il menu a tendina (selectbox) nella barra laterale
selected_topic = st.sidebar.selectbox(
    "Linee Guida Disponibili:",
    topic_options
)

# --- AREA PRINCIPALE DELLA PAGINA ---

# Controlliamo cosa ha selezionato l'utente
if selected_topic == "--- Seleziona un argomento ---":
    # Se non ha ancora scelto, mostriamo una pagina di benvenuto
    st.info("**Benvenuto!** Usa il menu a sinistra per consultare una linea guida.")
    st.markdown("""
    ### Come funziona questa applicazione?
    
    1.  **Naviga:** Seleziona un argomento clinico dal menu a tendina nella barra laterale a sinistra.
    2.  **Consulta:** L'applicazione caricherà e visualizzerà il documento PDF ufficiale corrispondente.
    3.  **Interroga (Prossimamente):** A breve verrà integrato un assistente virtuale (chatbot) che ti permetterà di fare domande dirette sul contenuto dei documenti per trovare informazioni in pochi secondi.
    """)
    # Puoi aggiungere un'immagine per rendere la home page più accattivante
    # st.image("path/to/your/image.jpg", caption="Medicina basata sull'evidenza, a portata di click.")

else:
    # Se l'utente ha scelto un topic, mostriamo il PDF
    st.header(f"📄 Linee Guida: {selected_topic}")
    
    # Recupera il nome del file PDF dal nostro dizionario
    pdf_filename = TOPICS.get(selected_topic)
    
    if pdf_filename:
        # Costruisce il percorso completo al file (es. "linee_guida/cardiomiopatie.pdf")
        # os.path.join è il modo migliore per unire percorsi, funziona su tutti i sistemi operativi
        pdf_path = os.path.join(PDF_DIRECTORY, pdf_filename)
        
        # Chiama la nostra funzione per visualizzare il PDF
        show_pdf(pdf_path)
    else:
        # Questo errore non dovrebbe mai apparire se la logica è corretta, ma è una buona pratica includerlo
        st.error("Si è verificato un errore nella selezione del topic. Riprova.")

# Aggiungiamo un piccolo footer nella sidebar
st.sidebar.markdown("---")
st.sidebar.write("App creata per la consultazione rapida.")
