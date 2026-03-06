import streamlit as st
import requests
import os

# Настройки страницы
st.set_page_config(page_title="ОГЭ по математике с ИИ", layout="wide")

# Заголовок
st.title("Подготовка к ОГЭ по математике с ИИ-помощником")

# Поле для ввода задачи
user_task = st.text_area("Введите задачу по математике:", height=150)

# Кнопка отправки
if st.button("Решить задачу"):
    if user_task:
        with st.spinner("ИИ думает..."):
            # Вызов API ИИ-помощника
            api_key = os.getenv("AI_API_KEY")  # Замените на ваш ключ
            headers = {"Authorization": f"Bearer {api_key}"}
            data = {"prompt": f"Реши задачу: {user_task}"}

            try:
                response = requests.post(
                    "https://api.example.com/v1/ai/solve",
                    headers=headers,
                    json=data
                )
                response.raise_for_status()
                solution = response.json().get("solution", "Решение не найдено")
                st.success("Решение:")
                st.write(solution)
            except Exception as e:
                st.error(f"Ошибка: {e}")
    else:
        st.warning("Пожалуйста, введите задачу.")

# Пример задачи (для демонстрации)
st.subheader("Пример задачи:")
st.write("""
Решите уравнение: 2x + 5 = 15
""")

