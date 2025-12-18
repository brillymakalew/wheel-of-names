import streamlit as st
import plotly.graph_objects as go
import random
import time

st.set_page_config(page_title="Wheel of Names", layout="wide")

# ======================
# SESSION STATE
# ======================
if "names" not in st.session_state:
    st.session_state.names = []

if "colors" not in st.session_state:
    st.session_state.colors = []

if "angle" not in st.session_state:
    st.session_state.angle = 0.0

# ======================
# SIDEBAR
# ======================
st.sidebar.title("🎛️ Control Panel")

name = st.sidebar.text_input("Tambah Nama")
if st.sidebar.button("➕ Tambah"):
    if name:
        st.session_state.names.append(name)
        st.session_state.colors.append(
            random.choice([
                "#ff595e", "#ffca3a", "#8ac926",
                "#1982c4", "#6a4c93"
            ])
        )

if st.session_state.names:
    st.sidebar.markdown("### 📋 Daftar Nama")
    for i, n in enumerate(st.session_state.names, 1):
        st.sidebar.write(f"{i}. {n}")

start = st.sidebar.button("🎡 START")

# ======================
# DRAW WHEEL
# ======================
def draw_wheel(rotation):
    fig = go.Figure(
        go.Pie(
            labels=st.session_state.names,
            values=[1] * len(st.session_state.names),
            rotation=rotation,
            direction="clockwise",
            sort=False,
            hole=0.35,
            marker=dict(colors=st.session_state.colors),
            textinfo="label",
            textfont=dict(size=18),
        )
    )

    fig.update_layout(
        showlegend=False,
        height=650,
        margin=dict(t=40, b=40, l=40, r=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=[
            dict(
                x=0.5,
                y=1.12,
                text="▼",
                showarrow=False,
                font=dict(size=40, color="red")
            )
        ]
    )
    return fig

# ======================
# MAIN
# ======================
st.title("🎡 Wheel of Names")

if len(st.session_state.names) < 2:
    st.info("Masukkan minimal 2 nama")
    st.stop()

wheel = st.empty()
wheel.plotly_chart(draw_wheel(st.session_state.angle), use_container_width=True)

# ======================
# SPIN LOGIC
# ======================
if start:
    speed = random.uniform(40, 50)

    while speed > 0.8:
        st.session_state.angle += speed
        speed *= 0.965

        # subtle jitter near end
        if speed < 4:
            st.session_state.angle += random.uniform(-0.8, 0.8)

        wheel.plotly_chart(
            draw_wheel(st.session_state.angle),
            use_container_width=True
        )
        time.sleep(0.03)

    # ======================
    # FINAL PICK (50/50)
    # ======================
    step = 360 / len(st.session_state.names)
    idx = int((-st.session_state.angle % 360) / step)

    if random.choice([True, False]):
        idx = (idx + 1) % len(st.session_state.names)

    winner = st.session_state.names[idx]
    st.balloons()
    st.success(f"🏆 PEMENANG: **{winner}**")
