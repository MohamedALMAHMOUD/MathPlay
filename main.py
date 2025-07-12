import streamlit as st

st.set_page_config(
    page_title="MathPlay | الرياضيات بين اللعب والتفاعل",
    layout="centered",
)

st.title("👋 مرحبًا بك في MathPlay")
st.markdown("""
<div dir="rtl" style="text-align: right;">
هذه منصة تعليمية تفاعلية تهدف إلى تسهيل فهم الرياضيات عبر اللعب والتفاعل.<br>
<br>
🎯 في القائمة الجانبية على اليمين يمكنك اختيار موضوع أو لعبة:<br>
- 📐 مركز الأبعاد المتجانس: شرح تفاعلي مع أمثلة.<br>
- 🎮 لعبة مركز الأبعاد: لعبة تفاعلية لتحريك الكتل وحساب المركز.<br>
<br>
📚 استمتع بالتعلم وشاركنا اقتراحاتك!
</div>
""", unsafe_allow_html=True)
