# ==============================================================================
# 1) IMPORT
# ==============================================================================
import os
import base64
from pathlib import Path
import streamlit as st

# ==============================================================================
# 2) CONFIG & STILI
#  - set_page_config deve essere la PRIMA chiamata Streamlit
# ==============================================================================
st.set_page_config(
    page_title="Archivio Linee Guida AI",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
    <style>
      h1 { text-align:center; padding-top:0rem; }
      .sidebar .sidebar-content { padding-top: 1rem !important; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3) COSTANTI & UTILITIES
# ==============================================================================
# Directory dei PDF: riferita al file corrente (robusto per Streamlit Cloud)
ROOT = Path(__file__).resolve().parent
PDF_DIRECTORY = ROOT / "linee_guida"

# Mappa "titolo" -> "filename". Puoi mantenerla per titoli curati
DEFAULT_TOPICS = {
    "Cardiomyopathies": "Cardiomyopathies.pdf",
    "Atrial Fibrillation": "Atrial_fibrillation.pdf",
    "Arterial and Aortic Diseases": "Arterial_and_aortic_diseases.pdf",
}

def discover_pdfs(directory: Path) -> dict:
    """Se vuoi generare i topic automaticamente dai PDF presenti in cartella."""
    topics = {}
    if directory.exists():
        for p in sorted(directory.glob("*.pdf")):
            nice = p.stem.replace("_", " ").title()
            topics[nice] = p.name
    return topics

def ensure_topics(map_or_discover=True) -> dict:
    """
    1) Usa la mappa curata DEFAULT_TOPICS se i file esistono.
    2) Se mancano file, rimuovili dalla mappa.
    3) Se directory vuota o vuoi full-auto, prova discovery.
    """
    topics = {}
    for title, fname in DEFAULT_TOPICS.items():
        path = PDF_DIRECTORY / fname
        if path.exists():
            topics[title] = fname

    if not topics and map_or_discover:
        # fallback a discovery automatica
        topics = discover_pdfs(PDF_DIRECTORY)

    return topics

def render_pdf_inline(pdf_path: Path, height: int = 800):
    """Mostra PDF in iframe base64; aggiungi anche un pulsante download."""
    with open(pdf_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    iframe = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="{height}" type="application/pdf"></iframe>'
    st.markdown(iframe, unsafe_allow_html=True)
    st.download_button(
        "⬇️ Scarica PDF",
        data=data,
        file_name=pdf_path.name,
        mime="application/pdf",
        use_container_width=True,
    )

# ==============================================================================
# 4) STATO & PARAMETRI
# ==============================================================================
if "topics" not in st.session_state:
    st.session_state.topics = ensure_topics()

TOPICS = st.session_state.topics  # dict: titolo -> filename

# Deep-link: ?topic=Titolo esatto
qp = st.query_params
if "topic" in qp and qp["topic"] in TOPICS:
    st.session_state["selected_topic"] = qp["topic"]

# ==============================================================================
# 5) UI PRINCIPALE
# ==============================================================================
st.title("Archivio Intelligente di Linee Guida con Assistente AI")
st.markdown("---")

with st.sidebar:
    st.title("📚 Indice Argomenti")
    st.markdown("Scegli un documento o usa l'assistente virtuale in basso a destra.")
    options = ["— Seleziona —"] + list(TOPICS.keys())
    idx_default = 0
    if "selected_topic" in st.session_state and st.session_state["selected_topic"] in TOPICS:
        idx_default = options.index(st.session_state["selected_topic"])
    selected = st.selectbox("Linee Guida Disponibili:", options, index=idx_default, key="sb_select")

if selected == "— Seleziona —":
    st.info("**Benvenuto!** Scegli un documento a sinistra oppure clicca sull’icona della chat per fare una domanda.")
else:
    st.header(f"📄 Linee Guida: {selected}")
    st.query_params["topic"] = selected  # aggiorna URL per deep-link
    pdf_filename = TOPICS.get(selected)
    pdf_path = PDF_DIRECTORY / pdf_filename
    if pdf_filename:
        if pdf_path.exists():
            try:
                render_pdf_inline(pdf_path, height=820)
            except Exception as e:
                st.error(f"Si è verificato un errore durante il rendering del PDF: {e}")
        else:
            st.error(f"File non trovato: `{pdf_path}`")
    else:
        st.warning("Documento non disponibile.")

st.sidebar.markdown("---")
st.sidebar.write("App per consultazione rapida delle linee guida.")

# ==============================================================================
# 6) CHATBOT (Botpress) — modalità diagnostica
# ==============================================================================
from streamlit.components.v1 import html as st_html

bot_id = st.secrets.get("botpress", {}).get("botId") or os.environ.get("BOTPRESS_BOT_ID")
client_id = st.secrets.get("botpress", {}).get("clientId") or os.environ.get("BOTPRESS_CLIENT_ID")

# Mostro a schermo se i secrets sono stati letti (senza esporli)
st.caption(f"🔎 BotID presente: {'✔️' if bool(bot_id) else '❌'}  |  ClientID presente: {'✔️' if bool(client_id) else '❌'}")

if not bot_id or not client_id:
    st.error("Bot non configurato: aggiungi `botId` e `clientId` nei secrets.")
else:
    # Prova 1: EMBEDDED dentro un div visibile
    st.markdown(
        """
        <div id="bp-status" style="padding:8px;border-radius:8px;background:#111;color:#fff;margin-bottom:8px;">
          Avvio Botpress…
        </div>
        <div id="botpress-webchat-container" style="width:100%;height:600px;border:1px solid #333;border-radius:10px;"></div>
        """,
        unsafe_allow_html=True
    )

    st_html(f"""
      <script src="https://cdn.botpress.cloud/webchat/v3.2/inject.js"></script>
      <script>
        const statusEl = document.getElementById('bp-status');
        function setStatus(msg) {{
          if (statusEl) statusEl.innerText = msg;
          console.log("[BP]", msg);
        }}

        window.addEventListener('load', function() {{
          setStatus("Pagina caricata, inizializzo…");
          try {{
            if (!window.botpress) {{
              setStatus("❌ window.botpress non presente (inject.js bloccato?)");
              return;
            }}
            window.botpress.init({{
              botId: "{bot_id}",
              clientId: "{client_id}",
              selector: "#botpress-webchat-container",
              configuration: {{
                version: "v1",
                botName: "Assistente Clinico",
                botDescription: "Posso aiutarti a trovare informazioni nelle linee guida.",
                composerPlaceholder: "Scrivi un messaggio…",
                useSessionStorage: true
              }}
            }});
            setStatus("✔️ Embedded init inviato. Se non vedi nulla tra poco, provo fallback flottante…");
            // Fallback alla bolla flottante dopo 2.5s se il container è ancora vuoto
            setTimeout(function() {{
              const host = document.querySelector("#botpress-webchat-container iframe");
              if (!host) {{
                setStatus("↪️ Fallback: inizializzo bolla flottante…");
                window.botpress.init({{
                  botId: "{bot_id}",
                  clientId: "{client_id}",
                  configuration: {{
                    version: "v1",
                    botName: "Assistente Clinico",
                    botDescription: "Posso aiutarti a trovare informazioni nelle linee guida.",
                    composerPlaceholder: "Scrivi un messaggio…",
                    useSessionStorage: true
                  }}
                }});
                setStatus("✔️ Fallback inviato. Se ancora non appare, controlla Console (F12) ed estensioni.");
              }} else {{
                setStatus("✔️ Embedded avviato (iframe rilevato).");
              }}
            }}, 2500);
          }} catch (e) {{
            console.error("Botpress init error:", e);
            setStatus("❌ Errore in init: vedi console (F12).");
          }}
        }});
      </script>
    """, height=0, width=0)
