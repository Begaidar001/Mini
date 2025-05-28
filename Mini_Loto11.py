import streamlit as st
import random

# --- Конфигурация страницы ---
st.set_page_config(page_title="🎰 Мини Лото Казино", layout="centered")

# --- Казино-стиль: фон и стили ---
st.markdown("""
    <style>
    body {
        background-image: url("https://images.unsplash.com/photo-1549924231-f129b911e442?auto=format&fit=crop&w=1500&q=80");
        background-size: cover;
    }
    .main {
        background-color: rgba(0, 0, 0, 0.75);
        padding: 2rem;
        border-radius: 15px;
    }
    h1, h2, h3, h4, h5, h6, p, div, label {
        color: white !important;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff7777;
    }
    </style>
""", unsafe_allow_html=True)

# --- Сессия ---
if "balance" not in st.session_state:
    st.session_state.balance = 1000  # начальный баланс

if "history" not in st.session_state:
    st.session_state.history = []

# --- Доступ по коду ---
st.title("🎰 Мини Лото Казино")

code_input = st.text_input("🔐 Введите код доступа > 1234:", type="password")
if code_input != "1234":
    st.warning("Введите верный код доступа.")
    st.stop()

st.success("Добро пожаловать в казино мини-лото!")

# --- Баланс ---
st.markdown(f"### 💳 Баланс: **{st.session_state.balance}** ₸")

# --- Интерфейс игры ---
st.header("📋 Сделайте ставку и выберите 5 чисел")
bet = st.number_input("💰 Ваша ставка (₸):", min_value=10, max_value=st.session_state.balance, step=10)

user_numbers = st.multiselect("🎯 Выберите 5 уникальных чисел от 1 до 20:",
                              options=list(range(1, 21)),
                              max_selections=5)

if st.button("🎲 Играть!"):
    if len(user_numbers) != 5:
        st.error("❗ Нужно выбрать ровно 5 чисел.")
    elif bet > st.session_state.balance:
        st.error("❗ Недостаточно средств.")
    else:
        # Игра
        winning_numbers = random.sample(range(1, 21), 5)
        matches = set(user_numbers) & set(winning_numbers)
        match_count = len(matches)

        # Комбинации и коэффициенты
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

        # Обновление баланса
        st.session_state.balance -= bet
        st.session_state.balance += win_amount

        # Добавить в историю
        st.session_state.history.insert(0, {
            "ставка": bet,
            "числа": sorted(user_numbers),
            "выпали": sorted(winning_numbers),
            "совпадения": match_count,
            "комбинация": combo_name,
            "выигрыш": win_amount
        })

        # Отображение
        st.subheader("📊 Результаты:")
        st.write("🎟️ Ваши числа:", sorted(user_numbers))
        st.write("🎲 Выпавшие числа:", sorted(winning_numbers))
        st.write("✅ Совпадения:", f"{match_count} — {combo_name}")
        if win_amount > 0:
            st.success(f"🎉 Вы выиграли: {win_amount} ₸")
        else:
            st.error("😢 Вы проиграли эту ставку.")

        st.markdown(f"### 💳 Новый баланс: **{st.session_state.balance}** ₸")

# --- История ставок ---
with st.expander("🧾 История ставок (последние 5 игр)"):
    if not st.session_state.history:
        st.info("История пуста. Начни играть!")
    else:
        for i, entry in enumerate(st.session_state.history[:5]):
            st.markdown(f"**🎯 Игра #{i+1}:**")
            st.markdown(f"- Ставка: {entry['ставка']} ₸")
            st.markdown(f"- Числа: {entry['числа']}")
            st.markdown(f"- Выпали: {entry['выпали']}")
            st.markdown(f"- Совпадения: {entry['совпадения']} — {entry['комбинация']}")
            st.markdown(f"- 💰 Выигрыш: {entry['выигрыш']} ₸")
            st.markdown("---")

# --- Подвал ---
st.caption("© 2025 Мини Лото Казино | Удачи и выигрышей!")
