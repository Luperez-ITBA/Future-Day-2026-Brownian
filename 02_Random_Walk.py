import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Configuración de la página con barra lateral colapsada por defecto
st.set_page_config(page_title="Estadística y Browniano - ITBA", layout="wide", initial_sidebar_state="collapsed")

if 'caminos' not in st.session_state:
    st.session_state.caminos = []

# --- CABECERA Y CONTROLES (Reemplaza a la barra lateral) ---
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

# Controles distribuidos en el cuerpo principal
col_slider, col_spacer = st.columns([2, 2])
with col_slider:
    n_pasos = st.slider("Pasos por paseo (N):", 100, 10000, 1000, step=100)

col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn1:
    if st.button("🚶‍♂️ Simular 10 paseos", use_container_width=True):
        for _ in range(10):
            pasos = np.random.choice([-1, 1], size=n_pasos)
            st.session_state.caminos.append(np.cumsum(pasos))
        st.rerun()

with col_btn2:
    if st.button("🚀 Simular 1000 paseos", use_container_width=True):
        for _ in range(1000):
            pasos = np.random.choice([-1, 1], size=n_pasos)
            st.session_state.caminos.append(np.cumsum(pasos))
        st.rerun()

with col_btn3:
    if st.button("🗑️ Reiniciar", use_container_width=True):
        st.session_state.caminos = []
        st.rerun()

st.write("---")

# --- CUERPO PRINCIPAL ---
tab1, tab2 = st.tabs(["📈 Trayectorias", "📊 Análisis Estadístico"])

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
