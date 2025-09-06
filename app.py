import streamlit as st
import pandas as pd
from datetime import date
import io
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Medical Appointment System", page_icon="🏥", layout="wide")

# ---------- FILE PATHS ----------
PATIENT_DB = "patient_database.csv"
DOCTOR_SCHEDULE = "doctor_schedule.xlsx"
ALL_APPOINTMENTS_FILE = "all_appointments.xlsx"

# Use st.session_state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# ---------- CREDENTIALS (for demonstration) ----------
# Replace this with a more secure method in a real application
CREDENTIALS = {
    "user1": "pass123",
    "admin": "admin123"
}

def authenticate(username, password):
    if username in CREDENTIALS and CREDENTIALS[username] == password:
        return True
    return False

# ---------- LOGIN PAGE ----------
if not st.session_state.authenticated:
    st.title("Welcome to the Patient Care-Pro")
    st.info("Please log in to continue.")
    
    # Use columns to center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form(key='login_form'):
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label="Log In")
    
    if submit_button:
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid username or password.")

# ---------- MAIN APPLICATION (after login) ----------
else:
    # Function to load data
    def load_data():
        if os.path.exists(PATIENT_DB):
            df_patients = pd.read_csv(PATIENT_DB)
        else:
            df_patients = pd.DataFrame()
    
        if os.path.exists(DOCTOR_SCHEDULE):
            df_schedule = pd.read_excel(DOCTOR_SCHEDULE)
        else:
            df_schedule = pd.DataFrame()
        
        return df_patients, df_schedule

    df_patients, df_schedule = load_data()

    # Log out button
    if st.sidebar.button("Log Out"):
        st.session_state.authenticated = False
        st.session_state.clear()
        st.rerun()

    # ---------- SIDEBAR NAVIGATION ----------
    st.sidebar.title("Navigation")
    section = st.sidebar.radio("Go to", ["📅 Book Appointment", "🗂 Upcoming Bookings", "✅ Available Slots"])

    # ---------- BOOK APPOINTMENT ----------
    if section == "📅 Book Appointment":
        st.title("📅 Book an Appointment")

        # Step 1: Patient Information
        st.subheader("Step 1: Patient Information")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name*")

            # Reframed Date of Birth Section
            st.write("**Date of Birth***")
            today = date.today()
            year_range = list(range(today.year, today.year - 120, -1))
            col_dob1, col_dob2, col_dob3 = st.columns(3)
            with col_dob1:
                dob_day = st.selectbox("Day", list(range(1, 32)))
            with col_dob2:
                dob_month = st.selectbox("Month", list(range(1, 13)), format_func=lambda x: date(2000, x, 1).strftime('%B'))
            with col_dob3:
                dob_year = st.selectbox("Year", year_range)
            
            # Combine the date components
            try:
                dob = date(dob_year, dob_month, dob_day)
            except ValueError:
                dob = None # Handle invalid dates like Feb 30th
            
            doctor = st.selectbox("Choose Doctor*", df_schedule["Doctor"].unique() if not df_schedule.empty else [])
            location = st.text_input("Clinic Location*")
        with col2:
            email = st.text_input("Email (optional)")
            phone = st.text_input("Phone (optional)")
            insurance_carrier = st.selectbox("Insurance Carrier", ["", "Aetna", "BlueCross", "Cigna", "UnitedHealthcare", "Medicare"])
            member_id = st.text_input("Insurance Member ID")
            group_number = st.text_input("Group Number")

        if st.button("Check Patient Status"):
            if not name or not location or not dob:
                st.error("Please fill all required fields marked with *")
            else:
                match = df_patients[df_patients['Name'].str.lower() == name.lower()]
                if not match.empty:
                    st.success(f"Returning patient found: {match.iloc[0]['Name']}")
                    st.session_state['patient_type'] = "Returning"
                    st.session_state['duration'] = 30
                else:
                    st.info("New patient detected.")
                    st.session_state['patient_type'] = "New"
                    st.session_state['duration'] = 60

                st.session_state.update({
                    'patient_name': name,
                    'doctor': doctor,
                    'location': location,
                    'dob': dob,
                    'email': email,
                    'phone': phone,
                    'insurance_carrier': insurance_carrier,
                    'member_id': member_id,
                    'group_number': group_number
                })

        # Step 2: Appointment Slot
        if "patient_type" in st.session_state:
            st.subheader("Step 2: Choose Appointment Slot")
            if not df_schedule.empty:
                available_dates = df_schedule[df_schedule["Doctor"] == st.session_state['doctor']]["Date"].unique()
                chosen_date = st.selectbox("Select Date", available_dates)

                filtered_slots = df_schedule[
                    (df_schedule["Doctor"] == st.session_state['doctor']) &
                    (df_schedule["Date"] == chosen_date) &
                    (df_schedule["Status"] == "Available")
                ]

                if not filtered_slots.empty:
                    chosen_time = st.selectbox("Select Time", filtered_slots["Time"].unique())
                    if st.button("Confirm Booking"):
                        idx = df_schedule[
                            (df_schedule["Doctor"] == st.session_state['doctor']) &
                            (df_schedule["Date"] == chosen_date) &
                            (df_schedule["Time"] == chosen_time)
                        ].index
                        df_schedule.loc[idx, "Status"] = "Booked"
                        df_schedule.to_excel(DOCTOR_SCHEDULE, index=False)

                        st.success(f"✅ Appointment confirmed for {st.session_state['patient_name']} "
                                   f"with {st.session_state['doctor']} on {chosen_date} at {chosen_time}")

                        new_entry = pd.DataFrame([{
                            "Patient Name": st.session_state['patient_name'],
                            "DOB": st.session_state['dob'],
                            "Patient Type": st.session_state['patient_type'],
                            "Doctor": st.session_state['doctor'],
                            "Location": st.session_state['location'],
                            "Date": chosen_date,
                            "Time": chosen_time,
                            "Duration (min)": st.session_state['duration'],
                            "Email": st.session_state['email'],
                            "Phone": st.session_state['phone'],
                            "Insurance Carrier": st.session_state['insurance_carrier'],
                            "Member ID": st.session_state['member_id'],
                            "Group Number": st.session_state['group_number']
                        }])

                        if os.path.exists(ALL_APPOINTMENTS_FILE):
                            existing_df = pd.read_excel(ALL_APPOINTMENTS_FILE)
                            updated_df = pd.concat([existing_df, new_entry], ignore_index=True)
                        else:
                            updated_df = new_entry

                        updated_df.to_excel(ALL_APPOINTMENTS_FILE, index=False)

                        excel_buffer = io.BytesIO()
                        updated_df.to_excel(excel_buffer, index=False)
                        excel_buffer.seek(0)
                        st.download_button(
                            label="⬇️ Download All Appointments",
                            data=excel_buffer,
                            file_name="all_appointments.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                else:
                    st.warning("No available slots for the selected date.")
            else:
                st.warning("Doctor schedule not found.")

    # ---------- UPCOMING BOOKINGS ----------
    elif section == "🗂 Upcoming Bookings":
        st.title("🗂 Upcoming Appointments")
        if os.path.exists(ALL_APPOINTMENTS_FILE):
            df = pd.read_excel(ALL_APPOINTMENTS_FILE)
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download CSV", csv, "upcoming_appointments.csv", "text/csv")
        else:
            st.info("No appointments file found yet.")

    # ---------- AVAILABLE SLOTS ----------
    elif section == "✅ Available Slots":
        st.title("✅ Available Slots")
        if not df_schedule.empty:
            doctor_choice = st.selectbox("Choose Doctor", df_schedule["Doctor"].unique())
            filtered_dates = df_schedule[
                (df_schedule["Doctor"] == doctor_choice) &
                (df_schedule["Status"] == "Available")
            ]["Date"].unique()
            if len(filtered_dates) > 0:
                chosen_date = st.selectbox("Choose Date", filtered_dates)
                available_df = df_schedule[
                    (df_schedule["Doctor"] == doctor_choice) &
                    (df_schedule["Date"] == chosen_date) &
                    (df_schedule["Status"] == "Available")
                ]
                if not available_df.empty:
                    st.subheader(f"Available Slots for {doctor_choice} on {chosen_date}")
                    st.dataframe(available_df, use_container_width=True)
                else:
                    st.info(f"No available slots for {doctor_choice} on {chosen_date}.")
            else:
                st.info(f"No available slots for {doctor_choice}.")
        else:
            st.warning("Doctor schedule file not found.")
