"""
☁️ WordCloud Studio — Legibilidad y Contraste Total
"""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import io
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="WordCloud Studio",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILOS — DISEÑO EDITORIAL
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700;9..144,900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* ═══ BASE ═══ */
    html, body, [class*="css"], .stApp, button, input, textarea, select {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .stApp {
        background-color: #faf8f4 !important;
        background-image: radial-gradient(circle, rgba(194, 65, 12, 0.035) 1px, transparent 1px);
        background-size: 22px 22px;
    }

    /* ═══ SIDEBAR — TINTA OSCURA ═══ */
    [data-testid="stSidebar"] {
        background-color: #1a1814 !important;
        border-right: 1px solid #2a2622 !important;
    }

    [data-testid="stSidebar"] * {
        color: #e8e2d5 !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: #2a2622 !important;
        margin: 1.2rem 0 !important;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #c9c1b3 !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
    }

    /* Marca superior del sidebar */
    .sb-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding-bottom: 1.25rem;
        margin-bottom: 1.25rem;
        border-bottom: 1px solid #2a2622;
    }
    .sb-brand-mark {
        width: 40px; height: 40px;
        background: linear-gradient(135deg, #c2410c, #d97706);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.15rem;
        box-shadow: 0 4px 12px rgba(194, 65, 12, 0.35);
    }
    .sb-brand-name {
        font-family: 'Fraunces', serif !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        color: #f5f0e8 !important;
        line-height: 1.1;
        letter-spacing: -0.01em;
    }
    .sb-brand-tag {
        font-size: 0.65rem !important;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #8b8378 !important;
        font-weight: 700;
        margin-top: 3px;
    }

    /* Títulos de sección en el sidebar */
    .sb-section {
        font-size: 0.68rem !important;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #d97706 !important;
        font-weight: 800;
        margin: 0.4rem 0 0.9rem 0;
        padding-bottom: 0.55rem;
        border-bottom: 1px solid #2a2622;
    }

    /* Inputs, selects y textareas del sidebar */
    [data-testid="stSidebar"] div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] div[data-baseweb="input"] > div,
    [data-testid="stSidebar"] div[data-baseweb="base-input"],
    [data-testid="stSidebar"] input[type="text"] {
        background-color: #26221d !important;
        color: #f5f0e8 !important;
        border: 1px solid #3d3833 !important;
        border-radius: 8px !important;
        transition: border-color 0.15s ease !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="select"] > div:hover,
    [data-testid="stSidebar"] div[data-baseweb="input"] > div:hover {
        border-color: #d97706 !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #f5f0e8 !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label {
        color: #e8e2d5 !important;
    }
    [data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
        background-color: #d97706 !important;
        border-color: #d97706 !important;
    }

    /* POPOVERS (desplegables) — GLOBAL, para que se lean siempre */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] [role="listbox"] {
        background-color: #ffffff !important;
        border: 1px solid #ebe5d9 !important;
        border-radius: 10px !important;
        box-shadow: 0 12px 32px rgba(26, 24, 20, 0.14) !important;
    }
    div[data-baseweb="popover"] li,
    div[data-baseweb="popover"] [role="option"] {
        color: #1a1814 !important;
        font-weight: 500 !important;
    }
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="popover"] [role="option"]:hover,
    div[data-baseweb="popover"] [aria-selected="true"] {
        background-color: #f5f0e8 !important;
        color: #1a1814 !important;
    }

    /* ═══ HERO ═══ */
    .hero {
        padding: 0.75rem 0 1.75rem 0;
        border-bottom: 1px solid #ebe5d9;
        margin-bottom: 1.75rem;
    }
    .hero-label {
        font-size: 0.7rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: #c2410c;
        font-weight: 800;
        margin-bottom: 0.7rem;
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
    }
    .hero-label::before {
        content: '';
        display: inline-block;
        width: 26px;
        height: 1px;
        background: #c2410c;
    }
    .hero h1 {
        font-family: 'Fraunces', serif !important;
        font-size: 3.2rem !important;
        font-weight: 700 !important;
        color: #1a1814 !important;
        letter-spacing: -0.025em !important;
        line-height: 1 !important;
        margin: 0 0 0.85rem 0 !important;
    }
    .hero p {
        color: #6b6359 !important;
        font-size: 1.02rem !important;
        margin: 0 !important;
        max-width: 620px;
        line-height: 1.55 !important;
    }

    /* ═══ TABS ═══ */
    [data-baseweb="tab-list"] {
        gap: 0.5rem !important;
        border-bottom: 1px solid #ebe5d9 !important;
        background: transparent !important;
    }
    button[data-baseweb="tab"] {
        background: transparent !important;
        color: #8b8378 !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        padding: 0.75rem 1rem !important;
        border-radius: 8px 8px 0 0 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #1a1814 !important;
    }
    [data-baseweb="tab-highlight"] {
        background-color: #c2410c !important;
        height: 3px !important;
        border-radius: 3px 3px 0 0 !important;
    }
    [data-baseweb="tab-border"] {
        background-color: transparent !important;
    }

    /* ═══ TEXTAREA ═══ */
    .stTextArea textarea,
    .stTextArea > div > div > textarea {
        background-color: #ffffff !important;
        border: 1.5px solid #ebe5d9 !important;
        border-radius: 14px !important;
        color: #1a1814 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.65 !important;
        padding: 1.1rem 1.2rem !important;
        transition: all 0.15s ease !important;
        box-shadow: 0 1px 2px rgba(26, 24, 20, 0.03) !important;
    }
    .stTextArea textarea:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #c2410c !important;
        box-shadow: 0 0 0 4px rgba(194, 65, 12, 0.09) !important;
        outline: none !important;
    }
    .stTextArea textarea::placeholder {
        color: #b3ab9e !important;
    }

    /* ═══ FILE UPLOADER ═══ */
    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploaderDropzone"] {
        background-color: #ffffff !important;
        border: 2px dashed #d4cbbe !important;
        border-radius: 14px !important;
        padding: 1.5rem !important;
        transition: all 0.15s ease !important;
    }
    [data-testid="stFileUploader"] section:hover,
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #c2410c !important;
        background-color: #fffbf7 !important;
    }
    [data-testid="stFileUploader"] section * {
        color: #1a1814 !important;
    }
    [data-testid="stFileUploader"] button {
        background-color: #1a1814 !important;
        color: #f5f0e8 !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
    }

    /* ═══ BOTONES ═══ */
    .stButton > button {
        background: #1a1814 !important;
        color: #f5f0e8 !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        padding: 0.65rem 1.4rem !important;
        letter-spacing: 0.01em !important;
        transition: all 0.18s ease !important;
        box-shadow: 0 1px 2px rgba(26, 24, 20, 0.08) !important;
    }
    .stButton > button p { color: inherit !important; }
    .stButton > button:hover {
        background: #c2410c !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 18px rgba(194, 65, 12, 0.28) !important;
        color: #ffffff !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* ═══ DOWNLOAD BUTTON ═══ */
    [data-testid="stDownloadButton"] > button {
        background-color: #f5f0e8 !important;
        color: #1a1814 !important;
        border: 1.5px solid #d4cbbe !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        padding: 0.7rem 1.4rem !important;
        transition: all 0.18s ease !important;
    }
    [data-testid="stDownloadButton"] > button p { color: inherit !important; }
    [data-testid="stDownloadButton"] > button:hover {
        background-color: #1a1814 !important;
        color: #f5f0e8 !important;
        border-color: #1a1814 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 18px rgba(26, 24, 20, 0.18) !important;
    }

    /* ═══ MÉTRICAS ═══ */
    [data-testid="metric-container"] {
        background: #ffffff !important;
        border: 1px solid #ebe5d9 !important;
        border-radius: 14px !important;
        padding: 1.1rem 1.3rem !important;
        box-shadow: 0 1px 3px rgba(26, 24, 20, 0.04) !important;
        position: relative;
        overflow: hidden;
    }
    [data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #c2410c, #d97706, #f59e0b);
    }
    [data-testid="metric-container"] label,
    [data-testid="metric-container"] [data-testid="stMetricLabel"] {
        color: #8b8378 !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #1a1814 !important;
        font-family: 'Fraunces', serif !important;
        font-weight: 700 !important;
        font-size: 1.85rem !important;
        letter-spacing: -0.02em !important;
    }

    /* ═══ EXPANDER ═══ */
    [data-testid="stExpander"] {
        border: 1px solid #ebe5d9 !important;
        border-radius: 12px !important;
        background-color: #ffffff !important;
        overflow: hidden;
    }
    [data-testid="stExpander"] summary {
        font-weight: 600 !important;
        color: #1a1814 !important;
        padding: 0.9rem 1.1rem !important;
    }
    [data-testid="stExpander"] summary:hover {
        color: #c2410c !important;
    }

    /* ═══ ALERTAS ═══ */
    [data-testid="stAlert"] {
        border-radius: 12px !important;
        border: none !important;
    }

    /* ═══ SCROLLBAR ═══ */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: #faf8f4; }
    ::-webkit-scrollbar-thumb {
        background: #d4cbbe;
        border-radius: 10px;
        border: 2px solid #faf8f4;
    }
    ::-webkit-scrollbar-thumb:hover { background: #c2410c; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONFIGURACIONES Y PALETAS
# ─────────────────────────────────────────────
STOPWORDS_ES = {
    "de","la","el","en","y","a","los","del","se","las","un","por","con","no","una","su",
    "para","es","al","lo","como","mas","pero","sus","le","ya","o","este","si","porque",
    "esta","entre","cuando","muy","sin","sobre","tambien","me","hasta","hay","donde",
    "quien","desde","nos","durante","ni","contra","ese","eso","ante","bajo","tras",
    "que","fue","son","han","ha","ser","era","estan","siendo","sido","he","has","hemos",
    "habian","tiene","tienen","hacer","puede","pueden","asi","tan","parte","todo","todos",
    "todas","cada","otro","otra","otros","otras","mismo","misma","nuestro","nuestra",
    "ellos","ellas","nosotros","les","esa","esos","esas","aquel","aquella","aquellos",
}

PALETAS = {
    "Escala de grises":     ["#111827","#1f2937","#374151","#4b5563","#6b7280","#9ca3af"],
    "Azul corporativo":     ["#1e3a5f","#1d4ed8","#2563eb","#3b82f6","#60a5fa","#93c5fd"],
    "Verde institucional":  ["#064e3b","#065f46","#047857","#059669","#10b981","#34d399"],
    "Gris azulado":         ["#0f172a","#1e293b","#334155","#475569","#64748b","#94a3b8"],
    "Terracota":            ["#7c2d12","#9a3412","#c2410c","#ea580c","#f97316","#fb923c"],
}

EJEMPLO_TEXTO = """La inteligencia artificial es una disciplina de la informática orientada a desarrollar sistemas capaces de ejecutar tareas que requieren capacidades cognitivas humanas. El aprendizaje automático, las redes neuronales profundas y el procesamiento del lenguaje natural constituyen los pilares técnicos de los sistemas modernos. Los modelos de lenguaje de gran escala, la visión computacional y la robótica autónoma representan aplicaciones de vanguardia. La inteligencia artificial transforma sectores como la salud, la educación, la manufactura, las finanzas y el transporte."""

# ─────────────────────────────────────────────
# FUNCIONES AUXILIARES
# ─────────────────────────────────────────────
def limpiar_y_contar(texto, stopwords, min_len):
    texto = re.sub(r"http\S+|www\S+", "", texto.lower())
    texto = re.sub(r"[^a-záéíóúüñ\s]", " ", texto)
    palabras = [p for p in texto.split() if p not in stopwords and len(p) >= min_len]
    texto_limpio = " ".join(palabras)
    df_freq = pd.DataFrame(Counter(palabras).most_common(50), columns=["Palabra", "Frecuencia"])
    return texto_limpio, df_freq

def generar_wordcloud(texto_limpio, paleta_nombre, max_words, fondo, forma):
    import random
    colores = PALETAS[paleta_nombre]

    def color_func(*args, **kwargs):
        return random.choice(colores)

    mascara = None
    if forma == "Círculo":
        size = 500
        y, x = np.ogrid[:size, :size]
        cx, cy = size // 2, size // 2
        mascara = np.ones((size, size), dtype=np.uint8) * 255
        mascara[(x - cx)**2 + (y - cy)**2 <= (size // 2 - 12)**2] = 0

    wc = WordCloud(
        width=900, height=450, max_words=max_words,
        background_color=fondo, color_func=color_func,
        mask=mascara, collocations=False,
        min_font_size=10, max_font_size=110, margin=5
    ).generate(texto_limpio)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    fig.patch.set_facecolor(fondo)
    plt.tight_layout(pad=0)
    return fig

# ─────────────────────────────────────────────
# PANEL LATERAL
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div class="sb-brand">
            <div class="sb-brand-mark">☁️</div>
            <div>
                <div class="sb-brand-name">WordCloud</div>
                <div class="sb-brand-tag">Studio · v1.0</div>
            </div>
        </div>
        <div class="sb-section">⚙️ Personalización</div>
    """, unsafe_allow_html=True)

    paleta_sel = st.selectbox("Paleta de colores", list(PALETAS.keys()))
    fondo_sel = st.radio("Fondo de la nube", ["Blanco", "Negro"], horizontal=True)
    fondo_color = "white" if fondo_sel == "Blanco" else "black"
    forma_sel = st.selectbox("Forma", ["Rectángulo", "Círculo"])
    max_words = st.slider("Máx. palabras visualizadas", 20, 200, 80)

    st.divider()
    st.markdown('<div class="sb-section">🧹 Filtro de texto</div>', unsafe_allow_html=True)

    idioma = st.selectbox("Eliminar conectores en:", ["Español", "Inglés", "Ambos", "Ninguno"])
    min_longitud = st.slider("Longitud mínima de palabra", 2, 6, 3)
    palabras_extra = st.text_input("Excluir palabras específicas:", placeholder="ej: ejemplo, texto, pag")

# ─────────────────────────────────────────────
# CONTENIDO PRINCIPAL
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-label">Herramienta de visualización</div>
    <h1>WordCloud Studio</h1>
    <p>Genera nubes de palabras profesionales de manera rápida y sencilla. Ajusta, filtra y descarga en un flujo editorial.</p>
</div>
""", unsafe_allow_html=True)

tab_pegar, tab_subir = st.tabs(["✍️ Pegar / Escribir Texto", "📂 Subir Archivo (.txt / .csv)"])

texto_input = ""

with tab_pegar:
    col_input, col_ejemplo = st.columns([4, 1])
    with col_ejemplo:
        if st.button("Cargar Ejemplo", use_container_width=True):
            st.session_state["texto_main"] = EJEMPLO_TEXTO

    val_def = st.session_state.get("texto_main", "")
    texto_input = st.text_area(
        "Ingresa tu texto aquí:",
        value=val_def,
        height=190,
        placeholder="Escribe o pega aquí el artículo, respuestas de encuestas, discursos...",
        label_visibility="collapsed"
    )

with tab_subir:
    archivo = st.file_uploader("Selecciona un archivo (.txt o .csv):", type=["txt", "csv"])
    if archivo:
        if archivo.name.endswith(".txt"):
            texto_input = archivo.read().decode("utf-8", errors="ignore")
        elif archivo.name.endswith(".csv"):
            df_csv = pd.read_csv(archivo)
            col_txt = st.selectbox("Selecciona la columna que contiene el texto:", df_csv.columns.tolist())
            texto_input = " ".join(df_csv[col_txt].dropna().astype(str).tolist())

st.markdown("<br>", unsafe_allow_html=True)

btn_generar = st.button("🚀 Generar Nube de Palabras", use_container_width=True)

# ─────────────────────────────────────────────
# RESULTADOS
# ─────────────────────────────────────────────
if btn_generar or (texto_input.strip() and "auto_run" not in st.session_state):
    st.session_state["auto_run"] = True

    if not texto_input.strip():
        st.warning("⚠️ Ingresa un texto o sube un archivo antes de generar.")
        st.stop()

    sw = set()
    if idioma in ("Español", "Ambos"): sw |= STOPWORDS_ES
    if idioma in ("Inglés", "Ambos"): sw |= set(STOPWORDS)
    if palabras_extra.strip():
        sw |= {p.strip().lower() for p in palabras_extra.split(",") if p.strip()}

    texto_limpio, df_freq = limpiar_y_contar(texto_input, sw, min_longitud)

    if not texto_limpio.strip():
        st.error("No se encontraron palabras válidas. Ajusta la longitud mínima o los filtros.")
        st.stop()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total palabras analizadas", f"{len(texto_limpio.split()):,}")
    c2.metric("Vocabulario único", f"{len(df_freq):,}")
    c3.metric("Palabra más frecuente", df_freq.iloc[0]["Palabra"] if not df_freq.empty else "-")

    st.markdown("<br>", unsafe_allow_html=True)

    fig_wc = generar_wordcloud(texto_limpio, paleta_sel, max_words, fondo_color, forma_sel)
    st.pyplot(fig_wc, use_container_width=True)

    buf = io.BytesIO()
    fig_wc.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor=fig_wc.get_facecolor())
    buf.seek(0)

    st.download_button("⬇️ Descargar Imagen PNG", data=buf.read(), file_name="nube_de_palabras.png", mime="image/png", use_container_width=True)

    with st.expander("📊 Ver tabla de frecuencias (Top 20)"):
        st.dataframe(df_freq.head(20), use_container_width=True)

    plt.close("all")
