import streamlit as st
import random
import base64

# --- Настройки страницы ---
st.set_page_config(page_title="🎰 Мини Лото Казино", layout="centered")

# --- Вставленный фон (без файла) ---
encoded_bg = """
iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAYAAAA+5YQ6AAAACXBIWXMAAAsTAAALEwEAmpwYAAA
AGXRFWHRTb2Z0d2FyZQBwYWludC5uZXQgNC4wLjEyMTcw9LrkAAAEdElEQVR4nO3dMQ0AAAzDsP3
TbQ43hAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADgb7wABEGH/tDAAAAAElFTkSuQmCC
"""
# --- Установка фонового изображения ---
def set_background(encoded_img):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_img}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background(encoded_bg)

# --- Простой интерфейс игры ---
st.title("🎰 Мини Лото Казино")

if "balance" not in st.session_state:
    st.session_state.balance = 1000
if "history" not in st.session_state:
    st.session_state.history = []

code = st.text_input("🔐 Введите код доступа>1234:", type="password")
if code != "1234":
    st.warning("❌ Неверный код")
    st.stop()

st.success("Добро пожаловать в казино мини-лото!")
st.markdown(f"💳 **Баланс: {st.session_state.balance} ₸**")

st.subheader("📝 Сделайте ставку и выберите 5 чисел")
bet = st.number_input("💰 Ваша ставка (₸):", min_value=10, max_value=500, step=10)
numbers = st.multiselect("🔢 Выберите 5 уникальных чисел от 1 до 20:", list(range(1, 21)), max_selections=5)

if st.button("🎲 Играть!"):
    if st.session_state.balance < bet:
        st.error("Недостаточно баланса!")
    elif len(numbers) != 5:
        st.warning("Пожалуйста, выберите ровно 5 чисел!")
    else:
        draw = random.sample(range(1, 21), 5)
        matches = len(set(numbers) & set(draw))

        # Выплата по совпадениям
        win_table = {5: 20, 4: 10, 3: 5}
        multiplier = win_table.get(matches, 0)
        win = bet * multiplier

        st.session_state.balance += win - bet
        st.session_state.history.append((numbers, draw, matches, win - bet))

        st.markdown("## 🎉 Результаты:")
        st.write(f"🎯 Ваши числа: {numbers}")
        st.write(f"🎰 Выпавшие числа: {draw}")
        st.success(f"🔗 Совпадений: {matches} — {'+' if win - bet >= 0 else ''}{win - bet} ₸")

# История ставок
if st.session_state.history:
    st.subheader("📜 История игр")
    for i, (nums, res, match, change) in enumerate(reversed(st.session_state.history[-5:])):
        st.markdown(f"**#{len(st.session_state.history)-i}** — 🎯 Числа: {nums}, 🎰 Выпали: {res}, ✅ Совпадения: {match}, 💸 Изменение: {'+' if change>=0 else ''}{change} ₸")
