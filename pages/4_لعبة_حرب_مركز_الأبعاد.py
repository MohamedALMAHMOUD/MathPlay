import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(page_title="🔥 حرب مركز الكتلة", layout="centered")
st.title("🎮 حرب مركز الكتلة بين لاعبين")
st.markdown("جرب أن تصيب مركز الكتلة قبل خصمك!")

# 🧠 Session state
if "round" not in st.session_state:
    st.session_state.round = 1
    st.session_state.p1_score = 0
    st.session_state.p2_score = 0
    st.session_state.niveau = 1

# 👑 اختيار المستوى
niveau = st.slider("اختر مستوى اللعبة", 1, 5, st.session_state.niveau)
st.session_state.niveau = niveau
n_points = niveau + 1  # عدد النقاط حسب المستوى

st.markdown(f"### 🌀 الجولة {st.session_state.round}/10 — مستوى {niveau} ({n_points} نقاط)")

# 🟢 توليد بيانات عشوائية نسبية
positions = np.random.randint(-10, 11, (n_points, 2))  # [-10, 10]
masses = np.round(np.random.uniform(1.0, 5.0, n_points), 1)

def barycentre(pts, m):
    total_mass = np.sum(m)
    return np.sum(pts.T * m, axis=1) / total_mass

G = barycentre(positions, masses)

# 🧭 عرض النقاط في الرسم
fig, ax = plt.subplots()
colors = ['blue', 'green', 'orange', 'purple', 'cyan']
for i, (x, y) in enumerate(positions):
    ax.scatter(x, y, s=120, color=colors[i % len(colors)])
    ax.text(x + 0.4, y + 0.4, f"P{i+1}\nm={masses[i]}", fontsize=9)
ax.axhline(0, color='gray', linestyle='--')
ax.axvline(0, color='gray', linestyle='--')
ax.set_xlim(-15, 15)
ax.set_ylim(-15, 15)
ax.set_title("📌 تموضع النقاط")
ax.grid(True)
ax.set_aspect('equal')
st.pyplot(fig)

# 🔫 إدخال اللاعبين
col1, col2 = st.columns(2)
with col1:
    st.subheader("👤 اللاعب 1")
    p1_x = st.number_input("x₁", step=0.5, format="%.1f", key="p1x")
    p1_y = st.number_input("y₁", step=0.5, format="%.1f", key="p1y")
with col2:
    st.subheader("👤 اللاعب 2")
    p2_x = st.number_input("x₂", step=0.5, format="%.1f", key="p2x")
    p2_y = st.number_input("y₂", step=0.5, format="%.1f", key="p2y")

# 🧠 التحقق وإطلاق النار
if st.button("🚀 أطلق!"):
    d1 = np.linalg.norm(np.array([p1_x, p1_y]) - G)
    d2 = np.linalg.norm(np.array([p2_x, p2_y]) - G)
    seuil = 1.5
    gagnant = "❌ لم يصب أي لاعب المركز بدقة كافية"

    if d1 < seuil and d1 < d2:
        st.session_state.p1_score += 1
        gagnant = "🏆 اللاعب 1 أصاب المركز!"
    elif d2 < seuil and d2 < d1:
        st.session_state.p2_score += 1
        gagnant = "🏆 اللاعب 2 أصاب المركز!"

    st.success(gagnant)
    st.markdown(f"📍 مركز الكتلة الحقيقي: **x = {round(G[0], 2)}, y = {round(G[1], 2)}**")
    st.markdown(f"🎯 مسافة اللاعب 1: `{round(d1, 2)}` | مسافة اللاعب 2: `{round(d2, 2)}`")

    # ➕ التقدم للجولة التالية
    if st.session_state.round < 10:
        st.session_state.round += 1
    else:
        st.balloons()
        st.markdown("## 🎉 انتهت الجولات!")
        st.markdown(f"👤 اللاعب 1: `{st.session_state.p1_score}` نقطة")
        st.markdown(f"👤 اللاعب 2: `{st.session_state.p2_score}` نقطة")
        if st.session_state.p1_score > st.session_state.p2_score:
            st.success("🏅 الفائز: اللاعب 1")
        elif st.session_state.p2_score > st.session_state.p1_score:
            st.success("🏅 الفائز: اللاعب 2")
        else:
            st.warning("🤝 تعادل مثير!")

# ♻️ زر إعادة التشغيل
if st.button("🔄 أعد اللعبة"):
    st.session_state.round = 1
    st.session_state.p1_score = 0
    st.session_state.p2_score = 0
