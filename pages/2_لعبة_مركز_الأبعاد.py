import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="🎮 لعبة اسحب الكتل وحسب G", layout="wide")
st.title("🎮 اسحب الكتل على الرسم واظهر مركز الأبعاد")

st.markdown("""
<div dir="rtl" style="text-align: right;">
✅ اسحب النقاط داخل الرسم (Canvas)، ثم اضغط على: احسب G.
</div>
""", unsafe_allow_html=True)

# إعداد النقاط الافتراضية
n = st.slider("عدد الكتل", 2, 6, 3)
positions = np.column_stack((np.linspace(50, 350, n), np.linspace(50, 350, n)))  # canvas pixel coords

# canvas setup
canvas_result = st_canvas(
    fill_color="rgba(255, 0, 0, 0.1)",
    stroke_width=3,
    stroke_color="#000",
    background_color="#eee",
    width=400,
    height=400,
    initial_drawing={
        "version": "4.4.0",
        "objects": [{
            "type": "circle",
            "left": int(positions[i,0]),
            "top": int(positions[i,1]),
            "radius": 10,
            "fill": "blue"
        } for i in range(n)]
    },
    drawing_mode="point",
    key="canvas"
)

# قراءة المواضع بعد السحب
if canvas_result.json_data:
    objs = canvas_result.json_data["objects"]
    positions = np.array([[obj["left"], obj["top"]] for obj in objs])

# إدخال الكتل
masses = [st.number_input(f"⚖️ كتلة P{i+1}", min_value=0.1, value=1.0, step=0.1, key=f"m_{i}") for i in range(n)]
masses = np.array(masses)

def barycentre(pts, m):
    pts_norm = pts / 100  # نحول من بيكسل إلى نظام إحداثيات عادي
    return np.sum(pts_norm.T * m, axis=1) / np.sum(m)

# حساب مركز الأبعاد ورسمه
if st.button("🎯 احسب G"):
    G = barycentre(positions, masses)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(positions[:,0], positions[:,1], s=100, c="blue")
    for i,(x,y) in enumerate(positions):
        ax.text(x+5, y+5, f"P{i+1}(m={masses[i]})", fontsize=9)

    # رسم مركز الأبعاد
    Gpix = G * 100
    ax.scatter(Gpix[0], Gpix[1], c="red", s=150, marker="X")
    ax.text(Gpix[0]+5, Gpix[1], "G", color="red", fontsize=12)

    ax.set_title("موقع G حسب سحب النقاط")
    ax.set_xlim(0,400); ax.set_ylim(0,400)
    ax.set_aspect('equal'); ax.invert_yaxis()
    ax.grid(True)
    st.pyplot(fig)

    st.success(f"📍 G ≈ ({round(G[0],2)}, {round(G[1],2)}) [في نظام الإحداثيات]")
