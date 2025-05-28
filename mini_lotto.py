import streamlit as st
import random

# --- Настройки ---
ACCESS_CODE = "1234"  # Код доступа

# --- Защита входа ---
st.title("🎰 Мини-Лото — Генерация, Ставка и Выигрыш")

code_input = st.text_input("🔐 Введите код доступа:", type="password")
if code_input != ACCESS_CODE:
    st.warning("Введите правильный код для доступа.")
    st.stop()

st.success("✅ Доступ разрешён! Удачи в игре!")

# --- Интерфейс игры ---
st.header("💸 Сделайте ставку и выберите 5 чисел от 1 до 20")
bet = st.number_input("💰 Ваша ставка:", min_value=1, step=1)

user_numbers = st.multiselect(
    "🎯 Выберите 5 уникальных чисел:",
    options=list(range(1, 21)),
    max_selections=5
)

if st.button("🎲 Играть"):
    if len(user_numbers) != 5:
        st.error("❗ Пожалуйста, выберите ровно 5 чисел.")
    else:
        winning_numbers = random.sample(range(1, 21), 5)
        matches = set(user_numbers) & set(winning_numbers)
        num_matches = len(matches)

        st.subheader("📍 Результаты:")
        st.write("🎉 Выпавшие числа:", sorted(winning_numbers))
        st.write("✅ Ваши совпадения:", sorted(matches) if matches else "Нет совпадений")

        # Расчёт выигрыша
        multiplier = {3: 2, 4: 5, 5: 10}.get(num_matches, 0)
        winnings = bet * multiplier

        if winnings > 0:
            st.success(f"🎉 Поздравляем! Совпадений: {num_matches}, Вы выиграли: {winnings}!")
        else:
            st.error("😢 К сожалению, вы проиграли. Попробуйте снова!")
