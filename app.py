import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import date

# ---------------------------
# MongoDB Connection
# ---------------------------
MONGO_URI = "mongodb://localhost:27017/"

client = MongoClient(MONGO_URI)
db = client["health_tracker"]
collection = db["health_records"]

# ---------------------------
# App Title
# ---------------------------
st.set_page_config(page_title="Health Tracker", page_icon="🏥")

st.title("🏥 Personal Health Tracker")

menu = st.sidebar.selectbox(
    "Menu",
    ["Add Health Record", "View Records"]
)

# ---------------------------
# Add Record
# ---------------------------
if menu == "Add Health Record":

    st.subheader("Enter Daily Health Data")

    record_date = st.date_input("Date", date.today())

    weight = st.number_input(
        "Weight (kg)",
        min_value=0.0,
        step=0.1
    )

    systolic = st.number_input(
        "Systolic BP",
        min_value=0
    )

    diastolic = st.number_input(
        "Diastolic BP",
        min_value=0
    )

    heart_rate = st.number_input(
        "Heart Rate (BPM)",
        min_value=0
    )

    steps = st.number_input(
        "Steps Walked",
        min_value=0
    )

    water = st.number_input(
        "Water Intake (Liters)",
        min_value=0.0,
        step=0.1
    )

    if st.button("Save Record"):

        data = {
            "date": str(record_date),
            "weight": weight,
            "blood_pressure": f"{systolic}/{diastolic}",
            "heart_rate": heart_rate,
            "steps": steps,
            "water_intake": water
        }

        collection.insert_one(data)

        st.success("Health record saved successfully!")

# ---------------------------
# View Records
# ---------------------------
elif menu == "View Records":

    st.subheader("Health Records")

    records = list(collection.find({}, {"_id": 0}))

    if records:
        df = pd.DataFrame(records)
        st.dataframe(df, use_container_width=True)

        st.subheader("Summary")

        avg_weight = df["weight"].mean()
        avg_steps = df["steps"].mean()
        avg_heart_rate = df["heart_rate"].mean()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Average Weight",
            f"{avg_weight:.1f} kg"
        )

        col2.metric(
            "Average Steps",
            f"{avg_steps:.0f}"
        )

        col3.metric(
            "Average Heart Rate",
            f"{avg_heart_rate:.0f} BPM"
        )

        st.line_chart(
            df.set_index("date")[["weight"]]
        )

        st.bar_chart(
            df.set_index("date")[["steps"]]
        )

    else:
        st.warning("No records found.")
