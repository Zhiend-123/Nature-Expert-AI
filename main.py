# 1 простой вариант

import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(
    page_title="Nature Expert AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #2e7d32;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        border: none;
        color: white;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    .result-card {
        background-color: black;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2913/2913520.png", width=100)
    st.title("Настройки")
    api_key = st.text_input("API Key", value="AIzaSyB1Bu1tLvt_raHE_RDXsI6jhUvL5M1skfQ", type="password")

    st.divider()
    st.info("""
    **Как использовать:**
    1. Загрузите четкое фото.
    2. Нажмите 'Анализировать'.
    3. Дождитесь вердикта ИИ.
    """)

    model_name = st.selectbox("Модель ИИ", ["models/gemini-2.5-flash"])

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name)

st.title("🌿 Nature Expert AI")
st.markdown("##### *Умный анализ птиц, грибов и минералов на базе мультимодального ИИ*")

st.divider()
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📸 Загрузка данных")
    uploaded_file = st.file_uploader("Выберите изображение...", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Объект для анализа", use_container_width=True)
        analyze_btn = st.button("🔍 Начать глубокий анализ")
    else:
        st.info("Пожалуйста, загрузите фотографию для начала работы.")
with col2:
    st.subheader("🧠 Вердикт ИИ")
    if uploaded_file and analyze_btn:
        with st.spinner('Изучаю текстуры и признаки...'):
            try:
                prompt = """
                Ты эксперт-натуралист. Проанализируй фото:
                Используй строго этот формат (каждый пункт с новой строки):

                1. *ТИП:* (птица, гриб или минерал)
                2. *НАЗВАНИЕ:* (Русское + Латынь)
                3. *ДЕТАЛИ:* (ключевые признаки)
                4. *ОСОБЕННОСТИ:* (описание ареала, съедобности или твердости)

                Отвечай на русском языке. Между пунктами делай двойной перенос строки.
                """
                response = model.generate_content([prompt, image])

                formatted_text = response.text.replace('\n', '<br>')
                st.markdown(f"""
                <div class="result-card" style="line-height: 1.6;">
                    {formatted_text}
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Ошибка: {e}")
    else:
        st.write("Результаты появятся здесь после завершения анализа.")

st.divider()
footer_col1, footer_col2 = st.columns([3, 1])
with footer_col1:
    st.caption(
        "⚠️ **Отказ от ответственности:** ИИ может ошибаться. Никогда не употребляйте в пищу грибы, основываясь только на анализе приложения.")
with footer_col2:
    st.caption("v1.0")
