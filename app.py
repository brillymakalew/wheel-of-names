import streamlit as st
import plotly.graph_objects as go
import random
import time
import math

st.set_page_config(
    page_title="🎰 Neon Wheel of Names",
    layout="wide"
)

st.markdown(
    """
    <style>
    body {
        background-color: #050012;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================
# SESSION STATE
# =====================
if "names" not in st.session_state:
    st.session_state.names = []

if "angle" not in st.session_state:
    st.session_state.angle = 0

if "spinning" not in st.session_state:
    st.session_state.spinning = False

# =====================
# SIDEBAR INPUT
# =====================
st.sidebar.title("🎰 CONTROL PANEL")

name = st.sidebar.text_input("Tambah Nama")
if st.sidebar.button("ADD"):
    if name:
        st.session_state.names.append(name)

start = st.sidebar.button("▶ START")
stop = st.sidebar.button("■ STOP")

# =====================
# WHEEL FUNCTION
# =====================
def draw_wheel(rotation):
    labels = st.session_state.names
    values = [1] * len(labels)

    colors = [
        "#ff00ff", "#00ffff", "#00ff55",
        "#ffaa00", "#ff0055", "#7700ff"
    ]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.25,
                rotation=rotation,
                marker=dict(colors=colors * 10),
                textinfo="label",
                textfont=dict(size=18, color="white"),
            )
        ]
    )

    fig.update_layout(
        showlegend=False,
        paper_bgcolor="#050012",
        plot_bgcolor="#050012",
        height=700,
        annotations=[
            dict(
                x=0.5,
                y=1.08,
                text="⬇ POINTER ⬇",
                showarrow=False,
                font=dict(size=20, color="yellow")
            )
        ]
    )
    return fig

# =====================
# MAIN UI
# =====================
st.title("🎡 NEON WHEEL OF NAMES")

if len(st.session_state.names) < 2:
    st.warning("Masukkan minimal 2 nama")
    st.stop()

chart = st.empty()

# =====================
# START SPIN
# =====================
if start:
    st.session_state.spinning = True
    speed = random.uniform(25, 35)

    while speed > 0.5:
        st.session_state.angle += speed
        speed *= 0.97

        if speed < 3:
            st.session_state.angle += random.uniform(-1.5, 1.5)

        chart.plotly_chart(
            draw_wheel(st.session_state.angle),
            use_container_width=True
        )

        time.sleep(0.05)

    st.session_state.spinning = False

    # =====================
    # DRAMATIC 50–50
    # =====================
    step = 360 / len(st.session_state.names)
    idx = int((-st.session_state.angle % 360) / step)

    if random.choice([True, False]):
        idx = (idx + 1) % len(st.session_state.names)

    winner = st.session_state.names[idx]

    st.balloons()
    st.success(f"🎉 PEMENANG: **{winner}** 🎉")

# =====================
# STOP BUTTON (MANUAL)
# =====================
if not start:
    chart.plotly_chart(
        draw_wheel(st.session_state.angle),
        use_container_width=True
    )
