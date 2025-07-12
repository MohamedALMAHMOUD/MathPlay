import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import matplotlib.pyplot as plt
from streamlit_drawable_canvas import st_canvas

# === إعداد الصفحة ===
st.set_page_config(page_title="MathPlay | الرياضيات بين اللعب والتفاعل", layout="wide")

# === القائمة الجانبية على اليمين ===
with st.sidebar:
    selected = option_menu(
        menu_title="📚 القائمة الرئيسية",
        options=["🏠 الصفحة الرئيسية", "📌 مركز الأبعاد المتجانس", "🧪 اختبر فهمك"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical"
    )

# === 1. الصفحة الرئيسية ===
if selected == "🏠 الصفحة الرئيسية":
    st.title("🎮 MathPlay | الرياضيات بين اللعب والتفاعل")
    st.markdown("""
    <div dir="rtl" style="text-align: right; font-size: 20px;">
    مرحبًا بك في منصة <b>MathPlay</b> التعليمية!  
    هنا نمزج بين اللعب، التفاعل، والتفكير النقدي لفهم مفاهيم الرياضيات بشكل أعمق وأكثر متعة 🤩  
    اختر من القائمة الجانبية لتبدأ التعلم التفاعلي.
    </div>
    """, unsafe_allow_html=True)

# === 2. مركز الأبعاد المتجانس ===
elif selected == "📌 مركز الأبعاد المتجانس":
    st.title("📌 محاكي لحساب مركز الأبعاد المتجانس")

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

# === 3. اختبر فهمك ===
elif selected == "🧪 اختبر فهمك":
    st.title("🧠 اختبار تفاعلي: هل فهمت مفهوم مركز الأبعاد؟")
    score = 0

    with st.form("quiz_form"):
        q1 = st.radio("ما هو الشرط الأساسي لوجود مركز أبعاد متجانس لمجموعة نقاط؟", [
            "يجب أن تكون الكتل متساوية", 
            "يجب أن تكون الكتل موجبة", 
            "يجب أن تكون النقاط على خط مستقيم"
        ])

        q2 = st.radio("إذا كانت كل الكتل متساوية، فأين يقع مركز الأبعاد؟", [
            "في مركز الكتلة الأكبر", 
            "في متوسط الإحداثيات", 
            "في أقرب نقطة للأصل"
        ])

        q3 = st.radio("ما الذي يحدد تأثير نقطة معينة في موقع المركز؟", [
            "لون النقطة", 
            "قربها من الأصل", 
            "كتلتها"
        ])

        submitted = st.form_submit_button("🔍 تحقق من إجاباتك")

        if submitted:
            if q1 == "يجب أن تكون الكتل موجبة": score += 1
            if q2 == "في متوسط الإحداثيات": score += 1
            if q3 == "كتلتها": score += 1

            st.success(f"✔️ نتيجتك: {score}/3")
            if score == 3:
                st.balloons()
                st.markdown("🎉 ممتاز! لديك فهم عميق للمفهوم.")
            else:
                st.markdown("👀 راجع المحاكي وجرّب مرة أخرى.")

