import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="Browniano - ITBA", layout="wide")

if 'caminos' not in st.session_state:
    st.session_state.caminos = []

# --- SIDEBAR ---
with st.sidebar:
    try:
        # Cargamos el logo institucional
        logo = Image.open('logo.png')
        st.image(logo, use_container_width=True)
    except:
        st.write("ITBA - Future Day")
    
    st.header("Configuración")
    n_pasos = st.slider("Pasos por paseo (N):", 100, 10000, 1000, step=100)
    
    if st.button("🚶‍♂️ Simular 10 paseos"):
        for _ in range(10):
            pasos = np.random.choice([-1, 1], size=n_pasos)
            st.session_state.caminos.append(np.cumsum(pasos))
            
    if st.button("🗑️ Reiniciar"):
        st.session_state.caminos = []
        st.rerun()

# --- CUERPO PRINCIPAL ---
# Título actualizado según tu indicación
st.title("🥴 Del Paseo del Borracho al Movimiento Browniano")
st.write("---")

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
    st.pyplot(fig_tr)
    
    # Aclaración sobre el proceso
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
        st.pyplot(fig_hist)
        
        # Aclaración sobre el resultado final y el TCL
        st.write("### Posición Final y Teorema Central del Límite")
        st.write(f"""
        En este gráfico observamos la **posición final** de todas las trayectorias simuladas. 
        Como predice el **Teorema Central del Límite**, la distribución de estos puntos tiende a formar 
        una **Campana de Gauss**, demostrando que el desorden individual genera un orden estadístico predecible.
        """)
        
        st.info("💡 Esta idea aplica a la **física estadística**. Para profundizar en la evidencia experimental de los átomos, sugerimos buscar el fenómeno del 'Movimiento Browniano'.")
    else:
        st.warning("Simula algunos paseos más para generar la estadística de las posiciones finales.")