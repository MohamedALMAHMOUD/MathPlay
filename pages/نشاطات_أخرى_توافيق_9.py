import streamlit as st
import random
import math

st.set_page_config(page_title="🎓 نشاط تفاعلي في التعداد", layout="wide")
st.title("🎓 نشاط تفاعلي لفهم التعداد")

# قائمة الوضعيات
situations = [
    {'situation_ar': 'يتم إنشاء رمز سري مكون من 6 رموز يتم اختيارها عشوائيا من بين 10 رموز مختلفة.', 'n': 10, 'k': 6, 'repetition': True, 'ordre': True, 'complet': False, 'type': 'ترتيب مع تكرار (n^k)'},
    {'situation_ar': 'يختار التلميذ 3 كتب عشوائيا من أصل 12 لقراءتها مرة واحدة.', 'n': 12, 'k': 3, 'repetition': False, 'ordre': False, 'complet': False, 'type': 'توافيق بدون تكرار (C(n,k))'},
    {'situation_ar': 'يختار تلميذ ترتيبا لجلوس 5 طلاب في 5 كراسي.', 'n': 5, 'k': 5, 'repetition': False, 'ordre': True, 'complet': True, 'type': 'ترتيب كامل (n!)'},
    {'situation_ar': 'يتم اختيار 4 طلاب لتمثيل القسم في مسابقة، حيث يتم تعيين قائد و3 مساعدين.', 'n': 10, 'k': 4, 'repetition': False, 'ordre': True, 'complet': False, 'type': 'ترتيب جزئي (P(n,k))'},
    {'situation_ar': 'يختار التلميذ 4 أنواع من الفاكهة (من أصل 5) لصنع سلطة، ويمكنه اختيار نفس الفاكهة أكثر من مرة.', 'n': 5, 'k': 4, 'repetition': True, 'ordre': False, 'complet': False, 'type': 'توافيق مع تكرار (C(n+k-1,k))'},
]

# تهيئة الحالة
if "situation" not in st.session_state:
    st.session_state.situation = random.choice(situations)
    st.session_state.etape = 0
    st.session_state.repetition = None
    st.session_state.ordre = None
    st.session_state.complet = None

situation = st.session_state.situation

# رسم الشجرة بدقة
def generer_arbre(rep=None, ordre=None, complet=None):
    def style_noeud(id, label, actif):
        color = "#87CEEB" if actif else "#f0f0f0"
        return f'{id} [label="{label}", style="rounded,filled", fontname="Arial", fillcolor="{color}"];'

    g = ['digraph G {', 'rankdir=LR;', 'node [shape=box];']

    # تكرار
    g.append(style_noeud("A", "🔢 هل السحب مع تكرار؟", rep is not None))
    g.append(style_noeud("B1", "✅ نعم", rep is True))
    g.append(style_noeud("B2", "❌ لا", rep is False))

    # ترتيب
    g.append(style_noeud("C1", "📐 هل الترتيب مهم؟", rep is True and ordre is not None))
    g.append(style_noeud("C2", "📐 هل الترتيب مهم؟", rep is False and ordre is not None))

    # نهايات
    g.append(style_noeud("D1", "✅ نعم", rep is True and ordre is True))
    g.append(style_noeud("D2", "❌ لا", rep is True and ordre is False))
    g.append(style_noeud("D3", "✅ نعم", rep is False and ordre is True))
    g.append(style_noeud("D4", "❌ لا", rep is False and ordre is False))

    g.append(style_noeud("R1", "📌 النوع:\nترتيب مع تكرار (n^k)", rep is True and ordre is True))
    g.append(style_noeud("R2", "📌 النوع:\nتوافيق مع تكرار C(n+k-1,k)", rep is True and ordre is False))
    g.append(style_noeud("R3", "🔍 هل تأخذ كل العناصر؟", rep is False and ordre is True and complet is not None))
    g.append(style_noeud("R4", "📌 النوع:\nتوافيق بدون تكرار C(n,k)", rep is False and ordre is False))
    g.append(style_noeud("R5", "📌 النوع:\nترتيب جزئي P(n,k)", rep is False and ordre is True and complet is False))
    g.append(style_noeud("R6", "📌 النوع:\nترتيب كامل (n!)", rep is False and ordre is True and complet is True))

    g += [
        "A -> B1", "A -> B2",
        "B1 -> C1", "B2 -> C2",
        "C1 -> D1", "C1 -> D2",
        "C2 -> D3", "C2 -> D4",
        "D1 -> R1", "D2 -> R2",
        "D4 -> R4", "D3 -> R3",
        "R3 -> R5 [label=\"❌ لا\"]", "R3 -> R6 [label=\"✅ نعم\"]"
    ]
    g.append("}")
    return "\n".join(g)

# واجهة
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"### 🧮 الوضعية:\n{ situation['situation_ar'] }")

    if st.session_state.etape == 0:
        choix = st.radio("❓ هل التكرار مسموح؟", ["✅ نعم", "❌ لا"])
        if st.button("➡️ التالي"):
            st.session_state.repetition = choix == "✅ نعم"
            if st.session_state.repetition == situation["repetition"]:
                st.session_state.etape += 1
            else:
                st.warning("✋ أعد التفكير، هل يمكن اختيار نفس العنصر أكثر من مرة؟")

    elif st.session_state.etape == 1:
        choix = st.radio("❓ هل الترتيب مهم؟", ["✅ نعم", "❌ لا"])
        if st.button("➡️ التالي"):
            st.session_state.ordre = choix == "✅ نعم"
            if st.session_state.ordre == situation["ordre"]:
                if not situation["repetition"] and st.session_state.ordre:
                    st.session_state.etape += 1
                else:
                    st.session_state.etape = 3
            else:
                st.warning("✋ أعد التفكير: هل يغيّر الترتيب النتيجة؟")

    elif st.session_state.etape == 2:
        choix = st.radio("❓ هل جميع العناصر مستخدمة؟", ["✅ نعم", "❌ لا"])
        if st.button("➡️ التالي"):
            st.session_state.complet = choix == "✅ نعم"
            if st.session_state.complet == situation["complet"]:
                st.session_state.etape += 1
            else:
                st.warning("✋ فكر مجددًا: هل يتم استخدام كل العناصر؟")

    elif st.session_state.etape == 3:
        reponse = st.selectbox("📌 ما هو نوع التعداد المناسب؟", [
            "ترتيب مع تكرار (n^k)",
            "توافيق مع تكرار (C(n+k-1,k))",
            "ترتيب كامل (n!)",
            "ترتيب جزئي (P(n,k))",
            "توافيق بدون تكرار (C(n,k))"
        ])
        if st.button("🎯 تحقق"):
            if reponse == situation["type"]:
                st.success("✅ إجابة صحيحة!")
                st.session_state.etape += 1
            else:
                st.error("❌ حاول مرة أخرى. هذا ليس النوع الصحيح.")

    elif st.session_state.etape == 4:
        def calc(n, k, rep, ord, comp):
            if comp and ord and not rep:
                return math.factorial(n)
            if rep and ord:
                return n ** k
            if not rep and ord:
                return math.perm(n, k)
            if not rep and not ord:
                return math.comb(n, k)
            if rep and not ord:
                return math.comb(n + k - 1, k)

        user_val = st.number_input("🧮 أدخل عدد الإمكانيات:", min_value=0, step=1)
        if st.button("🔍 تحقق من النتيجة"):
            correct = calc(situation['n'], situation['k'], situation['repetition'], situation['ordre'], situation['complet'])
            if user_val == correct:
                st.success("✅ أحسنت! النتيجة صحيحة.")
            else:
                st.error(f"❌ الإجابة غير صحيحة. النتيجة الصحيحة هي: `{correct}`")

    if st.button("🔁 تمرين جديد"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

with col2:
    st.markdown("### 🌳 الشجرة التفاعلية")
    st.graphviz_chart(generer_arbre(
        st.session_state.get('repetition'),
        st.session_state.get('ordre'),
        st.session_state.get('complet')
    ))



st.title("🌲 شجرة اتخاذ القرار: كيف تختار النوع الصحيح للعد؟")

st.markdown("اتبع الشجرة أدناه لمعرفة نوع التعداد المناسب حسب خصائص المسألة.")

st.graphviz_chart("""
digraph D {
    node [shape=box style=rounded fontname="Arial"];

    A [label="🔢 هل السحب \nمع تكرار؟"];
    B1 [label="✅ نعم"];
    B2 [label="❌ لا"];

    C1 [label="📐 هل الترتيب مهم؟"];
    C2 [label="📐 هل الترتيب مهم؟"];

    D1 [label="✅ نعم"];
    D2 [label="❌ لا"];
    D3 [label="✅ نعم"];
    D4 [label="❌ لا"];

    R1 [label="📌 النوع: \nترتيب أو تراتيب مع تكرار\n(n^k)", shape=ellipse, style=filled, fillcolor=lightblue];
    R2 [label="📌 النوع: \nتوافيق مع تكرار\n(C(n+k-1, k))", shape=ellipse, style=filled, fillcolor=lightgreen];
    R3 [label="🔍 هل تأخذ كل العناصر؟"];
    R4 [label="📌 النوع: \nتوافيق بدون تكرار\n(C(n,k))", shape=ellipse, style=filled, fillcolor=lightgreen];
    R5 [label="📌 النوع: \nترتيب أو تراتيب مع التكرار\n(P(n,k))", shape=ellipse, style=filled, fillcolor=lightblue];
    R6 [label="📌 النوع: \nترتيب لكل العناصر\n(n!)", shape=ellipse, style=filled, fillcolor=orange];

    A -> B1;
    A -> B2;

    B1 -> C1;
    B2 -> C2;

    C1 -> D1;
    C1 -> D2;
    C2 -> D3;
    C2 -> D4;

    D1 -> R1;
    D2 -> R2;
    D4 -> R4;
    D3 -> R3;

    R3 -> R5 [label="❌ لا"];
    R3 -> R6 [label="✅ نعم"];
}
""")

