import streamlit as st
from openai import OpenAI

# Инициализация клиента OpenAI
client = OpenAI(
    base_url='http://localhost:1143/v1',
    api_key='llm'
)

# Словарь для выбора модели в зависимости от темы
model_mapping = {
    "Код: Qwen-Coder": "lmstudio-community/Qwen2.5-Coder-7B-Instruct-GGUF/Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf",
    "Текст: Vikhr-Qwen-ru": "lmstudio-community/Qwen2.5-Coder-7B-Instruct-GGUF/Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf",
    "Математика: Qwen-Math": "lmstudio-community/Qwen2.5-Coder-7B-Instruct-GGUF/Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf"
}


def generate_text(prompt, model, max_tokens=200, temperature=0.7, style=None, is_code=False):
    if is_code:
        # Чёткий запрос для генерации только кода
        prompt = f"Напиши только код. Никаких объяснений, комментариев или дополнительного текста:\n{prompt}"
    elif style:
        # Если стиль указан, добавляем его к промту
        prompt = f"Напиши {style}:\n{prompt}"

    response = client.completions.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=0.95
    )
    # Возвращаем текст как есть
    return response.choices[0].text.strip()


st.set_page_config(page_title="ThinkForge", page_icon="🧊", layout="wide")

st.markdown("""
    <style>
    .big-font {
        font-size: 24px !important;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Ассистент Атома")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<p class="big-font">Выберите тему:</p>', unsafe_allow_html=True)
    tema = st.selectbox("", options=["Код: Qwen-Coder", "Текст: Vikhr-Qwen-ru", "Математика: Qwen-Math"], index=0)

    if tema != "Код: Qwen-Coder":
        st.markdown('<p class="big-font">Введите стиль текста:</p>', unsafe_allow_html=True)
        style = st.text_input("",
                              placeholder="Например: статья, пресс-релиз, креативное письмо, математическая формула, алгебраическая задача")
    else:
        style = None

    st.markdown('<p class="big-font">Введите текст (промт):</p>', unsafe_allow_html=True)
    prompt = st.text_area("", value="", height=200)

with col2:
    with st.expander("Настройки генерации", expanded=True):
        max_tokens = st.slider("Максимальное количество токенов:", min_value=50, max_value=2000, value=1800, step=50)
        temperature = st.slider("Температура (креативность):", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

if st.button("Сгенерировать"):
    if not prompt:
        st.error("Введите текст для генерации!")
    else:
        selected_model = model_mapping.get(tema, None)
        if not selected_model:
            st.error(f"Модель для темы '{tema}' не задана!")
        else:
            try:
                with st.spinner('Генерация текста...'):
                    # Если выбран "Код: Qwen-Coder", активируется режим генерации только кода
                    is_code = tema == "Код: Qwen-Coder"
                    generated_text = generate_text(prompt, model=selected_model, max_tokens=max_tokens,
                                                   temperature=temperature, style=style, is_code=is_code)
                st.success("Текст успешно сгенерирован!")
                st.markdown("### Сгенерированный текст:")
                st.text_area("", value=generated_text, height=300)
            except Exception as e:
                st.error(f"Ошибка при генерации текста: {e}")
