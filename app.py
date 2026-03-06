import streamlit as st
import requests
import os

st.set_page_config(page_title="ОГЭ по математике с ИИ", layout="wide")
st.title("Подготовка к ОГЭ по математике с ИИ-помощником")

user_task = st.text_area("Введите задачу по математике:", height=150)

if st.button("Решить задачу"):
    if user_task:
        with st.spinner("ИИ думает..."):
            api_key = os.getenv("GIGACHAT_API_KEY")  # Убедитесь, что ключ чистый (без кодирования)
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "GigaChat",
                "messages": [{"role": "user", "content": f"Реши задачу: {user_task}"}]
            }

            try:
                response = requests.post(
                    "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
                    headers=headers,
                    json=data,
                    verify=False,
                    timeout=10
                )
                response.raise_for_status()
                st.write("Полный ответ API:", response.json())  # Для отладки
                solution = response.json()["choices"][0]["message"]["content"]
                st.success("Решение:")
                st.write(solution)
            except Exception as e:
                st.error(f"Ошибка: {e}")

# Пример задачи (для демонстрации)
st.subheader("Пример задачи:")
st.write("""
Решите уравнение: 2x + 5 = 15
""")











