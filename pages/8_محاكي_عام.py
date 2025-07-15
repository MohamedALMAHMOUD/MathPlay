import streamlit as st
import math
import random
from itertools import combinations, combinations_with_replacement, permutations, product
from collections import defaultdict, Counter
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ✅ إعداد الصفحة
st.set_page_config(page_title="🎲 محاكي التعداد المتقدم", layout="wide")
st.title("🎲 محاكي التعداد المتقدم")
st.markdown("صمم مشكلة التعداد الخاصة بك واستكشف جميع الإمكانيات مع تصورات تفاعلية 🔍")

# ⚙️ إعدادات متقدمة
st.header("⚙️ إعداد الكائنات")

# إعداد أكثر مرونة
config_mode = st.radio("🎯 نمط الإعداد", ["بسيط", "متقدم"])

if config_mode == "بسيط":
    nb_objets = st.number_input("🧩 عدد أنواع الكائنات", min_value=1, value=3, max_value=10)
    
    col_config = st.columns(min(nb_objets, 4))
    types_par_objet = []
    noms_objets = []
    
    for i in range(nb_objets):
        with col_config[i % 4]:
            nom = st.text_input(f"اسم الكائن {i+1}", value=f"كائن_{i+1}")
            types = st.number_input(f"🎨 المتغيرات لـ {nom}", min_value=1, value=3, max_value=20)
            types_par_objet.append(types)
            noms_objets.append(nom)
else:
    st.markdown("**إعداد متقدم بأوزان مخصصة**")
    if 'objets_config' not in st.session_state:
        st.session_state.objets_config = [{"nom": "كائن_1", "variantes": 3, "poids": [1, 1, 1]}]
    
    # واجهة لإضافة/إزالة الكائنات
    col_add, col_remove = st.columns(2)
    with col_add:
        if st.button("➕ إضافة كائن"):
            st.session_state.objets_config.append({
                "nom": f"كائن_{len(st.session_state.objets_config)+1}", 
                "variantes": 2, 
                "poids": [1, 1]
            })
    
    with col_remove:
        if st.button("➖ حذف الأخير") and len(st.session_state.objets_config) > 1:
            st.session_state.objets_config.pop()
    
    # إعداد تفصيلي
    types_par_objet = []
    noms_objets = []
    poids_objets = []
    
    for i, obj_config in enumerate(st.session_state.objets_config):
        with st.expander(f"🎨 إعداد {obj_config['nom']}"):
            col1, col2 = st.columns(2)
            with col1:
                nom = st.text_input(f"الاسم", value=obj_config['nom'], key=f"nom_{i}")
                variantes = st.number_input(f"عدد المتغيرات", min_value=1, value=obj_config['variantes'], key=f"var_{i}")
            
            with col2:
                st.markdown("**أوزان المتغيرات:**")
                poids = []
                for j in range(variantes):
                    poids_val = st.number_input(f"وزن المتغير {j+1}", min_value=0.1, value=1.0, step=0.1, key=f"poids_{i}_{j}")
                    poids.append(poids_val)
        
        types_par_objet.append(variantes)
        noms_objets.append(nom)
        poids_objets.append(poids)

n = sum(types_par_objet)  # إجمالي العناصر

# 🎯 إعدادات السحب
st.markdown("---")
st.header("🎯 إعدادات السحب")

col1, col2 = st.columns(2)
with col1:
    tirage_k = st.number_input("🎯 عدد العناصر المراد سحبها", min_value=1, value=min(2, n), max_value=n if n <= 20 else 20)
with col2:
    nb_simulations = st.number_input("🔄 عدد المحاكيات", min_value=1, value=1000, max_value=100000)

col1, col2, col3 = st.columns(3)
with col1:
    remise = st.radio("🔁 الإرجاع", ["✅ مع الإرجاع", "❌ بدون إرجاع"])
with col2:
    ordre = st.radio("📐 أهمية الترتيب", ["✅ مهم", "❌ غير مهم"])
with col3:
    numerote = st.radio("🔢 العناصر قابلة للتمييز", ["✅ نعم", "❌ لا"])

# ✅ الحسابات والعرض
st.markdown("---")
if st.button("🚀 حساب وتحليل", type="primary"):
    # التحقق من الجدوى
    possible = True
    if remise == "❌ بدون إرجاع" and tirage_k > n:
        possible = False
        st.error("🚫 مستحيل: سحب بدون إرجاع مع k > n")
    
    if possible:
        # 🔢 حساب الإمكانيات
        def calcul_possibilites(n, k, remise, ordre):
            if remise == "✅ مع الإرجاع" and ordre == "✅ مهم":
                return n ** k, "ترتيبات مع تكرار", f"n^k = {n}^{k}"
            elif remise == "✅ مع الإرجاع" and ordre == "❌ غير مهم":
                return math.comb(n + k - 1, k), "تركيبات مع تكرار", f"C(n+k-1,k) = C({n}+{k}-1,{k})"
            elif remise == "❌ بدون إرجاع" and ordre == "✅ مهم":
                return math.perm(n, k), "ترتيبات بدون تكرار", f"A(n,k) = {n}!/{n-k}!"
            elif remise == "❌ بدون إرجاع" and ordre == "❌ غير مهم":
                return math.comb(n, k), "تركيبات بدون تكرار", f"C(n,k) = C({n},{k})"

        resultat, type_calc, formule = calcul_possibilites(n, tirage_k, remise, ordre)

        # عرض النتائج الرئيسية
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 نوع الحساب", type_calc)
        with col2:
            st.metric("🔢 النتيجة النظرية", f"{resultat:,}")
        with col3:
            st.metric("📐 الصيغة", formule)

        # 📦 توليد فضاء العينة
        espace = []
        index_objet = 0
        for i, (nom, count) in enumerate(zip(noms_objets, types_par_objet)):
            for j in range(count):
                if numerote == "✅ نعم":
                    espace.append(f"{nom}_{j+1}")
                else:
                    espace.append(f"{nom}")
                index_objet += 1

        # 🎲 محاكاة مونتي كارلو
        st.subheader("🎲 المحاكاة والتحليل الإحصائي")
        
        def generer_tirage():
            if remise == "✅ مع الإرجاع":
                if ordre == "✅ مهم":
                    return tuple(random.choices(espace, k=tirage_k))
                else:
                    return tuple(sorted(random.choices(espace, k=tirage_k)))
            else:
                if ordre == "✅ مهم":
                    return tuple(random.sample(espace, tirage_k))
                else:
                    return tuple(sorted(random.sample(espace, tirage_k)))

        # توليد السحوبات
        tirages = [generer_tirage() for _ in range(nb_simulations)]
        compteur_tirages = Counter(tirages)

        # التحليل الإحصائي
        tirages_uniques = len(compteur_tirages)
        frequence_max = max(compteur_tirages.values())
        frequence_min = min(compteur_tirages.values())
        frequence_moyenne = sum(compteur_tirages.values()) / len(compteur_tirages)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🎯 السحوبات الفريدة المُلاحظة", f"{tirages_uniques:,}")
        with col2:
            st.metric("📈 أعلى تكرار", frequence_max)
        with col3:
            st.metric("📉 أقل تكرار", frequence_min)
        with col4:
            st.metric("📊 متوسط التكرار", f"{frequence_moyenne:.1f}")

        
        # 🌲 شجرة الإمكانيات المرجحة
        if resultat <= 1000:  # حد معقول
            st.subheader("🌲 شجرة الإمكانيات المرجحة")
            
            # توليد جميع الإمكانيات
            if remise == "✅ مع الإرجاع":
                if ordre == "✅ مهم":
                    toutes_possibilites = list(product(espace, repeat=tirage_k))
                else:
                    toutes_possibilites = list(combinations_with_replacement(espace, tirage_k))
            else:
                if ordre == "✅ مهم":
                    toutes_possibilites = list(permutations(espace, tirage_k))
                else:
                    toutes_possibilites = list(combinations(espace, tirage_k))

            # بناء الشجرة الهرمية
            arbre_data = defaultdict(lambda: defaultdict(int))
            
            for possibilite in toutes_possibilites:
                freq_theorique = compteur_tirages.get(possibilite, 0)
                prob_theorique = freq_theorique / nb_simulations if nb_simulations > 0 else 1/len(toutes_possibilites)
                
                # المستوى الأول: العنصر الأول
                niveau1 = possibilite[0]
                arbre_data[niveau1]["total"] += prob_theorique
                
                # المستوى الثاني: التركيبة الكاملة
                niveau2 = " → ".join(possibilite)
                arbre_data[niveau1][niveau2] = prob_theorique

            # إنشاء الرسم البياني الشجري (Sunburst)
            labels = []
            parents = []
            values = []
            
            # الجذر
            labels.append("جميع الإمكانيات")
            parents.append("")
            values.append(1.0)
            
            # المستوى الأول
            for niveau1, data in arbre_data.items():
                labels.append(niveau1)
                parents.append("جميع الإمكانيات")
                values.append(data["total"])
                
                # المستوى الثاني
                for niveau2, prob in data.items():
                    if niveau2 != "total":
                        labels.append(niveau2)
                        parents.append(niveau1)
                        values.append(prob)

            if len(labels) > 1:
                fig_sunburst = go.Figure(go.Sunburst(
                    labels=labels,
                    parents=parents,
                    values=values,
                    branchvalues="total",
                    hovertemplate="<b>%{label}</b><br>الاحتمال: %{value:.3f}<extra></extra>"
                ))
                fig_sunburst.update_layout(title="شجرة الإمكانيات المرجحة", height=600)
                st.plotly_chart(fig_sunburst, use_container_width=True)

        # 📊 التصورات
        st.subheader("📊 التصورات")
        
        # رسم بياني للتكرارات
        if len(compteur_tirages) <= 50:  # حد للوضوح
            df_freq = pd.DataFrame([
                {"السحب": str(tirage), "التكرار": freq, "الاحتمال": freq/nb_simulations}
                for tirage, freq in compteur_tirages.most_common(20)
            ])
            
            fig = px.bar(df_freq, x="السحب", y="التكرار", 
                        title="أعلى 20 سحب من حيث التكرار",
                        hover_data=["الاحتمال"])
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)

        # توزيع التكرارات
        freq_distribution = Counter(compteur_tirages.values())
        df_dist = pd.DataFrame([
            {"التكرار": freq, "عدد السحوبات": count}
            for freq, count in freq_distribution.items()
        ])
        
        fig2 = px.bar(df_dist, x="التكرار", y="عدد السحوبات",
                     title="توزيع تكرارات الظهور")
        st.plotly_chart(fig2, use_container_width=True)
        # 📋 جدول مفصل
        if st.checkbox("📋 عرض الجدول التفصيلي للنتائج"):
            if len(compteur_tirages) <= 200:
                df_details = pd.DataFrame([
                    {
                        "الترتيب": i+1,
                        "السحب": str(tirage),
                        "التكرار الملاحظ": freq,
                        "الاحتمال الملاحظ": f"{freq/nb_simulations:.4f}",
                        "الاحتمال النظري": f"{1/resultat:.4f}" if resultat > 0 else "غير متاح"
                    }
                    for i, (tirage, freq) in enumerate(compteur_tirages.most_common())
                ])
                st.dataframe(df_details, use_container_width=True)
            else:
                st.warning("نتائج كثيرة جداً للعرض في جدول. استخدم الرسوم البيانية أعلاه.")

        # 🎲 عينات من السحوبات
        if st.checkbox("🎲 عرض عينات من السحوبات"):
            st.subheader("عينات من السحوبات المولدة")
            echantillons = random.sample(tirages, min(10, len(tirages)))
            for i, tirage in enumerate(echantillons, 1):
                st.write(f"**السحب {i}:** {' → '.join(tirage)}")

        # 📈 تحليل التقارب
        if st.checkbox("📈 تحليل التقارب"):
            st.subheader("تحليل التقارب")
            
            # حساب تقارب عدد السحوبات الفريدة
            tirages_progressifs = []
            uniques_progressifs = []
            seen = set()
            
            for i, tirage in enumerate(tirages, 1):
                seen.add(tirage)
                if i % (nb_simulations // 100) == 0 or i == nb_simulations:
                    tirages_progressifs.append(i)
                    uniques_progressifs.append(len(seen))
            
            df_convergence = pd.DataFrame({
                "عدد السحوبات": tirages_progressifs,
                "السحوبات الفريدة": uniques_progressifs,
                "النظري": [min(resultat, x) for x in tirages_progressifs]
            })
            
            fig_conv = px.line(df_convergence, x="عدد السحوبات", 
                             y=["السحوبات الفريدة", "النظري"],
                             title="تقارب عدد السحوبات الفريدة")
            st.plotly_chart(fig_conv, use_container_width=True)

        # 💡 نصائح وتفسير
        st.subheader("💡 تفسير النتائج")
        
        if tirages_uniques == resultat:
            st.success(f"✅ **ممتاز!** تم ملاحظة جميع السحوبات النظرية البالغ عددها {resultat}.")
        elif tirages_uniques < resultat:
            coverage = (tirages_uniques / resultat) * 100
            st.info(f"📊 **التغطية: {coverage:.1f}%** - {tirages_uniques} سحب فريد من أصل {resultat} محتمل.")
            if coverage < 90:
                st.warning("⚠️ قم بزيادة عدد المحاكيات للحصول على تغطية أفضل.")
        
        # تحليل التجانس
        frequence_attendue = nb_simulations / resultat
        ecart_type = math.sqrt(sum((f - frequence_attendue)**2 for f in compteur_tirages.values()) / len(compteur_tirages))
        
        if ecart_type < frequence_attendue * 0.1:
            st.success("✅ **توزيع منتظم**: السحوبات موزعة بشكل جيد.")
        elif ecart_type < frequence_attendue * 0.3:
            st.info("📊 **توزيع مقبول**: تغيير طفيف في التكرارات.")
        else:
            st.warning("⚠️ **توزيع غير منتظم**: تغيير كبير في التكرارات.")

# 📚 قسم المساعدة
with st.expander("📚 دليل الاستخدام"):
    st.markdown("""
    ## أنواع التعداد
    
    **🔄 مع الإرجاع + 📐 الترتيب مهم**: ترتيبات مع تكرار (n^k)
    - مثال: رمز PIN من 4 أرقام
    
    **🔄 مع الإرجاع + 📐 الترتيب غير مهم**: تركيبات مع تكرار
    - مثال: اختيار 3 فواكه من سلة (مع إمكانية التكرار)
    
    **🚫 بدون إرجاع + 📐 الترتيب مهم**: ترتيبات بدون تكرار
    - مثال: منصة التتويج لـ 3 أشخاص من بين 10 مشاركين
    
    **🚫 بدون إرجاع + 📐 الترتيب غير مهم**: تركيبات بدون تكرار
    - مثال: فريق من 5 أشخاص من بين 20 مرشح
    
    ## تفسير التصورات
    
    - **رسم بياني للتكرارات**: يظهر أي السحوبات تظهر بشكل أكثر تكراراً
    - **توزيع التكرارات**: يشير إلى انتظام التوزيع
    - **الشجرة المرجحة**: تصور التسلسل الهرمي للإمكانيات مع احتمالاتها
    - **التقارب**: يظهر كيف يتطور عدد السحوبات الفريدة
    """)