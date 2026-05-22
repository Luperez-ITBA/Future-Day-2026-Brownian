import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Configuración de la página con la barra lateral nativa colapsada
st.set_page_config(page_title="Estadística y Browniano - ITBA", layout="wide", initial_sidebar_state="collapsed")

if 'caminos' not in st.session_state:
    st.session_state.caminos = []

# --- ESTILOS CSS RESPONSIVOS Y PERSONALIZADOS ---
st.markdown("""
    <style>
    /* Recuadro celeste personalizado */
    .recuadro-celeste {
        font-size: 20px; 
        line-height: 1.6; 
        background-color: #e0f2fe; /* Fondo celeste claro */
        padding: 25px; 
        border-radius: 12px; 
        border-left: 8px solid #0284c7; /* Borde azul fuerte */
        color: #0f172a;
        text-align: center;
        margin-bottom: 10px;
    }
    
    /* Recuadros de la pestaña de aplicaciones */
    .recuadro-aplicacion {
        background-color: #e2e8f0; 
        padding: 20px; 
        border-radius: 12px; 
        border-left: 6px solid #0074D9;
        font-size: 18px;
        line-height: 1.6;
        color: #1e293b;
    }
    
    /* AGRANDAR PESTAÑAS (Para notar más la interactividad) */
    button[data-baseweb="tab"] {
        padding: 10px 20px !important;
    }
    button[data-baseweb="tab"] p {
        font-size: 20px !important;
        font-weight: 700 !important;
    }
    
    /* Adaptación automática para celulares */
    @media (max-width: 768px) {
        .recuadro-celeste { 
            font-size: 16px !important; 
            padding: 15px !important; 
        }
        .recuadro-aplicacion {
            font-size: 15px !important;
            padding: 15px !important;
        }
        button[data-baseweb="tab"] p {
            font-size: 15px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA (Logo y Título) ---
col_logo, col_titulo = st.columns([1, 4])

with col_logo:
    try:
        logo = Image.open('logo_itba.png')
        st.image(logo, use_container_width=True)
    except:
        st.write("### ITBA")

with col_titulo:
    st.title("🥴 Del Paseo del Borracho al Movimiento Browniano")

st.write("---")

# --- INTRODUCCIÓN HISTÓRICA ---
c_einstein, c_texto, c_wiener = st.columns([1.5, 6, 1.5])

with c_einstein:
    try:
        st.image('einstein.png', use_container_width=True, caption="Albert Einstein")
    except:
        pass

with c_texto:
    st.markdown("""
    <div class="recuadro-celeste">
        La <b><i>caminata al azar</i></b> suele representarse como la posición de un borracho que da pasos adelante o atrás con igual probabilidad. Tan sencilla idea da lugar a un fenómeno realmente fascinante conocido como <b><i>movimiento Browniano</i></b> que ocupó a mentes tan brillantes como Albert Einstein y Norbert Wiener (creador de la cibernética).
        <br><br>
        El <b><i>proceso de Wiener</i></b> o movimiento Browniano muestra cómo la repetición de un experimento totalmente azaroso va <b><i>tomando forma</i></b> en su aspecto <b><i>asintótico</i></b>, dando lugar a un <b><i>proceso gaussiano</i></b> que sigue leyes estadísticas universales.
    </div>
    """, unsafe_allow_html=True)

with c_wiener:
    try:
        st.image('norbert.png', use_container_width=True, caption="Norbert Wiener")
    except:
        pass

st.write("---")

# --- DISPOSICIÓN EN COLUMNAS FIJAS ---
col_control, col_display = st.columns([1, 3.2], gap="large")

# --- COLUMNA IZQUIERDA: CONTROLES FIX ---
with col_control:
    st.header("Configuración")
    n_pasos = st.slider("Pasos por paseo (N):", 100, 10000, 1000, step=100)
    
    st.write("") 
    
    if st.button("🚶‍♂️ Simular 10 paseos", use_container_width=True):
        for _ in range(10):
            pasos = np.random.choice([-1, 1], size=n_pasos)
            st.session_state.caminos.append(np.cumsum(pasos))
        st.rerun()

    if st.button("🚀 Simular 1000 paseos", use_container_width=True):
        for _ in range(1000):
            pasos = np.random.choice([-1, 1], size=n_pasos)
            st.session_state.caminos.append(np.cumsum(pasos))
        st.rerun()

    if st.button("🗑️ Reiniciar", use_container_width=True):
        st.session_state.caminos = []
        st.rerun()

# --- COLUMNA DERECHA: VISUALIZACIÓN Y PESTAÑAS ---
with col_display:
    tab1, tab2, tab3 = st.tabs(["📈 Trayectorias", "📊 Análisis Estadístico", "🚀 Aplicaciones"])

    with tab1:
        fig_tr, ax_tr = plt.subplots(figsize=(10, 5))
        for i, y in enumerate(st.session_state.caminos):
            alpha = 1.0 if i == len(st.session_state.caminos)-1 else 0.2
            color = "#1f77b4" if i == len(st.session_state.caminos)-1 else "gray"
            ax_tr.plot(y, color=color, alpha=alpha)
        
        ax_tr.set_title("Evolución Temporal")
        ax_tr.set_xlabel("Tiempo (pasos)")
        ax_tr.set_ylabel("Posición")
        st.pyplot(fig_tr, use_container_width=True)
        
        st.write("Estamos viendo una **distribución de trayectorias** que responden al concepto de **movimiento browniano**.")

    with tab2:
        if len(st.session_state.caminos) > 5:
            finales = [c[-1] for c in st.session_state.caminos]
            
            fig_hist, ax_hist = plt.subplots(figsize=(10, 5))
            ax_hist.hist(finales, bins=20, color='#2ecc71', edgecolor='white', density=True, alpha=0.7)
            
            # Curva de Gauss teórica
            x_teorico = np.linspace(min(finales)-10, max(finales)+10, 100)
            sigma = np.sqrt(n_pasos)
            gauss = (1/(sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * (x_teorico/sigma)**2)
            ax_hist.plot(x_teorico, gauss, color='red', lw=2, label="Campana de Gauss")
            
            ax_hist.set_title("Distribución de Posiciones Finales")
            ax_hist.legend()
            st.pyplot(fig_hist, use_container_width=True)
            
            st.write("### Posición Final y Teorema Central del Límite")
            st.write(f"""
            En este gráfico observamos la **posición final** de todas las trayectorias simuladas. 
            Como predice el **Teorema Central del Límite**, la distribución de estos puntos tiende a formar 
            una **Campana de Gauss**, demostrando que el desorden individual genera un orden estadístico predecible.
            """)
            
            st.info("""
            💡 **Dato Histórico:** Esta idea aplica fundamentalmente a la **física estadística**. 
            En 1905, **Albert Einstein** utilizó esta misma matemática para explicar el movimiento de partículas 
            suspendidas en un líquido, proporcionando así la primera evidencia física indiscutible de la 
            existencia de los átomos.
            """)
        else:
            st.warning("Simula algunos paseos más para generar la estadística de las posiciones finales.")

    with tab3:
        st.subheader("💡 El Impacto en la Ciencia y las Finanzas")
        
        # Recuadro 1: Einstein
        col_img1, col_txt1 = st.columns([1, 4])
        with col_img1:
            try:
                st.image('einstein.png', use_container_width=True)
            except:
                st.write("🖼️ *einstein.png*")
        with col_txt1:
            st.markdown("""
            <div class="recuadro-aplicacion">
                El análisis del movimiento Browniano permitió a Einstein dar una prueba de la existencia de los átomos y se convirtió en el modelo matemático general para los <b><i>procesos de difusión</i></b> relacionados con fenómenos de transporte.
            </div>
            """, unsafe_allow_html=True)
            
        st.write("<br>", unsafe_allow_html=True)
        
        # Recuadro 2: Black-Scholes
        col_img2, col_txt2 = st.columns([1, 4])
        with col_img2:
            try:
                st.image('blackscholes.png', use_container_width=True)
            except:
                st.write("🖼️ *blackscholes.png*")
        with col_txt2:
            st.markdown("""
            <div class="recuadro-aplicacion">
                En <b><i>finanzas cuantitativas</i></b> el movimiento Browniano <b><i>geométrico</i></b> es la base de los modelos estocásticos de valuación de activos, como acciones y opciones, en particular del famoso <b><i>Modelo de Black-Scholes</i></b>.
            </div>
            """, unsafe_allow_html=True)
