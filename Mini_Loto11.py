import streamlit as st
import random

# --- Настройки ---
ACCESS_CODE = "1234"

# --- Конфигурация страницы ---
st.set_page_config(page_title="Мини Лото", page_icon="🎰", layout="centered")

# --- Стилизация через CSS ---
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff6b6b;
    }
    </style>
""", unsafe_allow_html=True)

# --- Заголовок ---
st.title("🎰 Мини Лото")
st.caption("Сделай ставку, выбери числа и проверь свою удачу!")

# --- Доступ по коду ---
with st.expander("🔐 Вход по коду", expanded=True):
    code_input = st.text_input("Введите код доступа>1234:", type="password")
    if code_input != ACCESS_CODE:
        st.warning("🚫 Неверный код. Введите корректный код для продолжения.")
        st.stop()
    else:
        st.success("✅ Доступ разрешён!")

# --- Ставка и выбор чисел ---
st.header("📋 Ввод данных")

col1, col2 = st.columns([1, 2])
with col1:
    bet = st.number_input("💰 Ставка (только целые):", min_value=1, step=1)
with col2:
    user_numbers = st.multiselect("🎯 Выберите 5 уникальных чисел от 1 до 20:",
                                   options=list(range(1, 21)),
                                   max_selections=5)

# --- Запуск игры ---
if st.button("🎲 Играть!"):
    if len(user_numbers) != 5:
        st.error("❗ Нужно выбрать ровно 5 уникальных чисел.")
    else:
        winning_numbers = random.sample(range(1, 21), 5)
        matches = set(user_numbers) & set(winning_numbers)
        num_matches = len(matches)

        st.subheader("📊 Результаты игры")
        st.markdown(f"**🎟️ Ваши числа:** {sorted(user_numbers)}")
        st.markdown(f"**🌀 Выпавшие числа:** {sorted(winning_numbers)}")
        st.markdown(f"**✅ Совпадения:** {sorted(matches) if matches else 'Нет'}")

        multiplier = {3: 2, 4: 5, 5: 10}.get(num_matches, 0)
        winnings = bet * multiplier

        if winnings > 0:
            st.success(f"🎉 Поздравляем! Совпадений: {num_matches} — Вы выиграли {winnings}!")
        else:
            st.error("😢 Увы! Совпадений недостаточно. Попробуй снова!")

# --- Подвал ---
st.markdown("---")
st.caption("© 2025 Мини Лото. Удачи и везения!")
