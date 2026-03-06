import streamlit as st
import requests
import base64
import os

st.set_page_config(page_title="ОГЭ по математике с ИИ", layout="wide")
st.title("Подготовка к ОГЭ по математике с ИИ-помощником")

user_task = st.text_area("Введите задачу по математике:", height=150)

if st.button("Решить задачу"):
    if user_task:
        with st.spinner("ИИ думает..."):
            # 1. Декодируем Client ID и Client Secret
            client_credentials_base64 = os.getenv("GIGACHAT_CREDENTIALS", "MDE5Y2MyMDUtOGIwNy03ZGIwLWJiYzgtZDYxNGM2ZWNlMGQ5OmYyODNjMWIyLWVhOGYtNGIyNi05ZTQ2LTgyNDAyYTcxMTJkNg==")
            client_credentials = base64.b64decode(client_credentials_base64).decode("utf-8")
            client_id, client_secret = client_credentials.split(":")

            # 2. Кодируем Client ID:Client Secret в Base64
            auth_string = f"{client_id}:{client_secret}"
            auth_base64 = base64.b64encode(auth_string.encode()).decode()

            # 3. Получаем Access Token
            auth_headers = {
                "Authorization": f"Basic {auth_base64}",
                "Content-Type": "application/x-www-form-urlencoded",
                "RqUID": "your_unique_request_id",
            }
            auth_data = {"scope": "GIGACHAT_API_PERS"}
            auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

            try:
                auth_response = requests.post(auth_url, headers=auth_headers, data=auth_data, verify=False)
                auth_response.raise_for_status()
                access_token = auth_response.json()["access_token"]
            except Exception as e:
                st.error(f"Ошибка при получении токена: {e}")
                st.stop()

            # 4. Отправляем запрос к API Гигachaт
            gigachat_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
            gigachat_data = {
                "model": "GigaChat",
                "messages": [{"role": "user", "content": f"Реши задачу: {user_task}"}],
            }
            gigachat_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

            try:
                response = requests.post(gigachat_url, headers=gigachat_headers, json=gigachat_data, verify=False)
                response.raise_for_status()
                solution = response.json()["choices"][0]["message"]["content"]
                st.success("Решение:")
                st.write(solution)
            except Exception as e:
                st.error(f"Ошибка при запросе к API: {e}")
                st.write("Ответ сервера:", response.text if 'response' in locals() else "Нет ответа")
    else:
        st.warning("Пожалуйста, введите задачу.")


# Пример задачи (для демонстрации)
st.subheader("Пример задачи:")
st.write("""
Решите уравнение: 2x + 5 = 15
""")












