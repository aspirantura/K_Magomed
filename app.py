import streamlit as st

# Настройки страницы
st.set_page_config(
    page_title="Алгоритм выбора метода хирургического лечения",
    page_icon="🦷",
    layout="wide"
)

# Заголовок
st.title("Алгоритм выбора метода хирургической коррекции")
st.markdown("### Верхняя ретрогнатия при расщелине верхней губы и нёба у взрослых пациентов")
st.markdown("---")

# Две колонки
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Параметры пациента")

    plan_mm = st.number_input(
        "Планируемое выдвижение верхней челюсти, мм",
        min_value=0.0, max_value=25.0, value=8.0, step=0.5
    )

    sna = st.number_input(
        "Угол SNA, градусы",
        min_value=60.0, max_value=90.0, value=74.0, step=0.1
    )

    anb = st.number_input(
        "Угол ANB, градусы",
        min_value=-15.0, max_value=10.0, value=-5.0, step=0.1
    )

    scars = st.selectbox(
        "Выраженность рубцовых изменений мягких тканей",
        ["Минимальные", "Умеренные", "Выраженные"]
    )

    ngf = st.selectbox(
        "Нёбно-глоточная функция",
        ["Сохранна (норма)", "Субкомпенсация", "Декомпенсация"]
    )

    cleft_type = st.selectbox(
        "Тип расщелины",
        ["Односторонняя", "Двусторонняя"]
    )

    calculate = st.button("Определить тактику лечения", type="primary", use_container_width=True)

with col2:
    st.subheader("Рекомендация")

    if calculate:
        # Преобразуем категориальные переменные
        scars_score = {"Минимальные": 0, "Умеренные": 1, "Выраженные": 2}[scars]
        ngf_score = {"Сохранна (норма)": 0, "Субкомпенсация": 1, "Декомпенсация": 2}[ngf]
        bilateral = 1 if cleft_type == "Двусторонняя" else 0

        reasons = []
        risk_factors = []
        method = None

        # Шаг 1: явные показания к ДО
        if plan_mm >= 10:
            method = "ДО"
            reasons.append(f"✓ Планируемое выдвижение ≥ 10 мм ({plan_mm} мм)")

        # Шаг 2: явные показания к Le Fort I
        elif plan_mm <= 8 and sna >= 73 and anb >= -5 and scars_score <= 1 and ngf_score == 0:
            method = "Le Fort I"
            reasons.append(f"✓ Планируемое выдвижение ≤ 8 мм ({plan_mm} мм)")
            reasons.append(f"✓ SNA ≥ 73° ({sna}°)")
            reasons.append(f"✓ ANB ≥ -5° ({anb}°)")
            reasons.append(f"✓ Рубцы не выраженные ({scars.lower()})")
            reasons.append(f"✓ Нёбно-глоточная функция сохранна")

        # Шаг 3: промежуточная зона
        else:
            if plan_mm > 8:
                risk_factors.append(f"Планируемое выдвижение > 8 мм ({plan_mm} мм)")
            if sna <= 72:
                risk_factors.append(f"SNA ≤ 72° ({sna}°)")
            if anb <= -7:
                risk_factors.append(f"ANB ≤ -7° ({anb}°)")
            if scars_score >= 2:
                risk_factors.append("Выраженные рубцовые изменения")
            if ngf_score >= 1:
                risk_factors.append(f"Снижение нёбно-глоточной функции ({ngf.lower()})")
            if bilateral == 1:
                risk_factors.append("Двусторонняя расщелина")

            score = 0
            if plan_mm > 8:
                score += 2
            if sna <= 72:
                score += 1
            if anb <= -7:
                score += 1
            if scars_score >= 2:
                score += 1
            if ngf_score >= 1:
                score += 1
            if bilateral == 1:
                score += 1

            if score >= 3:
                method = "ДО"
                reasons.append(f"Промежуточная клиническая ситуация")
                reasons.append(f"Выявлено {len(risk_factors)} факторов риска (балл = {score})")
            else:
                method = "Le Fort I"
                reasons.append(f"Промежуточная клиническая ситуация")
                reasons.append(f"Факторов риска недостаточно (балл = {score})")

        # Вывод результата
        if method == "ДО":
            st.success("### Рекомендованный метод:")
            st.markdown("## 🟢 Компрессионно-дистракционный остеогенез")
        else:
            st.info("### Рекомендованный метод:")
            st.markdown("## 🔵 Ортогнатическая операция по типу Le Fort I")

        st.markdown("---")
        st.markdown("**Обоснование:**")
        for reason in reasons:
            st.markdown(f"- {reason}")

        if risk_factors:
            st.markdown("**Учтённые факторы риска:**")
            for rf in risk_factors:
                st.markdown(f"- {rf}")

    else:
        st.info("Введите параметры пациента слева и нажмите кнопку «Определить тактику лечения»")

# Краткое описание логики алгоритма
st.markdown("---")
with st.expander("Логика алгоритма выбора метода"):
    st.markdown("""
    **Показания к компрессионно-дистракционному остеогенезу (ДО):**
    - планируемое выдвижение верхней челюсти ≥ 10 мм;
    - выраженные рубцовые изменения мягких тканей;
    - пограничная или сниженная нёбно-глоточная функция;
    - значительный сагиттальный дефицит (SNA ≤ 72°, ANB ≤ -7°);
    - двусторонняя расщелина в сочетании с другими факторами риска.

    **Показания к ортогнатической операции по типу Le Fort I:**
    - планируемое выдвижение ≤ 8 мм;
    - SNA ≥ 73°;
    - ANB ≥ -5°;
    - удовлетворительная нёбно-глоточная функция;
    - отсутствие выраженного рубцевания мягких тканей.

    **Промежуточная клиническая зона (8–10 мм):**
    при наличии 3 и более факторов риска предпочтение отдаётся дистракционному 
    остеогенезу; в иных случаях возможно выполнение ортогнатической операции 
    по типу Le Fort I.
    """)

# Подпись
st.markdown("---")
st.caption("Хамхоев М.Б. Хирургическая реабилитация взрослых пациентов с верхней ретрогнатией "
           "в результате расщелины верхней губы и нёба. — Москва, 2026")
