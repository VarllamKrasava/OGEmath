import os
import streamlit as st
import requests
import base64
import uuid

# Настройка страницы
st.set_page_config(page_title="Подготовка к экзаменам", layout="wide")

# Инициализация состояния страницы
if 'page' not in st.session_state:
    st.session_state.page = "main"

# Функция для главной страницы
def main_page():
    st.title("Подготовка к экзаменам")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("ЕГЭ"):
            st.session_state.page = "ege"
    with col2:
        if st.button("ОГЭ"):
            st.session_state.page = "oge"
    with col3:
        if st.button("ИИ-помощник"):
            st.session_state.page = "ai_assistant"

# Функция для страницы ЕГЭ
def ege_page():
    st.title("ЕГЭ")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Геометрия"):
            st.session_state.page = "ege_geometry"
    with col2:
        if st.button("Алгебра"):
            st.session_state.page = "ege_algebra"
    if st.button("Назад"):
        st.session_state.page = "main"

# Функция для страницы ОГЭ
def oge_page():
    st.title("ОГЭ")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Геометрия"):
            st.session_state.page = "oge_geometry"
    with col2:
        if st.button("Алгебра"):
            st.session_state.page = "oge_algebra"
    if st.button("Назад"):
        st.session_state.page = "main"

# Функция для страницы ИИ-помощника
def ai_assistant_page():
    st.title("Подготовка к ОГЭ и ЕГЭ по математике с ИИ-помощником")

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

    if st.button("Назад"):
        st.session_state.page = "main"

# Функция для страницы ЕГЭ Геометрия
def ege_geometry_page():
    st.title("ЕГЭ - Геометрия")
    st.write("Задания по геометрии для ЕГЭ:")

    tasks = [
        {"question": "Задача 1: Найдите площадь треугольника...", "answer": "Ответ: 10"},
        {"question": "Задача 2: Найдите длину гипотенузы...", "answer": "Ответ: 5"},
    ]

    for task in tasks:
        with st.expander(task["question"]):
            st.write(task["answer"])

    if st.button("Назад"):
        st.session_state.page = "ege"

# Функция для страницы ЕГЭ Алгебра
def ege_algebra_page():
    st.title("ЕГЭ - Алгебра")
    st.write("Задания по алгебре для ЕГЭ:")

    tasks = [
        {"question": "Задача 1: В кармане у Миши было четыре конфеты  — «Грильяж», «Белочка», «Коровка» и «Ласточка», а также ключи от квартиры. Вынимая ключи, Миша случайно выронил из кармана одну конфету. Найдите вероятность того, что потерялась конфета «Грильяж».", "answer": "Ответ: 0.25"},
        {"question": "Задача 2: Какова вероятность того, что случайно выбранный телефонный номер оканчивается двумя чётными цифрами?", "answer": "Вероятность того, что на одном из требуемых мест окажется чётное число, равна 0,5. Следовательно, вероятность того, что на двух местах одновременно окажутся два чётных числа, равна 0,5 · 0,5  =  0,25.Ответ: 0.25"},
    ]

    for task in tasks:
        with st.expander(task["question"]):
            st.write(task["answer"])

    if st.button("Назад"):
        st.session_state.page = "ege"

# Функция для страницы ОГЭ Геометрия
def oge_geometry_page():
    st.title("ОГЭ - Геометрия")
    st.write("Задания по геометрии для ОГЭ:")

    tasks = [
        {"question": "Задача 1: В треугольнике два угла равны 54° и 58°. Найдите его третий угол. Ответ дайте в градусах.", "answer": "Ответ: 68°"},
        {"question": "Задача 2: В равнобедренном треугольнике ABC с основанием AC внешний угол при вершине C равен 123°. Найдите величину угла ABC. Ответ дайте в градусах.", "answer": "Ответ: 66°"},
    ]

    for task in tasks:
        with st.expander(task["question"]):
            st.write(task["answer"])

    if st.button("Назад"):
        st.session_state.page = "oge"

# Функция для страницы ОГЭ Алгебра
def oge_algebra_page():
    st.title("ОГЭ - Алгебра")
    st.write("Задания по алгебре для ОГЭ:")

    tasks = [
        {"question": "Задача 1: Решите уравнение 10(x-9)=7", "answer": "Ответ: 9.7"},
        {"question": "Задача 2: Найдите значение выражения 3,8 + 2,9.", "answer": "Ответ: 6.7"},
    ]

    for task in tasks:
        with st.expander(task["question"]):
            st.write(task["answer"])

    if st.button("Назад"):
        st.session_state.page = "oge"

# Основной блок управления страницами
if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "ege":
    ege_page()
elif st.session_state.page == "oge":
    oge_page()
elif st.session_state.page == "ai_assistant":
    ai_assistant_page()
elif st.session_state.page == "ege_geometry":
    ege_geometry_page()
elif st.session_state.page == "ege_algebra":
    ege_algebra_page()
elif st.session_state.page == "oge_geometry":
    oge_geometry_page()
elif st.session_state.page == "oge_algebra":
    oge_algebra_page()
