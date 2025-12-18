import streamlit as st
import plotly.graph_objects as go
import random
import math

st.set_page_config(page_title="Smooth Wheel of Names", layout="wide")

# ======================
# SESSION STATE
# ======================
if "names" not in st.session_state:
    st.session_state.names = []

if "colors" not in st.session_state:
    st.session_state.colors = []

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
# DRAW BASE WHEEL
# ======================
def base_wheel(rotation=0):
    return go.Figure(
        data=[
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
        ],
        layout=go.Layout(
            showlegend=False,
            height=650,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=40, b=40),
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
    )

# ======================
# MAIN
# ======================
st.title("🎡 Smooth Wheel of Names")

if len(st.session_state.names) < 2:
    st.info("Masukkan minimal 2 nama")
    st.stop()

fig = base_wheel()

# ======================
# BUILD ANIMATION FRAMES
# ======================
if start:
    frames = []
    angle = 0
    speed = random.uniform(35, 45)

    while speed > 0.6:
        angle += speed
        speed *= 0.97

        if speed < 3:
            angle += random.uniform(-0.6, 0.6)

        frames.append(
            go.Frame(
                data=[go.Pie(rotation=angle)]
            )
        )

    fig.frames = frames

    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                buttons=[
                    dict(
                        label="Spin",
                        method="animate",
                        args=[
                            None,
                            dict(
                                frame=dict(duration=30, redraw=False),
                                transition=dict(duration=0),
                                fromcurrent=True,
                            ),
                        ],
                    )
                ],
            )
        ]
    )

    st.plotly_chart(fig, use_container_width=True)

    # ======================
    # FINAL RESULT
    # ======================
    step = 360 / len(st.session_state.names)
    idx = int((-angle % 360) / step)
    if random.choice([True, False]):
        idx = (idx + 1) % len(st.session_state.names)

    st.balloons()
    st.success(f"🏆 PEMENANG: **{st.session_state.names[idx]}**")

else:
    st.plotly_chart(fig, use_container_width=True)
