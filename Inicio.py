"""
☁️ WordCloud Studio — Versión con Alto Contraste y Legibilidad Garantizada
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
# CONFIGURACIÓN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="WordCloud Studio",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILOS — Forzado de contraste (Modo claro/oscuro compatible)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Fondo de la aplicación */
    .stApp {
        background-color: #f8fafc !important;
    }

    /* ── MENÚ LATERAL (SIDEBAR) ── */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    /* Forzar color oscuro en absolutamente TODOS los textos del Sidebar */
    [data-testid="stSidebar"] *, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] div {
        color: #0f172a !important;
    }

    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }

    /* ── ÁREA PRINCIPAL ── */
    .title-container h1 {
        font-size: 2.1rem !important;
        font-weight: 700 !important;
        color: #0f172a !important;
        margin-bottom: 0.2rem !important;
    }
    .title-container p {
        color: #475569 !important;
        font-size: 0.95rem !important;
    }

    /* Forzar etiquetas principales */
    [data-testid="stWidgetLabel"] p {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

    /* ── CUADRO DE TEXTO (TEXTAREA) Y DESPLEGABLES ── */
    textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        font-size: 0.95rem !important;
    }
    textarea::placeholder {
        color: #94a3b8 !important;
    }
    textarea:focus {
        border-color: #0f172a !important;
        box-shadow: 0 0 0 2px rgba(15, 23, 42, 0.1) !important;
    }

    /* Selectbox y Dropdowns */
    [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 6px !important;
        color: #0f172a !important;
    }
    [data-baseweb="select"] span {
        color: #0f172a !important;
    }

    /* ── PESTAÑAS (TABS) ── */
    button[data-baseweb="tab"] {
        color: #64748b !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #0f172a !important;
        border-bottom-color: #0f172a !important;
    }

    /* ── BOTONES ── */
    .stButton > button {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.2rem !important;
        transition: background-color 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: #1e293b !important;
    }

    /* Botón de descarga */
    [data-testid="stDownloadButton"] > button {
        background-color: #334155 !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }
    [data-testid="stDownloadButton"] > button:hover {
        background-color: #0f172a !important;
    }

    /* Métricas */
    [data-testid="metric-container"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 14px !important;
    }
    [data-testid="metric-container"] label {
        color: #64748b !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #0f172a !important;
    }
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
# PANEL LATERAL (Personalización)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Personalización")
    
    paleta_sel = st.selectbox("Paleta de colores", list(PALETAS.keys()))
    fondo_sel = st.radio("Fondo de la nube", ["Blanco", "Negro"], horizontal=True)
    fondo_color = "white" if fondo_sel == "Blanco" else "black"
    forma_sel = st.selectbox("Forma", ["Rectángulo", "Círculo"])
    max_words = st.slider("Máx. palabras visualizadas", 20, 200, 80)
    
    st.divider()
    st.markdown("### 🧹 Filtro de Texto")
    idioma = st.selectbox("Eliminar conectores en:", ["Español", "Inglés", "Ambos", "Ninguno"])
    min_longitud = st.slider("Longitud mínima de palabra", 2, 6, 3)
    palabras_extra = st.text_input("Excluir palabras específicas:", placeholder="ej: ejemplo, texto, pag")

# ─────────────────────────────────────────────
# CONTENIDO PRINCIPAL
# ─────────────────────────────────────────────
st.markdown("""
<div class="title-container">
    <h1>☁️ WordCloud Studio</h1>
    <p>Genera nubes de palabras profesionales de manera rápida y sencilla.</p>
</div>
""", unsafe_allow_html=True)

# Pestañas de entrada
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

# Botón de generación
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
