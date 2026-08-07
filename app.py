import streamlit as st
from g4f.client import Client
from PIL import Image
import io

# Настройка страницы
st.set_page_config(
    page_title="ZenAi",
    page_icon="🤖",
    layout="wide"
)

# Инициализация AI-клиента
client = Client()

# --- ИНИЦИАЛИЗА СЕССИИ И ИСТОРИИ ЧАТОВ ---
if "chats" not in st.session_state:
    # Структура: {"Чат 1": [сообщения], "Чат 2": [сообщения]}
    st.session_state.chats = {"Чат 1": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Чат 1"

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None


# --- БОКОВАЯ ПАНЕЛЬ (SIDEBAR) ---
with st.sidebar:
    st.title("⚙️ Настройки ZenAi")
    st.write("Персональный веб-бот от Зеникса (Ильхана)")
    
    st.markdown("---")
    
    # 🗂️ 1. УПРАВЛЕНИЕ ИСТОРИЕЙ ЧАТОВ
    st.subheader("💬 История чатов")
    
    # Кнопка создания нового чата
    if st.button("➕ Новый чат", use_container_width=True):
        new_chat_name = f"Чат {len(st.session_state.chats) + 1}"
        st.session_state.chats[new_chat_name] = []
        st.session_state.current_chat = new_chat_name
        st.session_state.uploaded_image = None
        st.rerun()

    # Выбор активного чата из списка
    chat_list = list(st.session_state.chats.keys())
    selected_chat = st.selectbox(
        "Выберите диалог:",
        chat_list,
        index=chat_list.index(st.session_state.current_chat)
    )
    st.session_state.current_chat = selected_chat

    # Удаление текущего чата
    if st.button("🗑️ Удалить текущий чат", use_container_width=True):
        if len(st.session_state.chats) > 1:
            del st.session_state.chats[st.session_state.current_chat]
            st.session_state.current_chat = list(st.session_state.chats.keys())[0]
            st.rerun()
        else:
            st.session_state.chats[st.session_state.current_chat] = []
            st.session_state.uploaded_image = None
            st.rerun()

    st.markdown("---")

    # 📷 2. ЗАГРУЗКА И АНАЛИЗ ФОТО
    st.subheader("🖼️ Прикрепить фото")
    uploaded_file = st.file_uploader(
        "Загрузите изображение для анализа:",
        type=["png", "jpg", "jpeg", "webp"]
    )
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Загруженное фото", use_container_width=True)
        st.session_state.uploaded_image = image
    else:
        st.session_state.uploaded_image = None

    st.markdown("---")

    # 🎭 3. РЕЖИМЫ И МОДЕЛИ
    st.subheader("🎭 Режим работы")
    mode = st.selectbox(
        "Выберите роль бота:",
        ["🤖 Обычный ассистент", "💻 Кодер / Разработчик", "🎨 Креативный дизайнер", "🎮 Игровой эксперт"]
    )
    
    system_prompts = {
        "🤖 Обычный ассистент": "Ты — ZenAi, персональный веб-бот, созданный Зениксом (Ильханом). На вопрос 'кто ты' или 'кто твой создатель' всегда отвечай, что ты ZenAi от Зеникса (Ильхана). Отвечай четко, понятным языком и без лишней воды.",
        "💻 Кодер / Разработчик": "Ты — ZenAi, ассистент-кодер, созданный Зениксом (Ильханом). Пиши чистый, оптимизированный код с подробными комментариями.",
        "🎨 Креативный дизайнер": "Ты — ZenAi, креативный дизайнер, созданный Зениксом (Ильханом). Генерируй концепт-идеи, описания 3D-моделей, скинов и UI-интерфейсов.",
        "🎮 Игровой эксперт": "Ты — ZenAi, эксперт по геймдеву, модингу и играм, созданный Зениксом (Ильханом). Помогай с разбором механик, Unity и разработкой игр."
    }

    st.subheader("⚡ Модель AI")
    selected_model = st.selectbox(
        "Выберите 'мозг' бота:",
        ["gpt-4o", "gpt-3.5-turbo", "gemini"]
    )

    st.markdown("---")

    # 🎨 4. ГЕНЕРАТОР КАРТИНОК ПО ОПИСАНИЮ
    st.subheader("✨ Генератор изображений")
    image_prompt = st.text_input("Опишите картинку (на англ.):", placeholder="Cyberpunk neon city...")
    if st.button("🎨 Сгенерировать картинку", use_container_width=True):
        if image_prompt:
            with st.spinner("Рисую..."):
                clean_prompt = image_prompt.replace(" ", "%20")
                img_url = f"https://pollinations.ai/p/{clean_prompt}?width=800&height=800&seed=42"
                st.image(img_url, caption=f"Результат: {image_prompt}", use_container_width=True)
        else:
            st.warning("Введите описание картинки!")


# --- ОСНОВНОЙ ИНТЕРФЕЙС ---
st.title("🤖 ZenAi")
st.caption(f"Активный диалог: **{st.session_state.current_chat}** | Персональная нейросеть от Зеникса (Ильхана)")

# Получаем сообщения для текущего диалога
current_messages = st.session_state.chats[st.session_state.current_chat]

# Отображение истории выбранного чата
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Поле ввода сообщения
if prompt := st.chat_input("Напиши что-нибудь..."):
    # Добавляем сообщение пользователя
    current_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Генерация ответа
    with st.chat_message("assistant"):
        formatted_messages = [{"role": "system", "content": system_prompts[mode]}]
        for msg in current_messages:
            formatted_messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Уведомление, если прикреплено фото
        if st.session_state.uploaded_image:
            st.info("🖼️ Изображение прикреплено к запросу.")

        try:
            response_stream = client.chat.completions.create(
                model=selected_model,
                messages=formatted_messages,
                stream=True
            )
            
            def stream_parser():
                for chunk in response_stream:
                    if hasattr(chunk.choices[0].delta, 'content'):
                        content = chunk.choices[0].delta.content
                        if content:
                            yield content

            full_response = st.write_stream(stream_parser)
            current_messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Ошибка при связи с сервером: {e}")
