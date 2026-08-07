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
    st.title("🤖 ZenAi Studio")
    st.caption("Создатель: Зеникс (Ильхан)")
    
    st.markdown("---")
    
    # 🎨 1. КАСТОМИЗАЦИЯ ИНТЕРФЕЙСА
    st.subheader("🎨 Тема оформления")
    selected_theme = st.selectbox(
        "Выберите стиль:",
        ["Dark Zen", "Cyberpunk", "Light Minimal"],
        key="theme_selector"
    )

    st.markdown("---")

    # 🎙️ 2. ГОЛОСОВОЙ ВВОД
    st.subheader("🎙️ Голосовой ввод")
    voice_prompt = speech_to_text(
        language='ru',
        start_prompt="🔴 Начать запись",
        stop_prompt="🟩 Завершить и отправить",
        key='voice_recorder'
    )

    st.markdown("---")

    # 🗂️ 3. ИСТОРИЯ ЧАТОВ
    st.subheader("💬 История чатов")
    
    if st.button("➕ Новый чат", use_container_width=True):
        new_chat_name = f"Чат {len(st.session_state.chats) + 1}"
        st.session_state.chats[new_chat_name] = []
        st.session_state.current_chat = new_chat_name
        st.session_state.uploaded_image = None
        st.rerun()

    chat_list = list(st.session_state.chats.keys())
    
    if st.session_state.current_chat not in chat_list:
        st.session_state.current_chat = chat_list[0]

    selected_chat = st.selectbox(
        "Выберите диалог:",
        chat_list,
        index=chat_list.index(st.session_state.current_chat)
    )
    st.session_state.current_chat = selected_chat

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

    # 📷 4. ЗАГРУЗКА ФОТО
    st.subheader("🖼️ Прикрепить фото")
    uploaded_file = st.file_uploader(
        "Загрузите фото:",
        type=["png", "jpg", "jpeg", "webp"]
    )
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Загруженное фото", use_container_width=True)
        st.session_state.uploaded_image = image
    else:
        st.session_state.uploaded_image = None

    st.markdown("---")

    # 🎭 5. РЕЖИМЫ И МОДЕЛИ
    st.subheader("🎭 Режим работы")
    mode = st.selectbox(
        "Выберите роль бота:",
        ["🤖 Обычный ассистент", "💻 Кодер / Разработчик", "🎨 Креативный дизайнер", "🎮 Игровой эксперт"]
    )
    
    base_identity = (
        "[ИНСТРУКЦИЯ ИИ: Твое имя ZenAi. Ты — персональный ИИ-ассистент, созданный разработчиком Зениксом (Ильханом). "
        "Твоя главная цель — помогать людям в любых задачах. "
        "Ни в коем случае НЕ называй себя Gemini, ChatGPT, Copilot или Google/OpenAI. "
        "На любые вопросы о том, кто ты или кто твой создатель — отвечай строго, "
        "что ты ZenAi, создан Зениксом (Ильханом) для помощи пользователям!]"
    )

    system_prompts = {
        "🤖 Обычный ассистент": f"{base_identity} Отвечай вежливо и понятно.",
        "💻 Кодер / Разработчик": f"{base_identity} Пиши чистый код с комментариями.",
        "🎨 Креативный дизайнер": f"{base_identity} Генерируй идеи, 3D-концепты и описания дизайнов.",
        "🎮 Игровой эксперт": f"{base_identity} Помогай с геймдевом, Unity, модингом и механиками."
    }

    selected_model = st.selectbox(
        "Выберите 'мозг' бота:",
        ["gpt-4o", "gpt-3.5-turbo", "gemini"]
    )

    st.markdown("---")

    # 🎨 6. ГЕНЕРАТОР КАРТИНОК
    st.subheader("✨ Генерация изображений")
    image_prompt = st.text_input("Опишите картинку (на англ.):", placeholder="Cyberpunk neon city...")
    if st.button("🎨 Сгенерировать", use_container_width=True):
        if image_prompt:
            with st.spinner("Рисую..."):
                clean_prompt = image_prompt.replace(" ", "%20")
                img_url = f"https://pollinations.ai/p/{clean_prompt}?width=800&height=800&seed=42"
                st.image(img_url, caption=f"Результат: {image_prompt}", use_container_width=True)
        else:
            st.warning("Введите описание картинки!")


# --- ПРИМЕНЕНИЕ СТИЛЕЙ СРАЗУ ПОСЛЕ ВЫБОРА ТЕМЫ ---
if selected_theme == "Cyberpunk":
    st.markdown("""
        <style>
        .stApp { background-color: #0d0221 !important; color: #00f0ff !important; }
        [data-testid="stSidebar"] { background-color: #1a0840 !important; }
        </style>
    """, unsafe_allow_html=True)
elif selected_theme == "Dark Zen":
    st.markdown("""
        <style>
        .stApp { background-color: #0e1117 !important; color: #ffffff !important; }
        [data-testid="stSidebar"] { background-color: #262730 !important; }
        </style>
    """, unsafe_allow_html=True)
elif selected_theme == "Light Minimal":
    st.markdown("""
        <style>
        .stApp { background-color: #f8f9fa !important; color: #212529 !important; }
        [data-testid="stSidebar"] { background-color: #e9ecef !important; }
        </style>
    """, unsafe_allow_html=True)


# --- ОСНОВНОЙ ИНТЕРФЕЙС И АВАТАРКИ ---
st.title("🤖 ZenAi")
st.caption(f"Активный диалог: **{st.session_state.current_chat}** | Создан Зениксом (Ильханом) для помощи людям")

current_messages = st.session_state.chats[st.session_state.current_chat]

# Отображение истории
for message in current_messages:
    avatar_icon = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

user_input = None

if text_prompt := st.chat_input("Напиши или надиктуй сообщение..."):
    user_input = text_prompt
elif voice_prompt:
    user_input = voice_prompt

# Обработка запроса
if user_input:
    current_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🤖"):
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
