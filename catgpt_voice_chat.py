import streamlit as st
st.set_page_config(page_title="CatGPT Voice", page_icon="🐱")

from gtts import gTTS
import speech_recognition as sr
import tempfile
from streamlit_audio_recorder import audio_recorder
from pydub import AudioSegment
import os

st.title("🗣️ Sesli CatGPT")

st.markdown("🎙️ Aşağıdaki mikrofon butonuna tıklayıp sorunu sesli söyleyebilirsin. CatGPT cevap verecek (sesli + yazılı).")

# 1. Ses kaydını al
audio_bytes = audio_recorder(text="🎤 Soru Sor", recording_color="#e53935", neutral_color="#6c757d", icon_size="2x")

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    st.info("Ses alındı, metne dönüştürülüyor...")

    # 2. Geçici WAV dosyasına yaz
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_file:
        wav_file.write(audio_bytes)
        wav_path = wav_file.name

    # 3. Ses → Metin
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)

    try:
        question = recognizer.recognize_google(audio_data, language="tr-TR")
        st.success(f"❓ Sorduğun: {question}")
    except sr.UnknownValueError:
        st.error("⚠️ Ses anlaşılamadı. Lütfen daha net konuş.")
        question = None
    except sr.RequestError:
        st.error("⚠️ Google API erişim hatası.")
        question = None

    # 4. CatGPT cevabı üret (dummy logic)
    if question:
        if "yemek" in question.lower():
            response = "Kedinizin beslenmesine dikkat edin, kaliteli mama kullanın."
        elif "tüy" in question.lower():
            response = "Tüy dökülmesi mevsimsel olabilir, düzenli tarama yapmalısınız."
        else:
            response = "Veteriner önerisi için detaylı bilgi gerekebilir ama genel sağlığı kontrol edin."

        st.markdown("🟢 **CatGPT Cevabı:** " + response)

        # 5. gTTS ile sesli cevap
        tts = gTTS(text=response, lang="tr", tld="com.tr")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tts_file:
            tts.save(tts_file.name)
            st.audio(tts_file.name, format="audio/mp3")
            st.caption("🔊 CatGPT cevabını dinleyebilirsin.")
