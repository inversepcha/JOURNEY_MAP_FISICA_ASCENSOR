import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import numpy as np

# =========================================================
# CONFIG PAGINA
# =========================================================

st.set_page_config(
    page_title="Ascensor Inteligente",
    page_icon="🏢",
    layout="wide"
)

# =========================================================
# ESTILOS
# =========================================================

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#000814,#001d3d);
    color:white;
}

section[data-testid="stSidebar"]{
    background:#001233;
    border-right:1px solid #16345f;
}

.block-container{
    padding-top:2rem;
    padding-bottom:1rem;
    max-width:1450px;
}

.stSlider > div > div > div > div{
    background:#ff4d5a;
}

div[data-testid="stRadio"] label{
    color:white !important;
    font-size:18px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("""
<h1 style="font-size:24px;">
⚙️ Variables físicas
</h1>
""", unsafe_allow_html=True)

masa_ascensor = st.sidebar.slider(
    "Masa ascensor (kg)",
    300,
    1000,
    500
)

masa_personas = st.sidebar.slider(
    "Masa personas (kg)",
    0,
    600,
    200
)

aceleracion = st.sidebar.slider(
    "Aceleración (m/s²)",
    0.5,
    5.0,
    1.5
)

velocidad = st.sidebar.slider(
    "Velocidad máxima (m/s)",
    1.0,
    10.0,
    3.0
)

eficiencia = st.sidebar.slider(
    "Eficiencia motor (%)",
    50,
    100,
    89
)

cantidad_pisos = st.sidebar.slider(
    "Cantidad pisos",
    2,
    20,
    8
)

altura_piso = st.sidebar.slider(
    "Altura por piso (m)",
    2,
    5,
    3
)

# =========================================================
# CALCULOS
# =========================================================

g = 9.81

masa_total = masa_ascensor + masa_personas

altura = (cantidad_pisos - 1) * altura_piso

fuerza = masa_total * (g + aceleracion)

energia_potencial = masa_total * g * altura

trabajo = fuerza * altura

tiempo = altura / velocidad if velocidad > 0 else 1

potencia = (trabajo / tiempo) / 1000

consumo = trabajo / (eficiencia / 100)

# =========================================================
# FUNCION TARJETAS
# =========================================================

def card_html(titulo, valor, unidad, color="white"):

    return f"""
    <div style="
        background:linear-gradient(180deg,#08142c,#07101f);
        border:1px solid #183a63;
        border-radius:18px;
        width:95px;
        height:90px;
        padding:6px;

        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;

        box-shadow:0 0 10px rgba(0,0,0,0.25);
    ">

        <div style="
            font-size:10px;
            color:#cbd5e1;
            font-weight:700;
            margin-bottom:5px;
            text-align:center;
        ">
            {titulo}
        </div>

        <div style="
            font-size:15px;
            font-weight:900;
            color:{color};
            line-height:1;
            text-align:center;
        ">
            {valor}
        </div>

        <div style="
            margin-top:5px;
            font-size:10px;
            color:#94a3b8;
            font-weight:600;
            text-align:center;
        ">
            {unidad}
        </div>

    </div>
    """

# =========================================================
# TITULO
# =========================================================

st.markdown("""
<div style="margin-top:60px;"></div>

<h1 style="
font-size:64px;
font-weight:900;
line-height:1.05;
margin-bottom:55px;
">
🏢 Ascensor Inteligente –<br>
Simulación Física
</h1>
""", unsafe_allow_html=True)

# =========================================================
# FORMULAS + TARJETAS
# =========================================================

left, right = st.columns([1.1,5])

with left:

    st.markdown("""
    <div style="
        padding-top:8px;
        padding-left:12px;
        font-size:18px;
        line-height:2.6;
        font-weight:800;
        white-space:nowrap;
    ">
        F − mg = ma<br>
        F = m(g + a)<br>
        v = at<br>
        Ep = mgh<br>
        P = W/t
    </div>
    """, unsafe_allow_html=True)

with right:

    cards_html = f"""
<html>

<body style="
    margin:0;
    background:transparent;
">

<div style="
    display:flex;
    gap:10px;
    align-items:flex-start;
    flex-wrap:wrap;
    margin-top:-6px;
">

    {card_html("⚖️ Masa", masa_total, "kg")}
    {card_html("🧲 Fuerza", int(fuerza), "N")}
    {card_html("🏢 Altura", f"{altura:.1f}", "m")}
    {card_html("⚡ Energía", int(energia_potencial), "J")}
    {card_html("🔋 Potencia", f"{potencia:.2f}", "kW")}
    {card_html("🔧 Trabajo", int(trabajo), "J")}
    {card_html("🪫 Consumo", int(consumo), "J")}
    {card_html("✅ Eficiencia", f"{eficiencia}%", "%", "#22c55e")}

</div>

</body>
</html>
"""

    components.html(cards_html, height=145)

# =========================================================
# ESPACIO
# =========================================================

st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)

# =========================================================
# PANEL Y SIMULACION
# =========================================================

col1, col2 = st.columns([1,2])

# =========================================================
# PANEL
# =========================================================

with col1:

    st.markdown("""
    <h2 style="
        font-size:34px;
        margin-bottom:25px;
    ">
    🎛️ Panel
    </h2>
    """, unsafe_allow_html=True)

    piso_actual = st.radio(
        "Seleccionar piso",
        list(range(cantidad_pisos,0,-1)),
        format_func=lambda x: f"Piso {x}"
    )

# =========================================================
# SIMULACION
# =========================================================

with col2:

    st.markdown("""
    <h2 style="
        font-size:34px;
        margin-bottom:25px;
    ">
    🏢 Simulación
    </h2>
    """, unsafe_allow_html=True)

    altura_total_px = 560

    piso_px = altura_total_px / cantidad_pisos

    # =====================================================
    # POSICION
    # =====================================================

    ascensor_y = (piso_actual - 1) * piso_px

    pisos_html = ""

    for i in range(cantidad_pisos):

        pisos_html += f"""
        <div style="
            position:absolute;
            bottom:{i*piso_px}px;
            width:100%;
            height:{piso_px}px;
            border-top:1px solid rgba(255,255,255,0.15);
        "></div>
        """

    simulacion_html = f"""

<style>

@keyframes glow {{

    from {{
        box-shadow:0 0 20px #22c55e;
    }}

    to {{
        box-shadow:
            0 0 35px #22c55e,
            0 0 60px #22c55e;
    }}

}}

</style>

<div style="
    width:340px;
    height:{altura_total_px}px;
    margin:auto;
    position:relative;
    border-radius:30px;
    border:6px solid #556987;
    background:#07152d;
    overflow:hidden;
    box-shadow:0 0 30px rgba(0,0,0,0.5);
">

    {pisos_html}

    <!-- DISPLAY -->

    <div style="
        position:absolute;
        top:18px;
        left:50%;
        transform:translateX(-50%);

        background:black;
        color:#22c55e;

        font-size:28px;
        font-weight:900;

        padding:6px 18px;

        border-radius:12px;

        border:2px solid #22c55e;

        box-shadow:0 0 15px #22c55e;
    ">
        {piso_actual}
    </div>

    <!-- TEXTO -->

    <div style="
        position:absolute;
        top:78px;
        width:100%;
        text-align:center;

        color:#cbd5e1;
        font-size:18px;
        font-weight:700;
    ">

        🟢 Piso {piso_actual}

    </div>

    <!-- ASCENSOR -->

    <div style="
        position:absolute;

        left:20px;
        bottom:{ascensor_y + 10}px;

        width:300px;
        height:{piso_px - 20}px;

        background:#16a34a;

        animation: glow 2s infinite alternate;

        border-radius:18px;

        transition:
            all 2.5s cubic-bezier(0.22, 1, 0.36, 1);

        will-change: bottom;

        box-shadow:0 0 30px #22c55e;

        overflow:hidden;

        border:2px solid rgba(255,255,255,0.15);
    ">

        <!-- PUERTA IZQUIERDA -->

        <div style="
            position:absolute;
            left:0;
            top:0;

            width:50%;
            height:100%;

            background:#16a34a;

            border-right:2px solid #052e16;
        "></div>

        <!-- PUERTA DERECHA -->

        <div style="
            position:absolute;
            right:0;
            top:0;

            width:50%;
            height:100%;

            background:#16a34a;
        "></div>

    </div>

</div>
"""

    components.html(simulacion_html, height=620)

# =========================================================
# GRAFICAS FISICAS
# =========================================================

st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

st.markdown("""
<h2 style="
font-size:42px;
font-weight:900;
margin-bottom:25px;
">
📊 Análisis Físico
</h2>
""", unsafe_allow_html=True)

pisos = np.arange(1, cantidad_pisos + 1)

alturas = pisos * altura_piso

energias = masa_total * g * alturas

velocidades = np.linspace(0, velocidad, cantidad_pisos)

g1, g2 = st.columns(2)

with g1:

    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
        x=alturas,
        y=energias,
        mode='lines+markers',
        name='Energía potencial'
    ))

    fig1.update_layout(
        title="Energía Potencial vs Altura",
        xaxis_title="Altura (m)",
        yaxis_title="Energía (J)",
        height=450,
        paper_bgcolor="#07152d",
        plot_bgcolor="#07152d",
        font=dict(color="white")
    )

    st.plotly_chart(fig1, use_container_width=True)

with g2:

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=pisos,
        y=velocidades,
        mode='lines+markers',
        name='Velocidad'
    ))

    fig2.update_layout(
        title="Velocidad del Ascensor",
        xaxis_title="Pisos",
        yaxis_title="Velocidad (m/s)",
        height=450,
        paper_bgcolor="#07152d",
        plot_bgcolor="#07152d",
        font=dict(color="white")
    )

    st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# ANALISIS TEMPORAL
# =========================================================

st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)

st.markdown("""
<h2 style="
font-size:42px;
font-weight:900;
margin-bottom:25px;
">
⚙️ Fenómenos físicos del sistema
</h2>
""", unsafe_allow_html=True)

tiempo_total = altura / velocidad

t = np.linspace(0, tiempo_total, 100)

altura_t = 0.5 * aceleracion * (t**2)
altura_t = np.clip(altura_t, 0, altura)

velocidad_t = aceleracion * t
velocidad_t = np.clip(velocidad_t, 0, velocidad)

aceleracion_t = np.full_like(t, aceleracion)

energia_t = masa_total * g * altura_t

potencia_t = fuerza * velocidad_t / 1000

trabajo_t = fuerza * altura_t

consumo_t = trabajo_t / (eficiencia / 100)

g3, g4 = st.columns(2)

with g3:

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t,
        y=altura_t,
        mode='lines',
        name='Altura'
    ))

    fig.update_layout(
        title="Altura vs Tiempo",
        xaxis_title="Tiempo (s)",
        yaxis_title="Altura (m)",
        height=420,
        paper_bgcolor="#07152d",
        plot_bgcolor="#07152d",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

with g4:

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t,
        y=velocidad_t,
        mode='lines',
        name='Velocidad'
    ))

    fig.update_layout(
        title="Velocidad vs Tiempo",
        xaxis_title="Tiempo (s)",
        yaxis_title="Velocidad (m/s)",
        height=420,
        paper_bgcolor="#07152d",
        plot_bgcolor="#07152d",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

g5, g6 = st.columns(2)

with g5:

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t,
        y=aceleracion_t,
        mode='lines',
        name='Aceleración'
    ))

    fig.update_layout(
        title="Aceleración vs Tiempo",
        xaxis_title="Tiempo (s)",
        yaxis_title="Aceleración (m/s²)",
        height=420,
        paper_bgcolor="#07152d",
        plot_bgcolor="#07152d",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

with g6:

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t,
        y=energia_t,
        mode='lines',
        name='Energía'
    ))

    fig.update_layout(
        title="Energía potencial vs Tiempo",
        xaxis_title="Tiempo (s)",
        yaxis_title="Energía (J)",
        height=420,
        paper_bgcolor="#07152d",
        plot_bgcolor="#07152d",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)