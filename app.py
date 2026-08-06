import streamlit as st
from g4f.client import Client
from PIL import Image

# Настройки страницы
st.set_page_config(page_title="Zenbot", page_icon="🤖")

# Заголовок
st.title("🤖 Zenbot")
st.caption("Персональный веб-бот от Зеникса (Ильхана)")

client = Client()

# Системная инструкция
SYSTEM_PROMPT = {
    "role": "system",
    "content": "Тебя зовут Zenbot. Ты полезный, умный и дружелюбный ИИ-ассистент. Твой создатель и разработчик — Зеникс (Ильхан). Если тебя спрашивают, кто тебя создал или кто твой разработчик, всегда отвечай, что тебя создал Зеникс (Ильхан)."
}

# История сообщений
if "messages" not in st.session_state:
    st.session_state.messages = [
        SYSTEM_PROMPT,
        {"role": "assistant", "content": "Привет! Я Zenbot. Чем могу помочь? Можешь прикрепить фото в боковой панели и нажать 'Отправить фото', или просто задать вопрос!"}
    ]

# Вывод истории сообщений
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            if msg.get("content"):
                st.markdown(msg["content"])
            if msg.get("image_display"):
                st.image(msg["image_display"], use_container_width=True)

# Загрузка картинки в БОКОВОЙ ПАНЕЛИ
with st.sidebar:
    st.header("Вложения")
    uploaded_file = st.file_uploader("Прикрепить фото к сообщению:", type=["png", "jpg", "jpeg", "webp"])
    
    # Кнопка для отправки ТОЛЬКО фото
    submit_photo = st.button("Отправить фото")

# --- ЛОГИКА ОБРАБОТКИ ---

final_prompt = None
final_image = None

# Сценарий 1: Пользователь нажал кнопку "Отправить фото"
if submit_photo and uploaded_file:
    final_prompt = "Опиши это изображение"
    final_image = uploaded_file

# Сценарий 2: Пользователь ввел текст
elif prompt := st.chat_input("Напиши что-нибудь..."):
    final_prompt = prompt
    if uploaded_file:
        final_image = uploaded_file

# --- ЕСЛИ ЕСТЬ ОТПРАВКА ---
if final_prompt:
    user_msg = {"role": "user", "content": final_prompt}
    
    if final_image:
        img_for_display = Image.open(final_image)
        user_msg["image_display"] = img_for_display
        
    st.session_state.messages.append(user_msg)
    
    with st.chat_message("user"):
        st.markdown(final_prompt)
        if final_image:
            st.image(final_image, use_container_width=True)

    with st.chat_message("assistant"):
        with st.spinner("Анализирую..."):
            try:
                api_messages = []
                for m in st.session_state.messages:
                    if m["role"] == "system":
                        api_messages.append({"role": "system", "content": m["content"]})
                    elif m.get("content"):
                        api_messages.append({"role": m["role"], "content": m["content"]})

                response = client.chat.completions.create(
                    model="gemini",
                    messages=api_messages,
                    image=final_image if final_image else None
                )
                
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
                st.rerun()

            except Exception as e:
                st.error(f"Ошибка при обработке: {e}")