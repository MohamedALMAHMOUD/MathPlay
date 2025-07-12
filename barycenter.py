import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="مركز الأبعاد المتجانس", layout="centered")

st.title("📌 محاكي لحساب مركز الأبعاد المتجانس")
st.markdown("تغيير القيم سيغير مكان مركز الأبعاد المتجانس.")
n = st.slider("عدد النقاط", 2, 6, 3)

positions = []
masses = []

st.markdown("### 📥 أدخل الإحداثيات والكتل")
for i in range(n):
    col1, col2, col3 = st.columns(3)
    with col1:
        x = st.number_input(f"x{i+1}", value=float(i+1), key=f"x_{i}")
    with col2:
        y = st.number_input(f"y{i+1}", value=float(i+2), key=f"y_{i}")
    with col3:
        m = st.number_input(f"m{i+1}", min_value=0.1, value=1.0, step=0.1, key=f"m_{i}")
    positions.append([x, y])
    masses.append(m)

positions = np.array(positions)
masses = np.array(masses)

def barycentre(pts, m):
    total_mass = np.sum(m)
    return np.sum(pts.T * m, axis=1) / total_mass

G = barycentre(positions, masses)

# === عرض المعادلات ===
st.markdown("### 🧮 معادلة مركز الأبعاد")

x_terms = [f"{round(masses[i], 2)} \\cdot {round(positions[i][0], 2)}" for i in range(n)]
y_terms = [f"{round(masses[i], 2)} \\cdot {round(positions[i][1], 2)}" for i in range(n)]

x_numerateur = " + ".join(x_terms)
y_numerateur = " + ".join(y_terms)
denominateur = " + ".join([f"{round(m, 2)}" for m in masses])

x_val = sum(masses[i] * positions[i][0] for i in range(n))
y_val = sum(masses[i] * positions[i][1] for i in range(n))
somme_masses = np.sum(masses)

xG = round(x_val / somme_masses, 3)
yG = round(y_val / somme_masses, 3)

st.latex(rf"x_G = \frac{{{x_numerateur}}}{{{denominateur}}} = \frac{{{round(x_val, 2)}}}{{{round(somme_masses, 2)}}} = {xG}")
st.latex(rf"y_G = \frac{{{y_numerateur}}}{{{denominateur}}} = \frac{{{round(y_val, 2)}}}{{{round(somme_masses, 2)}}} = {yG}")

# === رسم بياني ===
st.markdown("### 🖼️ التمثيل البياني")
fig, ax = plt.subplots(figsize=(6, 6))
ax.axhline(0, color='lightgray', linestyle='--')
ax.axvline(0, color='lightgray', linestyle='--')

for i, (x, y) in enumerate(positions):
    ax.scatter(x, y, s=100)
    ax.text(x + 0.1, y + 0.1, f"P{i+1} (m={round(masses[i],1)})", fontsize=10)

ax.scatter(G[0], G[1], color='red', s=150, marker='X')
ax.text(G[0] + 0.1, G[1] + 0.1, "G", color='red', fontsize=12)

ax.set_title("")
ax.set_aspect('equal')
ax.grid(True)
st.pyplot(fig)