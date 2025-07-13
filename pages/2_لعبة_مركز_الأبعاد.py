import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="🎮 لعبة مركز الأبعاد", layout="wide")
st.title("🎮 اسحب الكتل وحدد مركز الجاذبية!")

n = st.slider("🔢 عدد الكتل", 2, 6, 3)

# --- Initialisation des positions et masses ---
positions = np.column_stack((np.linspace(50, 350, n), np.linspace(100, 300, n)))
masses = np.array([1.0] * n)

with st.expander("⚖️ عدل كتل النقاط"):
    for i in range(n):
        masses[i] = st.slider(f"كتلة P{i+1}", 0.1, 10.0, 1.0, step=0.1, key=f"mass_{i}")

# --- Canvas interactif ---
canvas_result = st_canvas(
    fill_color="rgba(0, 100, 255, 0.4)",
    stroke_width=3,
    stroke_color="#000",
    background_color="#fafafa",
    width=400,
    height=400,
    initial_drawing={
        "version": "4.4.0",
        "objects": [
            {
                "type": "circle",
                "left": float(positions[i][0]),
                "top": float(positions[i][1]),
                "radius": 10,
                "fill": "#0066FF",
            }
            for i in range(n)
        ]
    },
    drawing_mode="transform",
    key="canvas",
    update_streamlit=True
)

if canvas_result.json_data and "objects" in canvas_result.json_data:
    objs = canvas_result.json_data["objects"]
    if len(objs) == n:
        positions = np.array([[obj["left"], obj["top"]] for obj in objs])

# --- Bouton pour deviner G ---
st.markdown("### ❓ أين تعتقد أن مركز الجاذبية؟")
guess_col, button_col = st.columns([3, 1])
with guess_col:
    gx = st.slider("x", 0, 400, 200)
    gy = st.slider("y", 0, 400, 200)

if button_col.button("🎯 تحقق"):
    def barycentre(pts, m):
        pts_norm = pts / 100
        return np.sum(pts_norm.T * m, axis=1) / np.sum(m)

    G = barycentre(positions, masses)
    Gpix = G * 100
    distance = np.linalg.norm(Gpix - [gx, gy])
    score = max(0, 100 - distance)

    st.success(f"📍 G الحقيقي: ({round(Gpix[0],1)}, {round(Gpix[1],1)})")
    st.info(f"📏 المسافة عن تخمينك: {int(distance)}px")
    st.metric("🎮 النتيجة", f"{int(score)} / 100")

    # --- Affichage graphique ---
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 400)
    ax.set_ylim(0, 400)
    ax.invert_yaxis()
    ax.grid(True)
    ax.set_title("🎯 موقع النقاط و G")

    # points
    for i, (x, y) in enumerate(positions):
        ax.scatter(x, y, s=100)
        ax.text(x + 5, y, f"P{i+1} (m={masses[i]})", fontsize=8)

    # barycentre réel
    ax.scatter(Gpix[0], Gpix[1], color="red", s=150, marker="X", label="G réel")

    # guess
    ax.scatter(gx, gy, color="green", s=100, marker="o", label="تخمينك")

    ax.legend()
    st.pyplot(fig)
