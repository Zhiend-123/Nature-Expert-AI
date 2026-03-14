import streamlit as st
from PIL import Image
from src.brain import setup_ai, get_nature_analysis
from src.history_manager import save_history, load_history, get_exif_coords
from streamlit_folium import folium_static
import folium
from datetime import datetime

# st.set_page_config(
#     page_title="Nature Expert AI",
#     page_icon="🌿",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

try:
    with open("../assets/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Файл стилей assets/style.css не найден. Используются стандартные настройки.")

if "full_history" not in st.session_state:
    st.session_state.full_history = load_history()

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2913/2913520.png", width=80)
    st.title("Настройки")

    api_key = st.secrets.get("GOOGLE_API_KEY") or st.text_input("Gemini API Key", type="password")

    if api_key:
        setup_ai(api_key)
        st.success("✅ API готов к работе")
    else:
        st.warning("⚠️ Введите API Key")

    model_option = st.selectbox("Модель ИИ", ["models/gemini-2.5-flash", "models/gemini-1.5-pro"])

    st.divider()
    if st.button("🗑 Очистить всю историю навсегда"):
        from src.history_manager import clear_history_file

        clear_history_file()
        st.session_state.full_history = []
        st.rerun()

st.title("🌿 Nature Expert AI")
st.markdown("##### *Ваш цифровой полевой дневник: птицы, грибы, минералы*")

tab1, tab2 = st.tabs(["🔍 Новый анализ", "📜 Ваша история и карта"])

with tab1:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("📸 Загрузка объекта")
        uploaded_file = st.file_uploader("Выберите фото (оригинал с GPS приветствуется)...",
                                         type=["jpg", "jpeg", "png"])

        if uploaded_file:
            coords = get_exif_coords(uploaded_file)
            uploaded_file.seek(0)

            img = Image.open(uploaded_file)
            st.image(img, use_container_width=True, caption="Выбранное изображение")
            analyze_btn = st.button("🚀 Запустить анализ ИИ")

    with col2:
        st.subheader("🧠 Вердикт натуралиста")
        if uploaded_file and analyze_btn:
            if not api_key:
                st.error("Пожалуйста, настройте API Key в боковой панели.")
            else:
                with st.spinner("ИИ изучает текстуры и форму..."):
                    try:
                        result_text = get_nature_analysis(model_option, img)

                        st.markdown(f'<div class="result-card">{result_text}</div>', unsafe_allow_html=True)

                        new_entry = {
                            "time": datetime.now().strftime("%H:%M | %d.%m.%Y"),
                            "text": result_text,
                            "image": img,
                            "coords": coords
                        }
                        st.session_state.full_history.append(new_entry)
                        save_history(st.session_state.full_history)

                        if coords:
                            st.success(f"📍 Координаты найдены и сохранены!")
                        else:
                            st.info("ℹ️ В фото нет данных GPS. Карта не будет отображать это место.")

                    except Exception as e:
                        st.error(f"Произошла ошибка: {e}")
        else:
            st.info("Результаты появятся здесь после завершения анализа.")
with tab2:
    if not st.session_state.full_history:
        st.info("Ваша история пока пуста. Проведите свой первый анализ в первой вкладке!")
    else:
        st.subheader("🌍 География ваших находок")

        points_with_gps = [e for e in st.session_state.full_history if e.get("coords")]

        if points_with_gps:
            # Центрируем карту на последней точке
            last_coords = points_with_gps[-1]["coords"]
            m = folium.Map(location=last_coords, zoom_start=6, tiles="OpenStreetMap")

            for entry in points_with_gps:
                lat, lon = entry["coords"]
                try:
                    title = entry["text"].split('\n')[2].replace('**НАЗВАНИЕ:**', '').strip()[:40]
                except:
                    title = "Объект"

                folium.Marker(
                    [lat, lon],
                    popup=f"<i>{title}</i>",
                    tooltip=title,
                    icon=folium.Icon(color='green', icon='leaf')
                ).add_to(m)

            folium_static(m, width=1100)
        else:
            st.warning("На карте нечего показывать: загруженные фото не содержали GPS-данных.")

        st.divider()
        st.subheader("📜 Все записи")

        # Вывод карточек истории от новых к старым
        history_len = len(st.session_state.full_history)
        for i in range(history_len - 1, -1, -1):
            entry = st.session_state.full_history[i]
            has_gps = "📍 GPS" if entry.get("coords") else "⚪ Нет координат"

            with st.expander(f"{entry['time']} — {has_gps}"):
                h_col1, h_col2 = st.columns([1, 2])
                with h_col1:
                    st.image(entry['image'], use_container_width=True)
                with h_col2:
                    st.markdown(f'<div class="result-card">{entry["text"]}</div>', unsafe_allow_html=True)

                    ctrl_col1, ctrl_col2 = st.columns([1, 1])
                    with ctrl_col1:
                        st.download_button(
                            label="📥 Скачать отчет (.txt)",
                            data=entry['text'],
                            file_name=f"analysis_{i}.txt",
                            key=f"dl_{i}"
                        )
                    with ctrl_col2:
                        if st.button(f"🗑 Удалить эту запись", key=f"del_{i}"):
                            st.session_state.full_history.pop(i)
                            save_history(st.session_state.full_history)
                            st.rerun()
st.divider()
st.caption("Nature Expert AI v1.2 | Разработано для исследователей природы. ИИ может ошибаться, будьте внимательны.")