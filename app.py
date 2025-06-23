import streamlit as st

st.set_page_config(page_title="Agroforestry PDD Builder", layout="wide")

st.title("🌿 Agroforestry Project Design Document (PDD) Builder")
st.markdown("Fill out each section to build your Verra-compatible PDD document.")

# Create section navigation
sections = ["1️⃣ Project Identification", "2️⃣ Project Description", "3️⃣ Baseline Scenario", 
            "4️⃣ Additionality", "5️⃣ Monitoring Plan", "6️⃣ Grouped Project Setup"]
selected = st.sidebar.radio("🧭 Go to Section", sections)

# Store form data in session_state
if "form_data" not in st.session_state:
    st.session_state.form_data = {}

# Section 1: Project Identification
if selected == "1️⃣ Project Identification":
    st.subheader("📄 Project Identification")
    with st.form("id_form"):
        st.session_state.form_data["project_title"] = st.text_input("Project Title")
        st.session_state.form_data["location"] = st.text_input("Project Location (District, State, Country)")
        st.session_state.form_data["gps"] = st.text_area("GPS Coordinates or Boundary Description")
        st.session_state.form_data["proponents"] = st.text_input("Project Proponents (Organizations, People)")
        st.session_state.form_data["start_year"] = st.number_input("Crediting Period Start Year", value=2025)
        st.session_state.form_data["crediting_years"] = st.slider("Crediting Period (years)", 5, 40, 20)
        st.session_state.form_data["methodology"] = st.text_input("Methodology Used (e.g., VM0047)")
        submitted = st.form_submit_button("Save Section")

# Section 2: Project Description
elif selected == "2️⃣ Project Description":
    st.subheader("🌾 Project Description")
    with st.form("desc_form"):
        st.session_state.form_data["land_history"] = st.text_area("Land-Use History (before the project)")
        st.session_state.form_data["project_activities"] = st.text_area("Project Activities (what will be done?)")
        st.session_state.form_data["species"] = st.text_input("Species to be Planted")
        st.session_state.form_data["social_benefits"] = st.text_area("Expected Social Benefits")
        st.session_state.form_data["env_benefits"] = st.text_area("Expected Environmental Benefits")
        submitted = st.form_submit_button("Save Section")

# Section 3: Baseline Scenario
elif selected == "3️⃣ Baseline Scenario":
    st.subheader("📉 Baseline Scenario")
    with st.form("baseline_form"):
        st.session_state.form_data["baseline_desc"] = st.text_area("What would happen without the project?")
        st.session_state.form_data["evidence"] = st.text_area("Evidence: images, land-use history, etc.")
        st.session_state.form_data["degradation_proof"] = st.text_area("Proof of Degraded Land")
        submitted = st.form_submit_button("Save Section")

# Section 4: Additionality
elif selected == "4️⃣ Additionality":
    st.subheader("🧮 Additionality")
    with st.form("add_form"):
        st.session_state.form_data["why_additional"] = st.text_area("Why wouldn't this project happen without carbon finance?")
        st.session_state.form_data["legal_barriers"] = st.selectbox("Is it required by law?", ["No", "Yes", "Not Sure"])
        st.session_state.form_data["financial_barriers"] = st.text_area("Financial or technical barriers")
        submitted = st.form_submit_button("Save Section")

# Section 5: Monitoring Plan
elif selected == "5️⃣ Monitoring Plan":
    st.subheader("🔍 Monitoring Plan")
    with st.form("monitoring_form"):
        st.session_state.form_data["monitoring_method"] = st.text_area("How will project progress be monitored?")
        st.session_state.form_data["data_collected"] = st.text_area("What data will be collected (tree survival, growth, etc.)?")
        st.session_state.form_data["monitoring_freq"] = st.selectbox("Monitoring Frequency", ["Annually", "Every 2 years", "Other"])
        st.session_state.form_data["tools_used"] = st.text_input("Tools used (satellite, drone, app, etc.)")
        submitted = st.form_submit_button("Save Section")

# Section 6: Grouped Project
elif selected == "6️⃣ Grouped Project Setup":
    st.subheader("📂 Grouped Project Setup")
    with st.form("group_form"):
        st.session_state.form_data["multi_farmers"] = st.selectbox("Are multiple farmers involved?", ["Yes", "No"])
        st.session_state.form_data["expansion_plan"] = st.text_area("How will new plots/farmers be added?")
        st.session_state.form_data["aggregation_method"] = st.text_area("How is land being aggregated/organized?")
        submitted = st.form_submit_button("Save Section")

# Display form data summary
st.markdown("---")
if st.button("📋 Show All Collected Data"):
    st.json(st.session_state.form_data)
