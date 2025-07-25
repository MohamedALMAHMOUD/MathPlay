import streamlit as st
import os
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from datetime import datetime
import openai
from openai import OpenAI
import math
from dotenv import load_dotenv
import time

# Charger variables d'env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

st.set_page_config(
    page_title="MathPlay | منصة لتعلم الرياضيات عن طريق اللعب والتفاعل",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🎮 MathPlay - منصة لتعلم الرياضيات عن طريق اللعب والتفاعل")


st.markdown("""
مرحباً بك في **MathPlay**، بيئة تعليمية تفاعلية تربط بين مفاهيم الرياضيات والتطبيق العملي عبر المحاكاة والألعاب!

🧠 في هذا التطبيق يمكنك:
- 🧲 استكشاف **مركز الأبعاد المتجانس** عبر محاكاة مرئية.
- 🎯 تجربة ألعاب بسيطة لفهم المفهوم بعمق.
- ✅ اختبار نفسك ومعرفة مدى استيعابك للفكرة.

🚀 **اختر صفحة من القائمة الجانبية وابدأ اللعب والتعلّم!**
""", unsafe_allow_html=True)

# === Reformulation avec ChatGPT ===
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def reformulate_question(text):
    try:
        system_msg = "Tu es un professeur de mathématiques expert et spécialisé dans le manuel de la terminale"
        user_msg = f"Reformule clairement la question posée par l'élève et répondre à la question en arabe : {text}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Erreur GPT : {e}")
        return text

# === Génération audio + vidéo ===
def generate_video(text_input):
    question = reformulate_question(text_input)

    audio_filename = "audio_arabe.mp3"
    tts = gTTS(text=question, lang="ar")
    tts.save(audio_filename)

    base_video = VideoFileClip("images/video.mp4")
    audio = AudioFileClip(audio_filename)

    repeat_count = math.ceil(audio.duration / base_video.duration)
    video_long = concatenate_videoclips([base_video] * repeat_count)
    video_final = video_long.set_duration(audio.duration)
    video_final = video_final.set_audio(audio)

    output_filename = f"video_final_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
    video_final.write_videofile(output_filename, fps=25, verbose=False, logger=None)

    return output_filename, question

# === Interface Streamlit ===
st.set_page_config(page_title="🎙️ MathBot GPT", layout="centered")
st.title("🤖 بوت يرد عليك بشكل تلقائي")
st.markdown("اطرح سؤالك بكل مايتعلق برياضيات البكالوريا📽️")

text_input = st.text_area("✏️ اطرح سؤالك هنا :", height=150, placeholder="مثال : ما الفرق بين التوافيق والتراتيب؟")

if st.button("🎬 اطرح سؤالك"):
    if not text_input.strip():
        st.warning("✋ أكتب سؤالك أولا.")
    else:
        with st.spinner("🛠️ الجواب..."):
            video_path, reformulated = generate_video(text_input)
            if "\frac" in reformulated or "\\" in reformulated:
                st.markdown("**🧮 Reformulation mathématique (LaTeX)**")
                st.latex(reformulated)
            else: st.markdown(f"**🔁 الجواب كتابة :** {reformulated}")
            st.markdown(f"**🔁 الجواب فيديو :** ")
            
            st.video(video_path)
            time.sleep(1)  # attendre un petit instant
            try:
                os.remove(video_path)
                st.info("✅ Vidéo supprimée après affichage.")
            except Exception as e:
                st.warning(f"❌ Erreur de suppression : {e}")