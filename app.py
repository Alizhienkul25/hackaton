import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ══════════════════════════════════════════════════════════════════
#  КОНФИГ СТРАНИЦЫ (должен быть ПЕРВОЙ командой Streamlit!)
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SmartCollege Monitor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════
#  КАСТОМНЫЙ CSS — красивый современный дизайн
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Скрываем стандартный хедер */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Общий фон */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    min-height: 100vh;
}

/* Боковая панель */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
}
[data-testid="stSidebar"] * {
    color: #e0e0ff !important;
}

/* Заголовок приложения */
.app-header {
    background: linear-gradient(90deg, rgba(102,126,234,0.15), rgba(118,75,162,0.15));
    border: 1px solid rgba(102,126,234,0.3);
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 28px;
    backdrop-filter: blur(10px);
}
.app-header h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}
.app-header p {
    color: rgba(224,224,255,0.6);
    margin: 6px 0 0;
    font-size: 0.95rem;
}

/* Карточки метрик */
.metric-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 20px 24px;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: transform 0.2s, border-color 0.2s;
}
.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(102,126,234,0.5);
}
.metric-card .value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #a78bfa;
    line-height: 1;
}
.metric-card .label {
    color: rgba(224,224,255,0.6);
    font-size: 0.82rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 6px;
}
.metric-card .sub {
    color: rgba(224,224,255,0.35);
    font-size: 0.75rem;
    margin-top: 4px;
}

/* Секции */
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: #e0e0ff;
    margin: 28px 0 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

/* Индикаторы оценок */
.grade-pill {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.grade-A { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.grade-B { background: rgba(96,165,250,0.15); color: #60a5fa; border: 1px solid rgba(96,165,250,0.3); }
.grade-C { background: rgba(251,191,36,0.15); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.grade-D { background: rgba(248,113,113,0.15); color: #f87171; border: 1px solid rgba(248,113,113,0.3); }

/* Кнопки */
.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 15px rgba(102,126,234,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(102,126,234,0.5) !important;
}

/* Поля ввода */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #e0e0ff !important;
    border-radius: 10px !important;
}

/* Слайдер */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #667eea, #764ba2) !important;
}

/* Алерты */
.stSuccess {
    background: rgba(52,211,153,0.1) !important;
    border: 1px solid rgba(52,211,153,0.3) !important;
    border-radius: 10px !important;
    color: #34d399 !important;
}
.stWarning {
    background: rgba(251,191,36,0.1) !important;
    border: 1px solid rgba(251,191,36,0.3) !important;
    border-radius: 10px !important;
}
.stError {
    background: rgba(248,113,113,0.1) !important;
    border: 1px solid rgba(248,113,113,0.3) !important;
    border-radius: 10px !important;
}
.stInfo {
    background: rgba(96,165,250,0.1) !important;
    border: 1px solid rgba(96,165,250,0.3) !important;
    border-radius: 10px !important;
    color: #60a5fa !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    overflow: hidden;
}

/* Plotly графики — прозрачный фон */
.js-plotly-plot {
    border-radius: 14px;
    overflow: hidden;
}

/* Рейтинговые карточки */
.rank-card {
    display: flex;
    align-items: center;
    gap: 16px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 10px;
    transition: border-color 0.2s;
}
.rank-card:hover { border-color: rgba(102,126,234,0.4); }
.rank-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: rgba(167,139,250,0.5);
    min-width: 36px;
    text-align: center;
}
.rank-num.top { color: #fbbf24; }
.rank-info { flex: 1; }
.rank-name { color: #e0e0ff; font-weight: 600; font-size: 0.95rem; }
.rank-meta { color: rgba(224,224,255,0.4); font-size: 0.8rem; margin-top: 2px; }
.rank-grade {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #a78bfa;
}

/* Вертикальный разделитель */
.divider {
    height: 1px;
    background: rgba(255,255,255,0.07);
    margin: 24px 0;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  КОНСТАНТЫ
# ══════════════════════════════════════════════════════════════════
DATA_FILE = "students.json"

SUBJECTS = [
    "Математика",
    "Физика",
    "Информатика",
    "Русская Литература",
    "Английский язык",
    "Всемирная История",
    "География",
    "Химия"
]

GROUPS = ["БНГС1-25", "ПО1-25", "ПО2-25", "АиУ1-25", "ТДНГ1-25", "ХТП1-25"]

# ══════════════════════════════════════════════════════════════════
#  ФУНКЦИИ РАБОТЫ С ДАННЫМИ
# ══════════════════════════════════════════════════════════════════

def load_data() -> list:
    """Загружает данные из JSON. Возвращает [] если файла нет или он повреждён."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Убедимся что это список
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []

def save_data(data: list) -> bool:
    """Сохраняет данные в JSON. Возвращает True если успешно."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        st.error(f"Ошибка сохранения: {e}")
        return False

def add_record(name: str, group: str, subject: str, grade: int) -> dict | None:
    """Добавляет запись. Возвращает запись или None при ошибке."""
    data = load_data()
    # Генерируем уникальный ID (не зависит от длины массива, чтобы не было дубликатов)
    max_id = max((r.get("id", 0) for r in data), default=0)
    record = {
        "id": max_id + 1,
        "name": name,
        "group": group,
        "subject": subject,
        "grade": grade,
        "date": datetime.now().strftime("%d.%m.%Y %H:%M")
    }
    data.append(record)
    if save_data(data):
        return record
    return None

def delete_record(record_id: int) -> bool:
    """Удаляет запись по ID. Возвращает True если запись нашлась и удалилась."""
    data = load_data()
    new_data = [r for r in data if r.get("id") != record_id]
    if len(new_data) == len(data):
        return False  # не нашли
    return save_data(new_data)

def get_grade_level(grade: int) -> tuple[str, str]:
    """Возвращает (текст уровня, CSS класс) для оценки."""
    if grade >= 90:
        return "Отлично", "grade-A"
    elif grade >= 75:
        return "Хорошо", "grade-B"
    elif grade >= 50:
        return "Удовл.", "grade-C"
    else:
        return "Неудовл.", "grade-D"

# Plotly тема (тёмная, прозрачный фон)
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#c0c0e0"),
    title_font=dict(family="Space Grotesk, sans-serif", color="#e0e0ff", size=16),
    xaxis=dict(gridcolor="rgba(255,255,255,0.07)", linecolor="rgba(255,255,255,0.1)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.07)", linecolor="rgba(255,255,255,0.1)"),
    margin=dict(l=20, r=20, t=40, b=20),
)

# ══════════════════════════════════════════════════════════════════
#  БОКОВАЯ ПАНЕЛЬ
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 12px 0 20px;">
        <div style="font-size:3rem;">🎓</div>
        <div style="font-family:'Space Grotesk',sans-serif; font-size:1.2rem;
             font-weight:700; color:#a78bfa; margin-top:6px;">SmartCollege</div>
        <div style="font-size:0.75rem; color:rgba(224,224,255,0.4); margin-top:2px;">Monitor v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Навигация",
        ["🏠  Главная",
         "➕  Добавить оценку",
         "📋  Таблица оценок",
         "📈  Графики",
         "🏆  Рейтинг и статистика"],
        label_visibility="collapsed"
    )

    # Мини-статистика в сайдбаре
    data_sidebar = load_data()
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    if data_sidebar:
        df_side = pd.DataFrame(data_sidebar)
        st.markdown(f"""
        <div style="color:rgba(224,224,255,0.5); font-size:0.78rem; text-align:center; line-height:2;">
            📊 Записей: <b style="color:#a78bfa">{len(df_side)}</b><br>
            👤 Студентов: <b style="color:#60a5fa">{df_side['name'].nunique()}</b><br>
            📚 Предметов: <b style="color:#34d399">{df_side['subject'].nunique()}</b><br>
            ⭐ Ср. балл: <b style="color:#fbbf24">{df_side['grade'].mean():.1f}</b>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="color:rgba(224,224,255,0.3); font-size:0.78rem; text-align:center;">
            Данных пока нет
        </div>
        """, unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color:rgba(224,224,255,0.25); font-size:0.7rem; text-align:center;">
        Хакатон 2025 · АиУ4-25<br>Python + Streamlit
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  СТРАНИЦА 0: ГЛАВНАЯ
# ══════════════════════════════════════════════════════════════════
if page == "🏠  Главная":
    st.markdown("""
    <div class="app-header">
        <h1>📊 SmartCollege Monitor</h1>
        <p>Система мониторинга успеваемости студентов · Трек G — Дашборды</p>
    </div>
    """, unsafe_allow_html=True)

    data = load_data()

    if not data:
        st.markdown("""
        <div style="text-align:center; padding: 60px 20px;">
            <div style="font-size:5rem;">🚀</div>
            <h2 style="color:#a78bfa; font-family:'Space Grotesk',sans-serif; margin:16px 0 8px;">
                Добро пожаловать!
            </h2>
            <p style="color:rgba(224,224,255,0.5); max-width:400px; margin:0 auto;">
                Приложение готово к работе. Начните с добавления оценок студентов.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("➕ Добавить первую оценку", use_container_width=True):
            st.rerun()
    else:
        df = pd.DataFrame(data)

        # Метрики
        col1, col2, col3, col4 = st.columns(4)
        metrics = [
            (col1, str(len(df)), "Всего записей", ""),
            (col2, str(df["name"].nunique()), "Студентов", ""),
            (col3, f"{df['grade'].mean():.1f}", "Средний балл", "из 100"),
            (col4, str(df["subject"].nunique()), "Предметов", ""),
        ]
        for col, val, label, sub in metrics:
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="value">{val}</div>
                    <div class="label">{label}</div>
                    <div class="sub">{sub}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown('<div class="section-title">Топ студентов</div>', unsafe_allow_html=True)
            top = df.groupby("name")["grade"].mean().sort_values(ascending=False).head(5)
            medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
            for i, (name, grade) in enumerate(top.items()):
                level, css = get_grade_level(int(grade))
                st.markdown(f"""
                <div class="rank-card">
                    <div class="rank-num {'top' if i < 3 else ''}">{medals[i]}</div>
                    <div class="rank-info">
                        <div class="rank-name">{name}</div>
                        <div class="rank-meta"><span class="grade-pill {css}">{level}</span></div>
                    </div>
                    <div class="rank-grade">{grade:.1f}</div>
                </div>
                """, unsafe_allow_html=True)

        with col_b:
            st.markdown('<div class="section-title">Последние оценки</div>', unsafe_allow_html=True)
            last = data[-8:][::-1]
            for rec in last:
                level, css = get_grade_level(rec["grade"])
                st.markdown(f"""
                <div style="display:flex; align-items:center; justify-content:space-between;
                     padding:10px 14px; background:rgba(255,255,255,0.03);
                     border:1px solid rgba(255,255,255,0.07); border-radius:10px; margin-bottom:8px;">
                    <div>
                        <span style="color:#e0e0ff; font-weight:500; font-size:0.9rem;">{rec['name']}</span>
                        <span style="color:rgba(224,224,255,0.4); font-size:0.8rem; margin-left:8px;">{rec['subject']}</span>
                    </div>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <span class="grade-pill {css}">{rec['grade']}</span>
                        <span style="color:rgba(224,224,255,0.3); font-size:0.75rem;">{rec['date']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  СТРАНИЦА 1: ДОБАВИТЬ ОЦЕНКУ
# ══════════════════════════════════════════════════════════════════
elif page == "➕  Добавить оценку":
    st.markdown("""
    <div class="app-header">
        <h1>➕ Добавить оценку</h1>
        <p>Введите данные студента. Оценка сохранится автоматически в students.json</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="section-title">Данные студента</div>', unsafe_allow_html=True)
        name = st.text_input(
            "ФИО студента",
            placeholder="Например: Сериков Арман Болатович",
            help="Введите полное имя студента"
        )
        group = st.selectbox("Группа", GROUPS, help="Выберите учебную группу")
        subject = st.selectbox("Предмет", SUBJECTS)

    with col2:
        st.markdown('<div class="section-title">Оценка</div>', unsafe_allow_html=True)
        grade = st.slider(
            "Балл (0 – 100)",
            min_value=0, max_value=100, value=75, step=1
        )

        # Красивый индикатор оценки
        level, css = get_grade_level(grade)
        grade_colors = {
            "grade-A": ("#34d399", "rgba(52,211,153,0.1)", "rgba(52,211,153,0.3)"),
            "grade-B": ("#60a5fa", "rgba(96,165,250,0.1)", "rgba(96,165,250,0.3)"),
            "grade-C": ("#fbbf24", "rgba(251,191,36,0.1)",  "rgba(251,191,36,0.3)"),
            "grade-D": ("#f87171", "rgba(248,113,113,0.1)", "rgba(248,113,113,0.3)"),
        }
        color, bg, border = grade_colors[css]
        bar_width = grade  # процент заполнения

        st.markdown(f"""
        <div style="background:{bg}; border:1px solid {border}; border-radius:14px; padding:20px 24px; margin-top:8px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <span style="color:rgba(224,224,255,0.7); font-size:0.9rem;">Оценка</span>
                <span style="font-family:'Space Grotesk',sans-serif; font-size:1.8rem;
                      font-weight:700; color:{color};">{grade}</span>
            </div>
            <div style="background:rgba(0,0,0,0.2); border-radius:999px; height:8px; overflow:hidden;">
                <div style="width:{bar_width}%; height:100%; background:{color};
                     border-radius:999px; transition:width 0.3s;"></div>
            </div>
            <div style="text-align:right; margin-top:8px;">
                <span class="grade-pill {css}">{level}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Кнопка сохранения
    if st.button("💾 Сохранить оценку", type="primary", use_container_width=True):
        # Валидация — приложение не падает от пустого ввода
        errors = []
        if not name or not name.strip():
            errors.append("Введите ФИО студента")
        elif len(name.strip()) < 3:
            errors.append("ФИО слишком короткое (минимум 3 символа)")
        elif len(name.strip()) > 100:
            errors.append("ФИО слишком длинное (максимум 100 символов)")

        if errors:
            for err in errors:
                st.error(f"❌ {err}")
        else:
            record = add_record(name.strip(), group, subject, grade)
            if record:
                st.success(f"✅ Сохранено! **{name.strip()}** | {subject} | **{grade} баллов** | {datetime.now().strftime('%d.%m.%Y %H:%M')}")
                st.balloons()
            # (ошибка уже показана внутри save_data)

    # Последние 5 записей
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Последние добавленные</div>', unsafe_allow_html=True)

    recent_data = load_data()
    if recent_data:
        for rec in reversed(recent_data[-5:]):
            level, css = get_grade_level(rec["grade"])
            st.markdown(f"""
            <div style="display:flex; align-items:center; justify-content:space-between;
                 padding:12px 16px; background:rgba(255,255,255,0.03);
                 border:1px solid rgba(255,255,255,0.07); border-radius:10px; margin-bottom:8px;">
                <div style="display:flex; align-items:center; gap:14px;">
                    <span style="color:#e0e0ff; font-weight:500;">{rec['name']}</span>
                    <span style="color:rgba(224,224,255,0.4); font-size:0.82rem;">
                        {rec['group']} · {rec['subject']}
                    </span>
                </div>
                <div style="display:flex; align-items:center; gap:12px;">
                    <span class="grade-pill {css}">{rec['grade']} баллов</span>
                    <span style="color:rgba(224,224,255,0.3); font-size:0.75rem;">{rec['date']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Ещё нет добавленных оценок.")

# ══════════════════════════════════════════════════════════════════
#  СТРАНИЦА 2: ТАБЛИЦА ОЦЕНОК
# ══════════════════════════════════════════════════════════════════
elif page == "📋  Таблица оценок":
    st.markdown("""
    <div class="app-header">
        <h1>📋 Таблица оценок</h1>
        <p>Просмотр, фильтрация и управление данными</p>
    </div>
    """, unsafe_allow_html=True)

    data = load_data()

    if not data:
        st.info("📭 Данных пока нет. Перейдите на страницу «Добавить оценку».")
    else:
        df = pd.DataFrame(data)

        # ── Фильтры ──
        st.markdown('<div class="section-title">Фильтры</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            available_groups = sorted(df["group"].unique().tolist())
            filter_group = st.multiselect(
                "Группа",
                options=available_groups,
                default=available_groups,
                placeholder="Все группы"
            )

        with col2:
            available_subjects = sorted(df["subject"].unique().tolist())
            filter_subject = st.multiselect(
                "Предмет",
                options=available_subjects,
                default=available_subjects,
                placeholder="Все предметы"
            )

        with col3:
            grade_range = st.slider(
                "Диапазон оценок",
                min_value=0, max_value=100,
                value=(0, 100),
                step=5
            )

        # Применяем фильтры (безопасно — не падает на пустых)
        if not filter_group:
            filter_group = available_groups
        if not filter_subject:
            filter_subject = available_subjects

        filtered = df[
            (df["group"].isin(filter_group)) &
            (df["subject"].isin(filter_subject)) &
            (df["grade"] >= grade_range[0]) &
            (df["grade"] <= grade_range[1])
        ].copy()

        # Добавляем столбец уровня
        filtered["Уровень"] = filtered["grade"].apply(lambda g: get_grade_level(g)[0])

        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:16px; margin-bottom:12px;">
            <span style="color:rgba(224,224,255,0.5); font-size:0.85rem;">
                Найдено: <b style="color:#a78bfa">{len(filtered)}</b> из {len(df)} записей
            </span>
        </div>
        """, unsafe_allow_html=True)

        if len(filtered) == 0:
            st.warning("По выбранным фильтрам записей не найдено.")
        else:
            # Переименовываем для отображения
            display_df = filtered[["id", "name", "group", "subject", "grade", "Уровень", "date"]].rename(columns={
                "id": "ID",
                "name": "ФИО студента",
                "group": "Группа",
                "subject": "Предмет",
                "grade": "Балл",
                "date": "Дата"
            })

            st.dataframe(
                display_df,
                use_container_width=True,
                height=420,
                hide_index=True,
                column_config={
                    "Балл": st.column_config.ProgressColumn(
                        "Балл",
                        min_value=0,
                        max_value=100,
                        format="%d"
                    ),
                    "ID": st.column_config.NumberColumn("ID", width="small"),
                }
            )

            # Экспорт CSV
            csv_data = filtered.to_csv(index=False, encoding="utf-8-sig")
            st.download_button(
                label="📥 Скачать как CSV",
                data=csv_data,
                file_name=f"grades_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        # ── Удаление записи ──
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Удалить запись</div>', unsafe_allow_html=True)

        col_del1, col_del2 = st.columns([2, 1])
        with col_del1:
            all_ids = sorted([r.get("id", 0) for r in data])
            if all_ids:
                delete_id = st.number_input(
                    "ID записи для удаления",
                    min_value=min(all_ids),
                    max_value=max(all_ids),
                    step=1,
                    help="ID указан в первом столбце таблицы"
                )
        with col_del2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Удалить запись", use_container_width=True):
                success = delete_record(int(delete_id))
                if success:
                    st.success(f"Запись #{int(delete_id)} удалена.")
                    st.rerun()
                else:
                    st.error(f"Запись с ID {int(delete_id)} не найдена.")

# ══════════════════════════════════════════════════════════════════
#  СТРАНИЦА 3: ГРАФИКИ
# ══════════════════════════════════════════════════════════════════
elif page == "📈  Графики":
    st.markdown("""
    <div class="app-header">
        <h1>📈 Графики успеваемости</h1>
        <p>Визуализация данных по предметам, группам и студентам</p>
    </div>
    """, unsafe_allow_html=True)

    data = load_data()

    if not data:
        st.info("📭 Нет данных для построения графиков. Добавьте оценки.")
    else:
        df = pd.DataFrame(data)

        col1, col2 = st.columns(2, gap="medium")

        # ── График 1: Средний балл по предметам (горизонтальный бар) ──
        with col1:
            avg_subj = (
                df.groupby("subject")["grade"]
                .agg(["mean", "count"])
                .reset_index()
                .rename(columns={"subject": "Предмет", "mean": "Средний балл", "count": "Кол-во"})
                .sort_values("Средний балл", ascending=True)
            )
            avg_subj["Средний балл"] = avg_subj["Средний балл"].round(1)

            fig1 = px.bar(
                avg_subj,
                x="Средний балл",
                y="Предмет",
                orientation="h",
                text="Средний балл",
                color="Средний балл",
                color_continuous_scale=["#f87171", "#fbbf24", "#34d399"],
                range_color=[40, 100],
                title="Средний балл по предметам",
                custom_data=["Кол-во"]
            )
            fig1.update_traces(
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>Средний балл: %{x}<br>Оценок: %{customdata[0]}<extra></extra>"
            )
            fig1.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False, height=350)
            st.plotly_chart(fig1, use_container_width=True)

        # ── График 2: Гистограмма распределения ──
        with col2:
            fig2 = px.histogram(
                df, x="grade", nbins=10,
                title="Распределение оценок",
                labels={"grade": "Балл", "count": "Студентов"},
                color_discrete_sequence=["#a78bfa"],
                opacity=0.85
            )
            fig2.update_traces(
                hovertemplate="Балл: %{x}<br>Кол-во: %{y}<extra></extra>"
            )
            fig2.update_layout(**PLOTLY_LAYOUT, height=350)
            st.plotly_chart(fig2, use_container_width=True)

        # ── График 3: Сравнение групп ──
        if df["group"].nunique() > 1:
            avg_group = (
                df.groupby("group")["grade"]
                .agg(["mean", "count", "min", "max"])
                .reset_index()
                .rename(columns={
                    "group": "Группа",
                    "mean": "Средний балл",
                    "count": "Записей",
                    "min": "Мин",
                    "max": "Макс"
                })
            )
            avg_group["Средний балл"] = avg_group["Средний балл"].round(1)

            fig3 = px.bar(
                avg_group,
                x="Группа",
                y="Средний балл",
                color="Группа",
                text="Средний балл",
                error_y=avg_group["Макс"] - avg_group["Средний балл"],
                error_y_minus=avg_group["Средний балл"] - avg_group["Мин"],
                title="Сравнение групп (среднее + разброс)",
                color_discrete_sequence=["#667eea", "#a78bfa", "#60a5fa", "#34d399", "#fbbf24", "#f87171"]
            )
            fig3.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=350)
            st.plotly_chart(fig3, use_container_width=True)

        # ── График 4: Heatmap предмет × группа ──
        if df["group"].nunique() > 1 and df["subject"].nunique() > 1:
            heat_data = df.pivot_table(
                values="grade",
                index="subject",
                columns="group",
                aggfunc="mean"
            ).round(1)

            fig4 = go.Figure(data=go.Heatmap(
                z=heat_data.values,
                x=heat_data.columns.tolist(),
                y=heat_data.index.tolist(),
                colorscale=[[0, "#f87171"], [0.5, "#fbbf24"], [1, "#34d399"]],
                zmin=0, zmax=100,
                text=heat_data.values.round(1),
                texttemplate="%{text}",
                hovertemplate="Предмет: %{y}<br>Группа: %{x}<br>Средний балл: %{z}<extra></extra>"
            ))
            fig4.update_layout(
                **PLOTLY_LAYOUT,
                title="Тепловая карта: средний балл по предметам и группам",
                height=max(300, len(heat_data) * 45 + 80)
            )
            st.plotly_chart(fig4, use_container_width=True)
        else:
            # Scatter если только одна группа
            fig4 = px.scatter(
                df, x="subject", y="grade",
                color="name",
                size="grade",
                title="Оценки студентов по предметам",
                labels={"subject": "Предмет", "grade": "Балл", "name": "Студент"},
                hover_data=["group", "date"]
            )
            fig4.update_layout(**PLOTLY_LAYOUT, height=380, xaxis_tickangle=-30)
            st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
#  СТРАНИЦА 4: РЕЙТИНГ И СТАТИСТИКА
# ══════════════════════════════════════════════════════════════════
elif page == "🏆  Рейтинг и статистика":
    st.markdown("""
    <div class="app-header">
        <h1>🏆 Рейтинг и статистика</h1>
        <p>Сводный анализ успеваемости группы</p>
    </div>
    """, unsafe_allow_html=True)

    data = load_data()

    if not data:
        st.info("📭 Нет данных. Добавьте оценки для просмотра статистики.")
    else:
        df = pd.DataFrame(data)

        # ── Общие метрики ──
        st.markdown('<div class="section-title">Сводные показатели</div>', unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns(5)
        metrics_main = [
            (col1, str(len(df)), "Всего оценок", ""),
            (col2, str(df["name"].nunique()), "Студентов", ""),
            (col3, f"{df['grade'].mean():.1f}", "Средний балл", "из 100"),
            (col4, str(df["grade"].max()), "Максимум", "баллов"),
            (col5, str(df["grade"].min()), "Минимум", "баллов"),
        ]
        for col, val, label, sub in metrics_main:
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="value" style="font-size:1.9rem;">{val}</div>
                    <div class="label">{label}</div>
                    <div class="sub">{sub}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        col_left, col_right = st.columns(2, gap="large")

        # ── Топ-5 студентов ──
        with col_left:
            st.markdown('<div class="section-title">🏅 Рейтинг студентов</div>', unsafe_allow_html=True)
            student_stats = (
                df.groupby("name")["grade"]
                .agg(["mean", "count"])
                .rename(columns={"mean": "avg", "count": "cnt"})
                .sort_values("avg", ascending=False)
                .head(10)
            )
            medals = ["🥇", "🥈", "🥉"] + [f"{i}." for i in range(4, 11)]
            for i, (name, row) in enumerate(student_stats.iterrows()):
                level, css = get_grade_level(int(row["avg"]))
                st.markdown(f"""
                <div class="rank-card">
                    <div class="rank-num {'top' if i < 3 else ''}">{medals[i]}</div>
                    <div class="rank-info">
                        <div class="rank-name">{name}</div>
                        <div class="rank-meta">
                            <span class="grade-pill {css}">{level}</span>
                            <span style="color:rgba(224,224,255,0.3); font-size:0.75rem; margin-left:8px;">
                                {int(row['cnt'])} {'оценка' if row['cnt']==1 else 'оценки' if 2<=row['cnt']<=4 else 'оценок'}
                            </span>
                        </div>
                    </div>
                    <div class="rank-grade">{row['avg']:.1f}</div>
                </div>
                """, unsafe_allow_html=True)

        # ── Круговая диаграмма уровней ──
        with col_right:
            st.markdown('<div class="section-title">Распределение по уровням</div>', unsafe_allow_html=True)

            df["Уровень"] = df["grade"].apply(lambda g: get_grade_level(g)[0])
            level_order = ["Отлично", "Хорошо", "Удовл.", "Неудовл."]
            level_colors = {"Отлично": "#34d399", "Хорошо": "#60a5fa", "Удовл.": "#fbbf24", "Неудовл.": "#f87171"}
            level_counts = df["Уровень"].value_counts().reindex(level_order).dropna().reset_index()
            level_counts.columns = ["Уровень", "Количество"]

            fig_pie = px.pie(
                level_counts,
                names="Уровень",
                values="Количество",
                color="Уровень",
                color_discrete_map=level_colors,
                hole=0.45
            )
            fig_pie.update_traces(
                textinfo="percent+label",
                hovertemplate="%{label}: %{value} студентов (%{percent})<extra></extra>"
            )
            fig_pie.update_layout(**PLOTLY_LAYOUT, height=340, showlegend=True,
                                   legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig_pie, use_container_width=True)

            # Нуждаются в помощи
            struggling = df[df["grade"] < 50][["name", "subject", "grade"]].copy()
            if len(struggling) > 0:
                st.markdown('<div class="section-title">⚠️ Требуют внимания (< 50 баллов)</div>',
                            unsafe_allow_html=True)
                struggling.columns = ["Студент", "Предмет", "Балл"]
                st.dataframe(struggling, use_container_width=True, hide_index=True)
            else:
                st.success("✅ Все студенты набрали 50 и выше баллов!")
