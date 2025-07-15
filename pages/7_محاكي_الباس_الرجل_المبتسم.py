
import streamlit as st
from PIL import Image
from itertools import product
import pathlib
import time

# 📁 Dossier des assets
ASSETS = pathlib.Path("images")

# 🎨 Lire automatiquement les fichiers disponibles
bonnet_list = sorted([p.stem for p in (ASSETS/"bonnet").glob("*.png")])
tshirt_list = sorted([p.stem for p in (ASSETS/"tshirt").glob("*.png")])
pantalon_list = sorted([p.stem for p in (ASSETS/"pantalon").glob("*.png")])

# 🧠 Page config
st.set_page_config(page_title="محاكي إلباس الرجل المبتسم", page_icon="🧍‍♂️")
st.title("🧍‍♂️ محاكي إلباس الرجل المبتسم")

st.markdown("👕 **اختر ألوان كل جزء :**")

# 🎛️ Sélections multiples
col1, col2, col3 = st.columns(3)
with col1:
    bonnet_colors = st.multiselect("🧢 القبعة", bonnet_list, default=bonnet_list)
with col2:
    tshirt_colors = st.multiselect("👕 القميص", tshirt_list, default=tshirt_list)
with col3:
    pantalon_colors = st.multiselect("👖 البنطال", pantalon_list, default=pantalon_list)

# 👇 Générer sur clic
if st.button("🎨 أطلق عملية تشكيل كل الخيارات الممكنة"):
    combos = list(product(bonnet_colors, tshirt_colors, pantalon_colors))
    st.success(f"{len(combos)} لوكات قيد التشكيل... ⏳")

    base_img = Image.open(ASSETS / "base.png")

    # Nombre de bonhommes par ligne (tu peux ajuster selon ton design)
    NB_PAR_LIGNE = 3

    # Zone dynamique d'affichage
    rows = [combos[i:i+NB_PAR_LIGNE] for i in range(0, len(combos), NB_PAR_LIGNE)]

    for ligne in rows:
        cols = st.columns(len(ligne))
        for idx, (bonnet, tshirt, pantalon) in enumerate(ligne):
            composed = base_img.copy()
            for layer, part in zip([pantalon, tshirt, bonnet], ["pantalon", "tshirt", "bonnet"]):
                img = Image.open(ASSETS / f"{part}/{layer}.png")
                composed.paste(img, (0, 0), mask=img)

            cols[idx].image(composed, caption=f"{bonnet} | {tshirt} | {pantalon}", width=180)
        time.sleep(1)  # petit délai entre chaque ligne