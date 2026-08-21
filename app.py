# app.py
"""
EcoNova: Smart Waste Management Ecosystem
"""

import copy
import streamlit as st
import folium
from streamlit_folium import st_folium
import logic
import data

st.set_page_config(
    page_title="EcoNova • Smart Waste Ecosystem",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# STYLING
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
.bin-card {
    border-radius: 14px;
    padding: 16px 20px;
    margin: 14px 0;
    display: flex;
    align-items: center;
    gap: 14px;
}

[data-testid="stSidebar"] .stButton > button {
    border-radius: 10px;
    font-weight: 600;
    text-align: left;
    justify-content: flex-start;
    margin-bottom: 4px;
}

#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# STATE INITIALIZATION
# ─────────────────────────────────────────────────────────────────────────────
if "citizens" not in st.session_state:
    st.session_state.citizens = copy.deepcopy(data.citizens)
if "hotspots" not in st.session_state:
    st.session_state.hotspots = copy.deepcopy(data.hotspots)
if "active_nav" not in st.session_state:
    st.session_state.active_nav = "scan"
if "active_user_name" not in st.session_state:
    st.session_state.active_user_name = st.session_state.citizens[0]["name"]
if "detected_result" not in st.session_state:
    st.session_state.detected_result = None

current_user = next((c for c in st.session_state.citizens if c["name"] == st.session_state.active_user_name), st.session_state.citizens[0])

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding-bottom: 10px;">
      <div style="font-size: 1.5rem; font-weight: 800; color: #10B981;">🌱 EcoNova</div>
      <div style="font-size: 0.82rem; color: #64748B;">Smart City Waste Network • Pune</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex; gap:8px; margin-bottom: 16px;">
      <span style="background:rgba(16,185,129,0.15); color:#059669; border-radius:99px; padding:3px 10px; font-size:0.75rem; font-weight:700;">🟢 Grid Active</span>
      <span style="background:rgba(245,158,11,0.15); color:#D97706; border-radius:99px; padding:3px 10px; font-size:0.75rem; font-weight:700;">🔥 4-Day Streak</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-size:0.72rem; font-weight:700; color:#94A3B8; text-transform:uppercase;'>Navigation</p>", unsafe_allow_html=True)

    nav_items = [
        ("📸 Scan Waste (AI Vision)", "scan"),
        ("🎬 Eco Shorts Feed", "eco"),
        ("📍 Community & Driver GIS Map", "community"),
        ("🏠 System Overview", "home"),
    ]

    for label, key in nav_items:
        is_active = (st.session_state.active_nav == key)
        if st.button(label, key=f"nav_{key}", use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state.active_nav = key
            st.rerun()

    st.divider()

    st.markdown("<p style='font-size:0.72rem; font-weight:700; color:#94A3B8; text-transform:uppercase;'>Citizen Authentication</p>", unsafe_allow_html=True)
    with st.expander("👤 Switch Account / Sign In", expanded=False):
        user_names = [c["name"] for c in st.session_state.citizens]
        curr_idx = user_names.index(st.session_state.active_user_name) if st.session_state.active_user_name in user_names else 0
        switch_acc = st.selectbox("Select Existing Citizen", user_names, index=curr_idx)
        if switch_acc != st.session_state.active_user_name:
            st.session_state.active_user_name = switch_acc
            st.session_state.detected_result = None
            st.rerun()

        st.markdown("---")
        st.markdown("**Register New Household:**")
        new_name = st.text_input("Full Name", placeholder="e.g. Priya Deshmukh")
        new_neigh = st.text_input("Society / Area", placeholder="e.g. Baner, Sector 2")
        if st.button("➕ Create & Login", use_container_width=True):
            if new_name.strip():
                new_profile = {
                    "id": f"c{len(st.session_state.citizens)+1}",
                    "name": new_name.strip(),
                    "neighborhood": new_neigh.strip() or "Pune Central",
                    "points": 0,
                    "streak": 1,
                    "badge": "🌱 Seedling Scout",
                    "co2_total": 0.0,
                }
                st.session_state.citizens.append(new_profile)
                st.session_state.active_user_name = new_name.strip()
                st.toast(f"Welcome {new_name}! Logged in.", icon="🌱")
                st.rerun()

    st.metric("EcoPoints", f"{current_user['points']} XP")
    st.metric("Lifetime CO₂ Saved", f"{current_user['co2_total']:.1f} kg")
    st.caption(f"🎖️ Habit Rank: **{current_user['badge']}**")

# ─────────────────────────────────────────────────────────────────────────────
# HEADER BAR
# ─────────────────────────────────────────────────────────────────────────────
headers = {
    "scan": "📸 AI Waste Scanner & Real-Time Carbon Offset",
    "eco": "🎬 Eco Shorts: Civic Awareness Feed",
    "community": "📍 Municipal Hotspots & Driver Dispatch GIS",
    "home": "🏠 EcoNova Smart City Overview"
}

st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 20px; border-bottom: 1px solid #E2E8F0; padding-bottom: 12px;">
  <div>
    <h2 style="margin:0; font-weight:800; font-size:1.5rem;">{headers.get(st.session_state.active_nav, 'EcoNova')}</h2>
    <span style="color:#64748B; font-size:0.85rem;">Active Citizen: <b>{current_user['name']}</b> ({current_user['neighborhood']})</span>
  </div>
  <div>
    <span style="background:#ECFDF5; color:#059669; border:1px solid #A7F3D0; font-weight:700; padding:6px 14px; border-radius:99px; font-size:0.85rem;">⚡ {current_user['points']} XP</span>
  </div>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# SCREEN 1: SCAN WASTE
# =============================================================================
if st.session_state.active_nav == "scan":
    c_left, c_right = st.columns([1, 1], gap="large")

    with c_left:
        st.markdown("### 📸 Point Camera or Upload Photo")
        mode = st.radio("Capture Mode:", ["Live Webcam Snap", "Upload Photo File", "Quick Demo Presets"], horizontal=True)

        img_data = None
        if mode == "Live Webcam Snap":
            cam = st.camera_input("Point camera at your item (Center the object)")
            if cam:
                img_data = cam.getvalue()
        elif mode == "Upload Photo File":
            up = st.file_uploader("Upload waste image", type=["png", "jpg", "jpeg"])
            if up:
                img_data = up.getvalue()
                st.image(up, use_container_width=True)
        else:
            preset = st.selectbox("Select Preset Demo Item:", [
                "E-Waste (Computer Mouse / Cable / Hardware)",
                "Stainless Steel / Metal Water Bottle",
                "PET Plastic Bottle (Clean Recyclable)",
                "Cardboard Box Packaging",
                "Organic Food Scraps"
            ])
            if "E-Waste" in preset:
                st.session_state.detected_result = {"category": "E-Waste", "label": "E-Waste / Tech Hardware (Computer Peripheral / Gadget)", "confidence": 97.6, "tip": logic.SORTING_TIPS["E-Waste"], "auto_weight": 0.25, "bin_info": logic.get_bin_info("E-Waste")}
            elif "Metal" in preset:
                st.session_state.detected_result = {"category": "Metal", "label": "Metal & Aluminium (Stainless Steel / Can / Foil)", "confidence": 98.2, "tip": logic.SORTING_TIPS["Metal"], "auto_weight": 0.30, "bin_info": logic.get_bin_info("Metal")}
            elif "Plastic" in preset:
                st.session_state.detected_result = {"category": "Plastic", "label": "Synthetic Plastic / Packaging Container", "confidence": 95.8, "tip": logic.SORTING_TIPS["Plastic"], "auto_weight": 0.08, "bin_info": logic.get_bin_info("Plastic")}
            elif "Cardboard" in preset:
                st.session_state.detected_result = {"category": "Paper", "label": "Cardboard Box / Kraft Paper Packaging", "confidence": 95.0, "tip": logic.SORTING_TIPS["Paper"], "auto_weight": 0.20, "bin_info": logic.get_bin_info("Paper")}
            else:
                st.session_state.detected_result = {"category": "Organic", "label": "Organic & Wet Food Waste (Compostable)", "confidence": 94.5, "tip": logic.SORTING_TIPS["Organic"], "auto_weight": 0.40, "bin_info": logic.get_bin_info("Organic")}

        if img_data:
            st.session_state.detected_result = logic.analyze_waste_image(img_data)

        st.markdown("#### 🏷️ Classification Confirmation")
        cat_options = ["E-Waste", "Metal", "Plastic", "Paper", "Organic", "Glass", "Textiles", "Hazardous"]
        detected_cat = st.session_state.detected_result["category"] if st.session_state.detected_result else "E-Waste"
        chosen_cat = st.selectbox("Category Override (if needed):", cat_options, index=cat_options.index(detected_cat) if detected_cat in cat_options else 0)

        auto_w = logic.DEFAULT_CATEGORY_WEIGHTS.get(chosen_cat, 0.25)
        st.caption(f"⚖️ **Auto-Estimated Weight:** `{auto_w} kg` (Standard municipal average)")

        if st.button("🌱 Log Clean Segregation (+10 XP)", type="primary", use_container_width=True):
            impact = logic.calculate_carbon_impact(chosen_cat, auto_w)
            logic.update_citizen_score(current_user, is_correct=True)
            current_user["co2_total"] += impact["co2_saved_kg"]
            st.balloons()
            st.toast(f"Logged {chosen_cat}! +10 XP & {impact['co2_saved_kg']} kg CO₂ saved!", icon="🔥")
            st.rerun()

    with c_right:
        st.markdown("### 🌍 Real-Time AI Detection & Bin Segregation")
        if st.session_state.detected_result:
            res = st.session_state.detected_result
            st.success(f"✅ **AI Detection:** {res['label']} ({res['confidence']}% Confidence)")
            
            bin_meta = logic.get_bin_info(chosen_cat)
            st.markdown(f"""
            <div class="bin-card" style="background:{bin_meta['bg_color']}; border:1.5px solid {bin_meta['badge_color']};">
              <div style="font-size:2.2rem;">{bin_meta['icon']}</div>
              <div>
                <div style="font-size:0.75rem; font-weight:800; color:{bin_meta['badge_color']}; text-transform:uppercase; letter-spacing:0.06em;">
                  Required Disposal Bin ({bin_meta['bin_color']} Bin)
                </div>
                <div style="font-size:1.1rem; font-weight:800; color:#1E293B; margin-top:2px;">
                  {bin_meta['bin_name']}
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.info(f"💡 **Disposal Tip:** {logic.SORTING_TIPS.get(chosen_cat, 'Segregate cleanly.')}")
        else:
            st.info("👉 Hold an item in front of your camera or pick a preset to see immediate AI detection & required bin.")

        live_math = logic.calculate_carbon_impact(chosen_cat, auto_w)
        m1, m2, m3 = st.columns(3)
        m1.metric("CO₂e Avoided", f"{live_math['co2_saved_kg']} kg")
        m2.metric("Driving Offset", f"{live_math['km_offset']} km")
        m3.metric("Tree Absorption", f"{live_math['tree_days']} d")

        st.markdown(f"**Habit Tier:** {current_user['badge']}")
        st.progress(min(current_user["points"] / 300, 1.0), text=f"{current_user['points']} / 300 XP to Earth Champion")


# =============================================================================
# SCREEN 2: ECO SHORTS (OPEN ACCESS VIDEO FEEDS)
# =============================================================================
elif st.session_state.active_nav == "eco":
    col_reel, col_side = st.columns([1.3, 0.7], gap="large")

    with col_reel:
        st.markdown("""
        <div style="border: 1px solid #E2E8F0; border-radius: 16px; padding: 18px; margin-bottom: 16px; background:#F8FAFC;">
          <span style="background:#ECFDF5; color:#059669; border:1px solid #A7F3D0; border-radius:99px; padding:2px 10px; font-size:0.75rem; font-weight:700;">🌱 DIY Reuse</span>
          <h3 style="margin:8px 0 4px 0; color:#0F172A;">How 5 Plastic Bottles Become a Self-Watering Planter</h3>
          <p style="color:#64748B; font-size:0.85rem; margin-bottom:12px;">@rewild.pune • 30s Green Byte</p>
        </div>
        """, unsafe_allow_html=True)
        # Direct reliable WebM/MP4 stream that works in all browsers without embed blocks
        st.video("https://media.w3.org/2010/05/sintel/trailer.mp4")
        st.markdown("<div style='display:flex; gap:20px; margin-top:8px; color:#64748B; font-weight:600;'><span>❤️ 1,240</span><span>💬 86</span><span>↗️ Share</span><span>🔖 Save</span></div>", unsafe_allow_html=True)

        st.divider()

        st.markdown("""
        <div style="border: 1px solid #E2E8F0; border-radius: 16px; padding: 18px; margin-bottom: 16px; background:#F8FAFC;">
          <span style="background:#EFF6FF; color:#2563EB; border:1px solid #BFDBFE; border-radius:99px; padding:2px 10px; font-size:0.75rem; font-weight:700;">💡 Waste Facts</span>
          <h3 style="margin:8px 0 4px 0; color:#0F172A;">Why Aluminium Cans are 100% Infinitely Recyclable</h3>
          <p style="color:#64748B; font-size:0.85rem; margin-bottom:12px;">@zerowaste.lab • Pune Civic Initiative</p>
        </div>
        """, unsafe_allow_html=True)
        st.video("https://www.w3schools.com/html/mov_bbb.mp4")

    with col_side:
        st.markdown("### 🌿 Segregation Golden Rules")
        st.markdown("""
        * 🟢 **Green Bin**: Wet & Kitchen Food Waste
        * 🔵 **Blue Bin**: Dry Recyclables (Plastic, Paper, Metal, Glass)
        * ⚫ **Black Bin**: E-Waste Drop-off (Gadgets & Cables)
        * 🔴 **Red Bin**: Hazardous & Sanitary Items
        """)
        st.info("💡 **Did you know?** Recycling one aluminum can saves enough energy to run a TV for 3 hours!")


# =============================================================================
# SCREEN 3: GIS COMMUNITY MAP
# =============================================================================
elif st.session_state.active_nav == "community":
    map_col, form_col = st.columns([1.2, 0.8], gap="large")

    with map_col:
        st.markdown("### 📍 Municipal GIS Hotspot Map")
        pending_count = sum(1 for h in st.session_state.hotspots if h["status"] == "Pending")
        resolved_count = sum(1 for h in st.session_state.hotspots if h["status"] == "Resolved")
        st.caption(f"🔴 **{pending_count} Active Overflow Spots** | 🟢 **{resolved_count} Cleared Cleanups**")

        pune_map = folium.Map(location=[18.5204, 73.8567], zoom_start=13)
        for h in st.session_state.hotspots:
            is_pending = (h["status"] == "Pending")
            folium.Marker(
                location=[h["lat"], h["lng"]],
                popup=f"<b>{h['location']}</b><br>{h['waste_type']}<br>Status: {h['status']}",
                tooltip=h['location'],
                icon=folium.Icon(color="red" if is_pending else "green", icon="trash" if is_pending else "ok-sign", prefix="glyphicon")
            ).add_to(pune_map)

        st_folium(pune_map, height=450, width=None, returned_objects=[])

    with form_col:
        st.markdown("### 🚨 Post an Overflowing Spot")
        with st.form("post_hotspot_form", clear_on_submit=True):
            spot_name = st.text_input("Landmark / Location", "Kothrud Bus Stand Corner")
            waste_obs = st.selectbox("Waste Observed", ["Overflowing Plastic Bin", "Commercial Mixed Debris", "Illegal Open Dump", "E-Waste Scrap"])
            obs_notes = st.text_area("Notes", "Pile blocking pedestrian path.")
            c_lat = st.number_input("Latitude", value=18.5074, format="%.4f")
            c_lng = st.number_input("Longitude", value=73.8077, format="%.4f")
            if st.form_submit_button("📢 Upload Hotspot & Alert Drivers (+15 XP)", type="primary"):
                st.session_state.hotspots.append({
                    "id": f"H{len(st.session_state.hotspots)+1}",
                    "location": spot_name,
                    "lat": c_lat,
                    "lng": c_lng,
                    "waste_type": waste_obs,
                    "notes": obs_notes,
                    "status": "Pending",
                    "reported_by": current_user["name"]
                })
                logic.update_citizen_score(current_user, is_correct=True, bonus_xp=5)
                st.toast("Hotspot alert dispatched to drivers!", icon="🚚")
                st.rerun()

        st.markdown("### 🚚 Municipal Driver Action Queue")
        pending_hotspots = [h for h in st.session_state.hotspots if h["status"] == "Pending"]
        if not pending_hotspots:
            st.success("🎉 All hotspots in this sector are clear!")
        else:
            for h in pending_hotspots:
                with st.expander(f"🔴 {h['location']}"):
                    st.write(f"**Type:** {h['waste_type']} • **Reported By:** {h['reported_by']}")
                    if st.button("✅ Mark Picked Up", key=f"btn_clear_{h['id']}"):
                        h["status"] = "Resolved"
                        st.toast(f"Cleared {h['location']}!", icon="✅")
                        st.rerun()


# =============================================================================
# SCREEN 4: SYSTEM OVERVIEW
# =============================================================================
elif st.session_state.active_nav == "home":
    m1, m2, m3 = st.columns(3)
    m1.metric("EcoPoints Earned", f"{current_user['points']} XP")
    m2.metric("Active Streak", f"{current_user['streak']} Days 🔥")
    m3.metric("Total CO₂ Diverted", f"{current_user['co2_total']:.1f} kg")

    st.divider()
    st.markdown("### 🌿 Welcome to EcoNova Smart City Waste Network")
    st.write("EcoNova connects citizens, residential societies, and municipal collection crews to automate waste segregation, reward sustainable habits, and eliminate blind, fuel-heavy collection routes.")
