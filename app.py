from datetime import datetime, date

st.title("수행평가 정리")

tasks = load_tasks()

today = date.today()

for task in tasks:
    target_date = datetime.strptime(
        task["date"],
        "%Y-%m-%d"
    ).date()

    dday = (target_date - today).days

    if dday > 0:
        dday_text = f"D-{dday}"
    elif dday == 0:
        dday_text = "D-DAY"
    else:
        dday_text = f"D+{abs(dday)}"

    st.write(
        f"📚 {task['subject']} | 📅 {task['date']} | 🔥 {dday_text}"
    )
