import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time # Added this import

def vertical_motion(t, g, v0, h0):
    """Calcula la posición vertical de la pelota."""
    return 0.5 * g * t**2 + v0 * t + h0

st.set_page_config(page_title="Simulación de Movimiento Vertical", layout="centered")
st.title("Simulación de Movimiento Vertical")

st.sidebar.header("Parámetros de la Simulación")
g = st.sidebar.slider("Gravedad (g) (m/s^2)", -20.0, 20.0, -9.81, 0.1)
v0 = st.sidebar.slider("Velocidad Inicial (v0) (m/s)", -50.0, 50.0, 0.0, 0.1)
h0 = st.sidebar.slider("Altura Inicial (h0) (m)", 1.0, 100.0, 50.0, 0.5)

st.write("### Resultados de la Simulación")

fig, ax = plt.subplots(figsize=(6, 8))
ax.set_xlim(-1, 1)
ax.set_ylim(0, h0 * 1.2)
ax.set_xlabel("Posición X (Arbitraria)")
ax.set_ylabel("Altura (y) (m)")
ax.set_title("Animación de la Pelota")
ax.grid(True)

ball, = ax.plot(0, h0, 'o', markersize=20, color='red')
t_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=12)

# La sección de FuncAnimation no es necesaria y causaba el error.
# La animación en Streamlit se maneja con el bucle while True y st.pyplot().

if st.button("Iniciar Simulación"):
    st.session_state.start_simulation = True

if st.button("Reiniciar Simulación"):
    st.session_state.start_simulation = False
    st.experimental_rerun()

if 'start_simulation' not in st.session_state:
    st.session_state.start_simulation = False

if st.session_state.start_simulation:
    current_time = 0.0
    dt = 0.05
    max_y = h0 * 1.2 # Ajustar el límite y para que la pelota no se salga de la vista
    if g > 0 and v0 >= 0: # Si la gravedad es positiva y la velocidad inicial es positiva, la pelota subirá
        # Encontrar el tiempo en el que la velocidad es 0 (punto más alto)
        t_peak = -v0 / g if g != 0 else 0
        y_peak = vertical_motion(t_peak, g, v0, h0)
        max_y = max(max_y, y_peak * 1.2)

    ax.set_ylim(0, max_y)

    status_placeholder = st.empty()
    plot_placeholder = st.empty()

    while True:
        y = vertical_motion(current_time, g, v0, h0)

        if y <= 0 and current_time > 0.01: # Asegurarse de que no sea el estado inicial si h0=0
            y = 0
            ball.set_ydata([y]) # `set_ydata` espera una secuencia, incluso para un solo punto
            t_text.set_text(f'Tiempo: {current_time:.2f} s\nAltura: {y:.2f} m\n¡Toca el suelo!')
            with plot_placeholder.container():
                st.pyplot(fig)
            status_placeholder.info(f"Simulación Terminada: La pelota tocó el suelo en {current_time:.2f} segundos.")
            break

        ball.set_ydata([y]) # `set_ydata` espera una secuencia, incluso para un solo punto
        t_text.set_text(f'Tiempo: {current_time:.2f} s\nAltura: {y:.2f} m')

        with plot_placeholder.container():
            st.pyplot(fig)
        status_placeholder.text(f"Tiempo: {current_time:.2f} s, Altura: {y:.2f} m")

        time.sleep(dt) # Added this line

        current_time += dt
        if current_time > 100: # Protección para evitar bucles infinitos
            status_placeholder.error("Simulación detenida: Tiempo máximo alcanzado (100s).")
            break

    st.session_state.start_simulation = False # Reiniciar el estado para el siguiente click
