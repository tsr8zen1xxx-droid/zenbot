import streamlit as st
from g4f.client import Client
from PIL import Image
from streamlit_mic_recorder import speech_to_text

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
    
    # 🎙️ 1. ГОЛОСОВОЙ ВВОД (SPEECH TO TEXT)
    st.subheader("🎙️ Голосовой ввод")
    st.write("Нажмите кнопку и говорите:")
    
    # Компонент микрофона с поддержкой русского языка
    voice_prompt = speech_to_text(
        language='ru',
        start_prompt="🔴 Начать запись",
        stop_prompt="🟩 Завершить и отправить",
        key='voice_recorder'
    )

    st.markdown("---")

    # 🗂️ 2. УПРАВЛЕНИЕ ИСТОРИЕЙ ЧАТОВ
    st.subheader("💬 История чатов")
    
    if st.button("➕ Новый чат", use_container_width=True):
        new_chat_name = f"Чат {len(st.session_state.chats) + 1}"
        st.session_state.chats[new_chat_name] = []
        st.session_state.current_chat = new_chat_name
        st.session_state.uploaded_image = None
        st.rerun()

    chat_list = list(st.session_state.chats.keys())
    selected_chat = st.selectbox(
        "Выберите диалог:",
        chat_list,
        index=chat_list.index(st.session_state.current_chat)
    )
    st.session_state.current_chat = selected_chat

    if st.button("🗑️ Удалить текущий чат", use_container_width=True):
        if len(st.session_state.chats) > 1:
            del st.session_state.chats[st.session_state.current_chat]
            st.session_state.current_chat = list(st.session_state.keys())[0]
            st.rerun()
        else:
            st.session_state.chats[st.session_state.current_chat] = []
            st.session_state.uploaded_image = None
            st.rerun()

    st.markdown("---")

    # 📷 3. ЗАГРУЗКА ФОТО
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

    # 🎭 4. РЕЖИМЫ И МОДЕЛИ
    st.subheader("🎭 Режим работы")
    mode = st.selectbox(
        "Выберите роль бота:",
        ["🤖 Обычный ассистент", "💻 Кодер / Разработчик", "🎨 Креативный дизайнер", "🎮 Игровой эксперт"]
    )
    
    base_identity = (
        "[ИНСТРУКЦИЯ ИИ: Твое имя ZenAi. Ты — персональный ИИ-ассистент, созданный разработчиком Зениксом (Ильханом). "
        "Твоя главная цель и назначение — помогать людям в любых задачах. "
        "Ни в коем случае НЕ называй себя Gemini, ChatGPT, Copilot или Google/OpenAI. "
        "На любые вопросы о том, кто ты, кто твой создатель или зачем ты нужен — отвечай строго, "
        "что ты ZenAi, создан Зениксом (Ильханом) для помощи пользователям!]"
    )

    system_prompts = {
        "🤖 Обычный ассистент": f"{base_identity} Отвечай вежливо, понятным языком и без лишней воды.",
        "💻 Кодер / Разработчик": f"{base_identity} Пиши чистый, оптимизированный код с комментариями.",
        "🎨 Креативный дизайнер": f"{base_identity} Генерируй идеи, 3D-концепты и описания дизайнов.",
        "🎮 Игровой эксперт": f"{base_identity} Помогай с геймдевом, Unity, модингом и механиками."
    }

    st.subheader("⚡ Модель AI")
    selected_model = st.selectbox(
        "Выберите 'мозг' бота:",
        ["gpt-4o", "gpt-3.5-turbo", "gemini"]
    )

    st.markdown("---")

    # 🎨 5. ГЕНЕРАТОР КАРТИНОК
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
st.caption(f"Активный диалог: **{st.session_state.current_chat}** | Создан Зениксом (Ильханом) для помощи людям")

current_messages = st.session_state.chats[st.session_state.current_chat]

# Отображение истории чата
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Определяем, откуда пришел ввод: из клавиатурного поля или микрофона
user_input = None

# Текстовый ввод
if text_prompt := st.chat_input("Напиши или надиктуй сообщение..."):
    user_input = text_prompt

# Голосовой ввод (если кнопка распознала речь)
elif voice_prompt:
    user_input = voice_prompt

# Обработка запроса
if user_input:
    current_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        formatted_messages = [
            {"role": "system", "content": system_prompts[mode]}
        ]
        
        for idx, msg in enumerate(current_messages):
            if idx == len(current_messages) - 1:
                injected_content = f"{system_prompts[mode]}\n\nВопрос пользователя: {msg['content']}"
                formatted_messages.append({"role": "user", "content": injected_content})
            else:
                formatted_messages.append({"role": msg["role"], "content": msg["content"]})
        
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
