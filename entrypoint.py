import streamlit as st

# Настройка страницы должна быть первой командой Streamlit
st.set_page_config(page_title="Nature Expert AI Hub", page_icon="🌿", layout="wide")

# Удаляем стандартные отступы сверху для красоты
st.markdown("""
    <style>
        .block-container {padding-top: 2rem;}
    </style>
""", unsafe_allow_html=True)

# Сайдбар для выбора версии
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2913/2913520.png", width=80)
    st.title("Управление версиями")

    app_mode = st.radio(
        "Выберите версию приложения:",
        ["Версия 1.0 (Базовая)", "Версия 2.0 (Продвинутая)"],
        help="v1.0 — легкий интерфейс. v2.0 — история, карты и расширенный анализ."
    )

    st.divider()
    st.info("Вы переключаетесь между разными этапами разработки проекта.")

# Логика запуска
if app_mode == "Версия 1.0 (Базовая)":
    st.title("📜 Nature Expert v1.0")
    # Выполняем код из main.py
    try:
        with open("version/main.py", encoding="utf-8") as f:
            exec(f.read())
    except FileNotFoundError:
        st.error("Файл main.py не найден в корневой папке.")

else:
    # Здесь мы запускаем твой новый app.py
    # Важно: В самом app.py нужно будет убрать или закомментировать st.set_page_config,
    # так как она уже вызвана здесь, в entrypoint.py
    try:
        with open("version/app.py", encoding="utf-8") as f:
            exec(f.read())
    except FileNotFoundError:
        st.error("Файл app.py не найден в корневой папке.")