import streamlit as st
from streamlit_option_menu import option_menu


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

