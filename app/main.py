import streamlit as st

# Настройка страницы (широкий формат, как на макете)
st.set_page_config(page_title="SSPMS - Landing", layout="wide")

# --- ВЕРХНЯЯ ПАНЕЛЬ (Имитация шапки) ---
col_logo, col_space, col_nav, col_btn = st.columns([2, 4, 3, 1])

with col_logo:
    st.markdown("### 🎓 **SSPMS**") # Логотип

with col_nav:
    # Просто текст вместо ссылок для красоты
    st.markdown("<p style='text-align: right; color: gray;'>About &nbsp;&nbsp;&nbsp; Features &nbsp;&nbsp;&nbsp; Contact</p>", unsafe_allow_html=True)

with col_btn:
    # Кнопка логина
    st.button("Login", use_container_width=True)

st.divider() # Линия-разделитель

# --- ГЛАВНЫЙ БЛОК (Заголовок и кнопка) ---
# Делаем отступы по бокам, чтобы текст был по центру
col1, col2, col3 = st.columns([1, 8, 1])

with col2:
    # Большой заголовок
    st.markdown("<h1 style='font-size: 50px; line-height: 1.2;'>Smart Student<br>Performance<br>Monitoring System</h1>", unsafe_allow_html=True)
    
    # Подзаголовок
    st.markdown("#### Data-driven insights for student success.")
    
    # Описание
    st.write("Monitor academic performance, identify students at risk, and provide timely support for a brighter academic future.")
    
    st.write("") # Пустая строка для отступа
    
    # Кнопка Get Started (пока просто заглушка)
    if st.button("Get Started →", type="primary"):
        st.info("Тут будет переход на страницу входа (Login)")

st.write("")
st.write("")

# --- БЛОК С 4 КАРТОЧКАМИ ---
col_card1, col_card2, col_card3, col_card4 = st.columns(4)

# Оформляем карточки с помощью HTML для красоты
card_style = """
<div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center; height: 150px;">
    <h1 style="margin: 0;">{icon}</h1>
    <p style="font-weight: bold; margin-top: 10px;">{title}</p>
</div>
"""

with col_card1:
    st.markdown(card_style.format(icon="📊", title="Predict Academic<br>Risks"), unsafe_allow_html=True)

with col_card2:
    st.markdown(card_style.format(icon="👥", title="Support Students<br>Early"), unsafe_allow_html=True)

with col_card3:
    st.markdown(card_style.format(icon="📈", title="Data-Driven<br>Decisions"), unsafe_allow_html=True)

with col_card4:
    st.markdown(card_style.format(icon="🎓", title="For Students,<br>Teachers and Curators"), unsafe_allow_html=True)
