if tasks:
    closest_task = min(
        tasks,
        key=lambda x: (datetime.strptime(x["date"], "%Y-%m-%d").date() - today).days
    )

    target_date = datetime.strptime(closest_task["date"], "%Y-%m-%d").date()
    dday = (target_date - today).days

    dday_text = f"D-{dday}" if dday > 0 else ("🔥 D-DAY 🔥" if dday == 0 else f"D+{abs(dday)}")

    # 🔥 핵심: 당일일 때만 크게 표시
    if dday == 0:
        st.markdown(
            f"""
            <div style="
                text-align:center;
                padding:80px;
                border-radius:30px;
                background:linear-gradient(135deg,#ff0000,#ff7300);
                color:white;
                margin-bottom:30px;
            ">
                <h1 style="font-size:90px;">
                    🔥🔥 {closest_task['subject']} 🔥🔥
                </h1>

                <h1 style="font-size:120px;">
                    {dday_text}
                </h1>

                <p style="font-size:30px;">
                    {closest_task['date']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
