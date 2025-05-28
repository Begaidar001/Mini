import streamlit as st
import random
import time
from PIL import Image

# --- Настройки страницы ---
st.set_page_config(page_title="🎰 Мини Лото Казино", layout="centered")

# --- Установка фонового изображения (локальный файл) ---
def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded = image.read()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded.encode('base64').decode()}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("i.webp")

# --- Инициализация сессии ---
if "balance" not in st.session_state:
    st.session_state.balance = 1000
if "history" not in st.session_state:
    st.session_state.history = []

# --- Заголовок и вход ---
st.title("🎰 Мини Лото Казино")
code_input = st.text_input("🔐 Введите код доступа:", type="password")
if code_input != "1234":
    st.warning("Введите верный код.")
    st.stop()
else:
    st.success("Добро пожаловать!")

st.markdown(f"### 💳 Баланс: **{st.session_state.balance}₸**")

# --- Интерфейс игры ---
st.header("📋 Ставка и выбор чисел")
bet = st.number_input("💰 Ставка (₸):", min_value=10, max_value=st.session_state.balance, step=10)
user_numbers = st.multiselect("🎯 Выберите 5 чисел от 1 до 20:", list(range(1, 21)), max_selections=5)

# --- Кнопка запуска ---
if st.button("🎲 Крутить барабаны!"):
    if len(user_numbers) != 5:
        st.error("Нужно выбрать ровно 5 чисел.")
    else:
        st.session_state.balance -= bet
        winning_numbers = []

        st.subheader("🎡 Вращение барабанов...")
        with st.container():
            bar_cols = st.columns(5)
            for i in range(5):
                with bar_cols[i]:
                    st.markdown("#### 🎰")
                    num = random.randint(1, 20)
                    time.sleep(0.3)
                    winning_numbers.append(num)
                    st.markdown(f"<h2 style='text-align:center;color:#FFD700'>{num}</h2>", unsafe_allow_html=True)

        # Подсчет совпадений
        matches = set(user_numbers) & set(winning_numbers)
        match_count = len(matches)
        combo_map = {
            0: ("❌ Нет совпадений", 0),
            1: ("⚪ 1 совпадение", 0),
            2: ("🟡 2 совпадения", 0),
            3: ("🟢 3 совпадения (x2)", 2),
            4: ("🔵 4 совпадения (x5)", 5),
            5: ("🟣 Джекпот! 5 совпадений (x10)", 10),
        }
        combo_name, multiplier = combo_map[match_count]
        win_amount = bet * multiplier
        st.session_state.balance += win_amount

        st.subheader("📊 Результаты:")
        st.markdown(f"**Выигрышные числа:** `{sorted(winning_numbers)}`")
        st.markdown(f"**Ваши числа:** `{sorted(user_numbers)}`")
        st.markdown(f"**Совпадения:** {match_count} — {combo_name}")
        if win_amount > 0:
            st.success(f"🎉 Вы выиграли {win_amount} ₸!")
        else:
            st.error("😢 Увы, ничего не выиграно.")

        # История
        st.session_state.history.insert(0, {
            "ставка": bet,
            "ваши": sorted(user_numbers),
            "выпали": sorted(winning_numbers),
            "совпадения": match_count,
            "комбинация": combo_name,
            "выигрыш": win_amount
        })

        st.markdown(f"### 💳 Новый баланс: **{st.session_state.balance}₸**")

# --- История ставок ---
with st.expander("🧾 История ставок"):
    if not st.session_state.history:
        st.info("История пока пуста.")
    else:
        for h in st.session_state.history[:5]:
            st.markdown(f"""
            - 🎯 Ваши: {h['ваши']}
            - 🎰 Выпали: {h['выпали']}
            - ✅ Совпадения: {h['совпадения']} ({h['комбинация']})
            - 💸 Выигрыш: {h['выигрыш']} ₸
            - 💵 Ставка: {h['ставка']} ₸
            ---
            """)

st.caption("© 2025 Мини Лото Казино")
