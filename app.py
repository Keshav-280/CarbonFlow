import streamlit as st
from docxtpl import DocxTemplate
import tempfile
import os
from datetime import datetime

# Set page config
st.set_page_config(page_title="Agroforestry PDD Builder", layout="wide")
st.title("🌿 Agroforestry Project Design Document (PDD) Builder")
st.markdown("Please fill out each section with care. We’ll compile everything into a Verra-compatible document.")

# Navigation
sections = [
    "1️⃣ Project Identification", "2️⃣ Project Description", "3️⃣ Baseline Scenario",
    "4️⃣ Additionality", "5️⃣ Monitoring Plan", "6️⃣ Grouped Project Setup", "📄 Download Final PDD"
]
selected = st.sidebar.radio("🧭 Navigate to Section", sections)

# Form data holder
if "form_data" not in st.session_state:
    st.session_state.form_data = {}

# Helper for text input

def empathetic_input(label, key, **kwargs):
    st.session_state.form_data[key] = st.text_input(label, **kwargs)

def empathetic_area(label, key, **kwargs):
    st.session_state.form_data[key] = st.text_area(label, **kwargs)

def upload_input(label, key):
    uploaded = st.file_uploader(label, type=["jpg", "png", "jpeg", "pdf"])
    if uploaded:
        st.session_state.form_data[key] = uploaded.read()

# Sections
if selected == "1️⃣ Project Identification":
    st.subheader("📄 Project Identification")
    with st.form("id_form"):
        empathetic_input("🌱 What is the title of your project?", "project_title")
        empathetic_input("📍 Where is your project located? (District, State, Country)", "location")
        empathetic_area("🗺️ Share GPS coordinates or describe the project boundary.", "gps")
        empathetic_input("👥 Who are the key project proponents?", "proponents")
        st.session_state.form_data["start_year"] = st.number_input("📅 Start year of crediting period", value=2025)
        st.session_state.form_data["crediting_years"] = st.slider("⏳ Credit period (years)", 5, 40, 20)
        empathetic_input("📘 Methodology used (e.g., VM0047)", "methodology")
        st.form_submit_button("💾 Save Section")

elif selected == "2️⃣ Project Description":
    st.subheader("🌾 Project Description")
    with st.form("desc_form"):
        empathetic_area("📖 Tell us about the land-use history.", "land_history")
        empathetic_area("🚜 What project activities will you undertake?", "project_activities")
        empathetic_input("🌳 What species will be planted?", "species")
        empathetic_area("💬 What are the expected social benefits?", "social_benefits")
        empathetic_area("🌍 What are the expected environmental benefits?", "env_benefits")
        st.form_submit_button("💾 Save Section")

elif selected == "3️⃣ Baseline Scenario":
    st.subheader("📉 Baseline Scenario")
    with st.form("baseline_form"):
        empathetic_area("🧾 What would happen without the project?", "baseline_desc")
        empathetic_area("📚 Provide evidence or land-use history.", "evidence")
        upload_input("📸 Upload proof of degradation (photo, map, etc.)", "degradation_image")
        st.form_submit_button("💾 Save Section")

elif selected == "4️⃣ Additionality":
    st.subheader("🧮 Additionality")
    with st.form("add_form"):
        empathetic_area("🤔 Why wouldn't this happen without carbon finance?", "why_additional")
        st.session_state.form_data["legal_barriers"] = st.selectbox("📜 Is the project legally required?", ["No", "Yes", "Not Sure"])
        empathetic_area("🛠️ Financial or technical barriers", "financial_barriers")
        st.form_submit_button("💾 Save Section")

elif selected == "5️⃣ Monitoring Plan":
    st.subheader("🔍 Monitoring Plan")
    with st.form("monitoring_form"):
        empathetic_area("📊 How will project progress be monitored?", "monitoring_method")
        empathetic_area("📈 What data will be collected?", "data_collected")
        st.session_state.form_data["monitoring_freq"] = st.selectbox("📅 Monitoring Frequency", ["Annually", "Every 2 years", "Other"])
        empathetic_input("🔧 Tools used (satellite, drone, etc.)", "tools_used")
        st.form_submit_button("💾 Save Section")

elif selected == "6️⃣ Grouped Project Setup":
    st.subheader("📂 Grouped Project Setup")
    with st.form("group_form"):
        st.session_state.form_data["multi_farmers"] = st.selectbox("👨‍🌾 Are multiple farmers involved?", ["Yes", "No"])
        empathetic_area("📌 How will new plots/farmers be added?", "expansion_plan")
        empathetic_area("🗂️ How is land organized or aggregated?", "aggregation_method")
        st.form_submit_button("💾 Save Section")

elif selected == "📄 Download Final PDD":
    st.subheader("📥 Download Final PDD")
    with st.spinner("Generating your document..."):
        doc = DocxTemplate("template_pdd.docx")  # You need to provide a docx template with Jinja2-style fields
        context = st.session_state.form_data

        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            doc.render(context)
            doc.save(tmp.name)
            with open(tmp.name, "rb") as f:
                st.download_button(
                    "📄 Download Your PDD",
                    data=f.read(),
                    file_name="Agroforestry_PDD.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        os.unlink(tmp.name)

# Optional debug
st.markdown("---")
if st.checkbox("📋 Show Collected Data"):
    st.json(st.session_state.form_data)
