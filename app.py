import streamlit as st

st.set_page_config(page_title="Agroforestry Carbon Credit Platform", layout="wide")

# --- Page 1: Introduction ---
def intro():
    st.title("🌱 Agroforestry Carbon Credit Platform")
    st.markdown("Welcome to the simplified platform that helps agroforestry project developers generate carbon credits under Verra's ARR methodology.")

    st.markdown("### 📊 Flow of the Platform")
    st.markdown("""
    1. **Understand the Project Flow**  
       → Learn how carbon credit projects work.

    2. **Provide Basic Project Information**  
       → Fill in only what's needed to auto-fill the PDD.

    3. **Estimate Carbon Credits**  
       → Get an estimate based on land, tree type, and duration.

    4. **Export Draft PDD or Save Session** (coming soon)
    """)

# --- Page 2: Collect User Inputs ---
def user_input():
    st.title("📝 Step 1: Provide Project Details")
    st.markdown("We'll ask for basic project information to pre-fill the PDD draft.")

    with st.form("project_form"):
        name = st.text_input("👤 Project Developer Name")
        location = st.text_input("📍 Project Location (District/State)")
        land_area = st.number_input("🌾 Total Land Area (hectares)", min_value=0.1, step=0.1)
        tree_density = st.slider("🌳 Tree Density (trees per hectare)", 100, 1000, 400, 50)
        start_year = st.number_input("🕒 Start Year of Project", min_value=2020, max_value=2100, value=2025)
        duration = st.slider("📆 Duration (Years)", 5, 40, 20)
        species = st.selectbox("🌿 Dominant Tree Species", ["Neem", "Bamboo", "Teak", "Poplar"])
        submit = st.form_submit_button("Generate Carbon Credit Estimate")

    if submit:
        st.session_state.update({
            "name": name,
            "location": location,
            "land_area": land_area,
            "tree_density": tree_density,
            "start_year": start_year,
            "duration": duration,
            "species": species,
        })
        st.success("Inputs saved! Go to the next tab to estimate credits.")

# --- Page 3: Carbon Credit Estimation ---
def carbon_estimator():
    st.title("📈 Step 2: Estimate Carbon Credits")

    if "land_area" not in st.session_state:
        st.warning("Please fill out the project details in Step 1.")
        return

    biomass_defaults = {
        "Neem": 10,
        "Bamboo": 5,
        "Teak": 12,
        "Poplar": 8,
    }

    # Use session data
    land_area = st.session_state["land_area"]
    tree_density = st.session_state["tree_density"]
    duration = st.session_state["duration"]
    species = st.session_state["species"]

    biomass_per_tree = biomass_defaults.get(species, 8)
    total_trees = land_area * tree_density
    total_biomass = total_trees * (biomass_per_tree * (duration / 10))  # Linear scale
    carbon = total_biomass * 0.47
    co2eq = carbon * 3.67
    buffer_deduction = co2eq * 0.22
    usable_credits = co2eq - buffer_deduction

    st.markdown(f"### Results for **{land_area} ha** of land planted with **{species}** over **{duration} years**:")
    st.metric("🌲 Total Biomass (tons)", f"{total_biomass:,.0f}")
    st.metric("🧪 Carbon Content (tons)", f"{carbon:,.0f}")
    st.metric("💨 Estimated CO₂e Sequestered", f"{co2eq:,.0f} tCO₂e")
    st.metric("🔒 After Buffer (22%)", f"{usable_credits:,.0f} Verified Credits")

    st.caption("Estimates based on default IPCC biomass factors and linear growth. For real registration, Verra validation is required.")

# Navigation
tabs = {
    "1️⃣ Introduction": intro,
    "2️⃣ Project Info": user_input,
    "3️⃣ Estimate Credits": carbon_estimator
}

tab = st.sidebar.radio("Navigate", list(tabs.keys()))
tabs[tab]()
