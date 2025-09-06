# 🏥 Patient Care-Pro
**AI-Powered Appointment Scheduling System**

Patient Care-Pro is a lightweight, user-friendly appointment scheduling system designed for small to mid-sized clinics.  
It helps clinic staff manage bookings, prevent scheduling conflicts, and maintain a clear log of appointments — all through a clean, web-based interface.

---

## ✨ Features
- **Book Appointments:**  
  Book slots for new or returning patients, with dynamic appointment durations:
  - **New patients:** 60 minutes  
  - **Returning patients:** 30 minutes

- **Real-Time Slot Management:**  
  Doctor availability is updated instantly. Booked slots are immediately marked to prevent double bookings.

- **Upcoming Appointments:**  
  View all confirmed appointments in one place with an option to **export data** to Excel or CSV.

- **Available Slots by Doctor & Date:**  
  Filter by doctor and date to quickly see which slots are open.

- **Insurance Handling:**  
  Capture patient insurance details such as carrier, member ID, and group number.

- **Simple Data Integration:**  
  Works directly with Excel and CSV files — no database setup required.

---

## 🗂 Folder Structure
Patient-Care-Pro/
│
├── app.py # Main Streamlit app
├── requirements.txt # Python dependencies
├── doctor_schedule.xlsx # Sample doctor schedule
├── patient_database.csv # Sample patient database
├── all_appointments.xlsx # Auto-generated after first booking
├── New Patient Intake Form.pdf # Reference patient intake form
└── README.md # Project documentation


---

## 🚀 Getting Started

Follow these steps to set up and run the application locally:

### **1. Prerequisites**
- Python 3.8 or above installed
- Internet connection (for installing dependencies)

### **2. Installation**

# Navigate to the project folder
cd Patient-Care-Pro

# Install dependencies
pip install -r requirements.txt

### **3. Run the Application**
streamlit run app.py

📂## 📂 Data Files Overview
| **File**                  | **Purpose** |
|---------------------------|-------------|
| **doctor_schedule.xlsx**  | Holds doctor availability and booked slots. |
| **patient_database.csv**  | Stores basic patient details for identifying new vs returning patients. |
| **all_appointments.xlsx** | Maintains a master log of confirmed bookings (auto-generated). |
| **New Patient Intake Form.pdf** | Sample form for patient data collection. |

---

## 🔐 Sample Login Credentials
| **Username** | **Password** |
|--------------|--------------|
| admin        | admin123     |

---

## 🧪 Testing Instructions
1. **Book a new appointment** using sample data.
2. **Verify the following:**
   - The chosen slot is marked as **Booked** in `doctor_schedule.xlsx`.
   - The new booking appears in `all_appointments.xlsx`.
   - The **Upcoming Bookings** tab displays the updated list.
3. Use the **Export** button to confirm it generates a valid CSV/Excel file.

---

## 🛠 Tech Stack
- **Frontend:** Streamlit  
- **Backend Logic:** Python  
- **Data Storage:** Excel & CSV files (via Pandas and OpenPyXL)

---

## 🙌 Acknowledgments
Developed as part of an internship assignment to demonstrate **AI agent workflows** for healthcare scheduling.

