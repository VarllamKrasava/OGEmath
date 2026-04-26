import streamlit as st

st.title("Hello, Railway!")
st.write("Приложение успешно запущено.")

import requests
import base64
import uuid
import os

# Настройки страницы
st.set_page_config(page_title="ОГЭ по математике с ИИ", layout="wide")
st.title("Подготовка к ОГЭ по математике с ИИ-помощником")

# Поле для ввода задачи
user_task = st.text_area("Введите задачу по математике:", height=150)

if st.button("Решить задачу"):
    if user_task:
        with st.spinner("ИИ думает..."):
            # 1. Декодируем Client ID и Client Secret из переменной окружения
            client_credentials_base64 = os.getenv(
                "GIGACHAT_CREDENTIALS",
                "MDE5Y2MyMDUtOGIwNy03ZGIwLWJiYzgtZDYxNGM2ZWNlMGQ5OmYyODNjMWIyLWVhOGYtNGIyNi05ZTQ2LTgyNDAyYTcxMTJkNg=="
            )
            client_credentials = base64.b64decode(client_credentials_base64).decode("utf-8")
            client_id, client_secret = client_credentials.split(":")

            # 2. Кодируем Client ID:Client Secret в Base64 для заголовка Authorization
            auth_string = f"{client_id}:{client_secret}"
            auth_base64 = base64.b64encode(auth_string.encode()).decode()

            # 3. Генерируем уникальный RqUID
            rquid = str(uuid.uuid4())

            # 4. Заголовки для запроса токена
            auth_headers = {
                "Authorization": f"Basic {auth_base64}",
                "Content-Type": "application/x-www-form-urlencoded",
                "RqUID": rquid,
            }

            # 5. Тело запроса для получения токена
            auth_data = "scope=GIGACHAT_API_PERS"

            # 6. Эндпоинт для получения токена
            auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

            # 7. Получаем Access Token
            try:
                auth_response = requests.post(
                    auth_url,
                    headers=auth_headers,
                    data=auth_data,
                    verify=False
                )
                auth_response.raise_for_status()
                access_token = auth_response.json()["access_token"]
            except Exception as e:
                st.error(f"Ошибка при получении токена: {e}")
                st.write("Ответ сервера:", auth_response.text if 'auth_response' in locals() else "Нет ответа")
                st.stop()

            # 8. Заголовки для запроса к API Гигachaт
            gigachat_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "RqUID": rquid,
            }

            # 9. Тело запроса к API Гигachaт
            gigachat_data = {
                "model": "GigaChat",
                "messages": [
                    {
                        "role": "system",
                        "content": """
                        Ты — эксперт по математике и помощник для подготовки к ОГЭ.
                        Решай задачи подробно, с пояснениями каждого шага.
                        Если в задаче требуется числовой ответ, давай его в десятичной дроби.
                        Если задача не имеет решения, объясни почему.
                        """
                    },
                    {
                        "role": "user",
                        "content": f"Реши задачу: {user_task}"
                    }
                ],
                "temperature": 0.7,
            }

            # 10. Эндпоинт API Гигachaт
            gigachat_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

            # 11. Отправляем запрос к API Гигachaт
            try:
                response = requests.post(
                    gigachat_url,
                    headers=gigachat_headers,
                    json=gigachat_data,
                    verify=False
                )
                response.raise_for_status()
                solution = response.json()["choices"][0]["message"]["content"]
                st.success("Решение:")
                st.write(solution)
            except Exception as e:
                st.error(f"Ошибка при запросе к API: {e}")
                st.write("Ответ сервера:", response.text if 'response' in locals() else "Нет ответа")
    else:
        st.warning("Пожалуйста, введите задачу.")

# Пример задачи
st.subheader("Пример задачи:")
st.write("Решите уравнение: 2x + 5 = 15")
st.subheader("Примечание:")
st.write("Для того что бы ответ получить в таком формате -3.72")
st.write('Необходимо написать "Дай ответ в десятичной дроби"')
