import streamlit as st
import webbrowser
import pandas as pd
import pydeck as pdk

# ---------------- Simple hardcoded login ----------------
def login(username, password):
    return username == "ramya" and password == "babitha"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login page
if not st.session_state.logged_in:
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.success("✅ Login successful!")
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("❌ Invalid username or password.")
    st.stop()

# ---------------- Dashboard after login ----------------
st.title("🚮 Smart Waste Management Dashboard")
st.write(f"Welcome, **{st.session_state['username']}**!")

# Logout
if st.sidebar.button("🔓 Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---------------- Tabs ----------------
tabs = st.tabs([
    "📸 Waste Detection",
    "🧠 AI Summary",
    "📍 Location Mapping",
    "📊 Waste Heatmap",
    "🤖 Cleanup Bot"
])

# --------- TAB 1: Waste Detection --------------
with tabs[0]:
    st.header("📸 Waste Detection")
    st.write("Choose your model for waste detection:")
    option = st.selectbox("Select Model", ["--Select--", "User-Trained Model", "Pretrained API (like GPT/LLaMA)"])

    if option == "User-Trained Model":
        st.info("⚙️ Running User-trained Model on uploaded image...")
        img = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if img:
            st.image(img, use_column_width=True)
            st.success("✅ Detection result placeholder (User-trained model).")

    elif option == "Pretrained API (like GPT/LLaMA)":
        st.info("⚙️ Sending image/text to API for waste detection...")
        input_text = st.text_area("Describe the scene or paste image description")
        if st.button("Detect with API"):
            if input_text:
                st.success("🤖 GPT-based detection result placeholder.")
            else:
                st.warning("Please describe the image or scene first.")

# --------- TAB 2: AI Summary --------------------
with tabs[1]:
    st.header("🧠 AI Summary & Safety Precautions")
    desc = st.text_area("Describe the detected waste:")
    if st.button("Generate Precautions"):
        if desc:
            st.success("🛡️ Precaution: Wear gloves and mask. Dispose bio-waste separately.")
        else:
            st.warning("Please provide description of waste.")

# --------- TAB 3: Location Mapping --------------
with tabs[2]:
    st.header("📍 Location Mapping")
    location = st.text_input("Enter Location (City/Area)")

    if st.button("Map Waste Location"):
        if location:
            try:
                df = pd.DataFrame({'lat': [17.385044], 'lon': [78.486671]})  # Hyderabad fallback
                st.map(df)
                st.success(f"📍 Map centered on: {location} (mock coordinates)")
            except:
                st.warning("⚠️ Could not map accurately. Opening Google Maps.")
                webbrowser.open(f"https://www.google.com/maps/search/{location}")
        else:
            st.warning("Enter a location first.")

# --------- TAB 4: Waste Heatmap ------------------
with tabs[3]:
    st.header("📊 Waste Heatmap")
    area = st.text_input("Enter City/Area for heatmap")

    if st.button("Show Heatmap"):
        if area:
            try:
                # Dummy heatmap data
                df = pd.DataFrame({
                    'lat': [17.385, 17.390, 17.395],
                    'lon': [78.486, 78.490, 78.495],
                    'waste_level': [50, 80, 120]
                })
                st.pydeck_chart(pdk.Deck(
                    map_style='mapbox://styles/mapbox/light-v9',
                    initial_view_state=pdk.ViewState(
                        latitude=17.39,
                        longitude=78.49,
                        zoom=12,
                        pitch=50,
                    ),
                    layers=[
                        pdk.Layer(
                            'HeatmapLayer',
                            data=df,
                            get_position='[lon, lat]',
                            get_weight='waste_level',
                            radius=100,
                            threshold=0.3
                        )
                    ],
                ))
                st.success(f"🔴 Highlighted high waste zones in {area}")
            except:
                webbrowser.open(f"https://www.google.com/maps/search/{area}")
        else:
            st.warning("Please enter area to generate heatmap.")

# --------- TAB 5: Cleanup Bot -------------------
with tabs[4]:
    st.header("🤖 Cleanup Command Center")
    if st.button("Send Cleanup Bot"):
        st.success("🧹 Cleanup bot dispatched successfully!")
