import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Smart Food Waste",
    page_icon="🍲",
    layout="wide"
)

st.title("🍲 AI Smart Food Waste Management")
st.subheader("Smart food planning for college hostels and canteens")

st.write(
    "Estimate food requirements, track surplus meals, "
    "and identify opportunities to reduce food waste."
)

st.sidebar.header("Enter Today's Details")

students = st.sidebar.number_input(
    "Expected students",
    min_value=1,
    value=200
)

attendance = st.sidebar.slider(
    "Expected attendance (%)",
    min_value=10,
    max_value=100,
    value=85
)

food_prepared = st.sidebar.number_input(
    "Meals prepared",
    min_value=0,
    value=200
)

average_consumption = st.sidebar.number_input(
    "Average meals consumed per student",
    min_value=0.1,
    max_value=2.0,
    value=0.9,
    step=0.1
)

expected_students = students * attendance / 100

# Baseline estimate, not a trained AI model
predicted_demand = round(
    expected_students * average_consumption
)

surplus = max(0, food_prepared - predicted_demand)
shortage = max(0, predicted_demand - food_prepared)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Expected attendance",
    f"{expected_students:.0f} students"
)

col2.metric(
    "Estimated meal demand",
    f"{predicted_demand} meals"
)

col3.metric(
    "Potential surplus",
    f"{surplus} meals"
)

st.divider()
st.header("💡 Smart Recommendations")

if shortage > 0:
    st.warning(
        f"Prepare approximately {shortage} additional meals "
        "to meet estimated demand."
    )
elif surplus > 0:
    st.success(
        f"Approximately {surplus} meals may remain. "
        "Verify food safety and arrange timely donation "
        "through an authorized food redistribution partner."
    )
else:
    st.info(
        "Meal preparation matches estimated demand."
    )

st.header("📊 Food Planning Summary")

data = pd.DataFrame({
    "Category": [
        "Estimated demand",
        "Meals prepared",
        "Potential surplus",
        "Potential shortage"
    ],
    "Meals": [
        predicted_demand,
        food_prepared,
        surplus,
        shortage
    ]
})

st.bar_chart(data.set_index("Category"))

st.header("📝 Save Today's Record")

date = st.date_input("Date")
meal_type = st.selectbox(
    "Meal",
    ["Breakfast", "Lunch", "Dinner"]
)

if st.button("Save Record"):
    record = pd.DataFrame([{
        "Date": str(date),
        "Meal": meal_type,
        "Expected Students": students,
        "Attendance (%)": attendance,
        "Meals Prepared": food_prepared,
        "Estimated Demand": predicted_demand,
        "Potential Surplus": surplus,
        "Potential Shortage": shortage
    }])

    try:
        old_data = pd.read_csv("food_records.csv")
        record = pd.concat(
            [old_data, record],
            ignore_index=True
        )
    except FileNotFoundError:
        pass

    record.to_csv("food_records.csv", index=False)
    st.success("Record saved successfully!")

try:
    history = pd.read_csv("food_records.csv")
    st.header("📚 Saved Food Records")
    st.dataframe(history, use_container_width=True)

    st.download_button(
        "Download Records as CSV",
        data=history.to_csv(index=False).encode("utf-8"),
        file_name="food_records.csv",
        mime="text/csv"
    )
except FileNotFoundError:
    st.caption("Your saved records will appear here.")