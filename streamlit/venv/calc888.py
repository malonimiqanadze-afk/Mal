import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Removals Volume & Packing Calculator",
    page_icon="🚚",
    layout="wide",
)

# --- DATABASE ---
ROOM_DATABASE = {
    "Hallway": {
        "shoe_rack": 15,
        "coat_stand": 10,
        "console_table": 18,
        "hallway_mirror": 8,
        "small_storage_bench": 20,
    },
    "Bedroom 1 (Master)": {
        "bed_frame_queen": 45,
        "mattress_queen": 50,
        "wardrobe_3_door": 85,
        "dresser": 45,
        "nightstand": 7,
        "vanity_table": 30,
    },
    "Bedroom 2": {
        "bed_frame_queen": 45,
        "mattress_queen": 50,
        "wardrobe_2_door": 50,
        "dresser": 40,
        "nightstand": 7,
    },
    "Bedroom 3": {
        "bed_frame_single": 25,
        "mattress_single": 25,
        "wardrobe_2_door": 50,
        "nightstand": 7,
        "chest_of_drawers": 35,
    },
    "Bedroom 4": {
        "bed_frame_single": 25,
        "mattress_single": 25,
        "wardrobe_2_door": 50,
        "nightstand": 7,
    },
    "Bedroom 5": {
        "bed_frame_single": 25,
        "mattress_single": 25,
        "small_cabinet": 20,
        "nightstand": 7,
    },
    "Living Room / Lounge": {
        "sofa_3_seater": 62,
        "sofa_2_seater": 40,
        "sectional_sofa": 105,
        "armchair": 25,
        "coffee_table": 14,
        "tv_stand": 28,
        "bookshelf": 45,
        "side_table": 8,
        "large_houseplant": 20,
    },
    "Kitchen & Dining": {
        "dining_table_large": 55,
        "dining_table_small": 38,
        "dining_chair": 7,
        "sideboard": 55,
        "refrigerator_large": 65,
        "refrigerator_standard": 38,
        "washing_machine_dryer": 22,
        "dishwasher": 20,
        "small_appliance": 7,
    },
    "Office": {
        "office_desk_large": 45,
        "office_desk_standard": 25,
        "office_chair": 18,
        "filing_cabinet": 28,
        "electronics_pc": 10,
    },
    "Garage": {
        "workbench": 45,
        "tool_chest": 30,
        "ladder": 15,
        "bicycle": 20,
        "lawn_mower": 25,
        "heavy_shelving_unit": 35,
    },
    "Storage": {
        "plastic_storage_box_large": 12,
        "suitcases_set": 15,
        "extra_shelving": 30,
        "miscellaneous_boxes_stack": 40,
    },
    "Garden": {
        "garden_table": 30,
        "garden_chair": 8,
        "parasol_umbrella": 12,
        "bbq_grill": 25,
        "flower_pots_planters": 15,
    },
}

# --- SESSION STATE INITIALIZATION ---
if "survey_data" not in st.session_state:
  st.session_state.survey_data = {}

# --- APP HEADER ---
st.title("🚚 Removals Company Estimate & Volume Calculator")
st.markdown(
    "Select rooms from the sidebar, input item quantities, add notes, and"
    " generate a professional volume & truck size report instantly."
)

# --- SIDEBAR NAVIGATION WITH DYNAMIC COMPLETION INDICATORS ---
st.sidebar.header("🏠 Room Navigation")

completed_rooms = list(st.session_state.survey_data.keys())

# Build dynamic labels for selectbox showing checkmarks for completed rooms
room_options = list(ROOM_DATABASE.keys())
formatted_options = []
for room in room_options:
  if room in completed_rooms:
    vol = st.session_state.survey_data[room]["volume"]
    formatted_options.append(f"✅ {room} ({vol} FT³)")
  else:
    formatted_options.append(f"⏳ {room} (Pending)")

selected_display = st.sidebar.selectbox(
    "Choose Room to Survey:", formatted_options
)
# Clean up selection string to match dictionary key
selected_room = selected_display.split(" (")[0].replace("✅ ", "").replace(
    "⏳ ", ""
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Completed Rooms:** {len(completed_rooms)} / {len(ROOM_DATABASE)}")
for r in completed_rooms:
  st.sidebar.text(
      f"• {r}: {st.session_state.survey_data[r]['volume']} FT³"
  )

# --- MAIN SURVEY AREA ---
st.header(f"Surveying: {selected_room}")

existing_room_data = st.session_state.survey_data.get(
    selected_room, {"items": {}, "comment": ""}
)

with st.form(key=f"form_{selected_room}"):
  st.subheader("📦 Item Quantities")
  col1, col2 = st.columns(2)

  room_items_input = {}
  items_list = list(ROOM_DATABASE[selected_room].items())
  half = (len(items_list) + 1) // 2

  with col1:
    for item_key, vol in items_list[:half]:
      readable_name = item_key.replace("_", " ").title()
      default_qty = (
          existing_room_data["items"].get(item_key, {}).get("qty", 0)
      )
      room_items_input[item_key] = st.number_input(
          f"{readable_name} ({vol} FT³)",
          min_value=0,
          value=default_qty,
          step=1,
      )

  with col2:
    for item_key, vol in items_list[half:]:
      readable_name = item_key.replace("_", " ").title()
      default_qty = (
          existing_room_data["items"].get(item_key, {}).get("qty", 0)
      )
      room_items_input[item_key] = st.number_input(
          f"{readable_name} ({vol} FT³)",
          min_value=0,
          value=default_qty,
          step=1,
      )

  st.subheader("💬 Room Notes / Comments")
  room_comment_input = st.text_area(
      f"Special instructions for {selected_room} (e.g., fragile items, tight"
      " access):",
      value=existing_room_data["comment"],
  )

  col_save, _ = st.columns([1, 4])
  submitted = col_save.form_submit_button("💾 Save Room")

  if submitted:
    room_vol = 0
    saved_items = {}
    for item_key, qty in room_items_input.items():
      if qty > 0:
        vol = ROOM_DATABASE[selected_room][item_key]
        saved_items[item_key] = {"qty": qty, "subtotal": qty * vol}
        room_vol += qty * vol

    if saved_items or room_comment_input.strip():
      st.session_state.survey_data[selected_room] = {
          "items": saved_items,
          "volume": room_vol,
          "comment": room_comment_input.strip(),
      }
      st.success(f"Successfully saved {selected_room}! Subtotal: {room_vol} FT³")
    elif selected_room in st.session_state.survey_data:
      del st.session_state.survey_data[selected_room]
      st.warning(f"Cleared {selected_room} as no items/notes were provided.")
    st.rerun()

st.markdown("---")

# --- COMPREHENSIVE OVERVIEW DASHBOARD & REPORT TAB ---
st.header("📊 Estimate Summary & Report Dashboard")

if not st.session_state.survey_data:
  st.info(
      "No rooms surveyed yet. Fill out items above and click **Save Room** to"
      " see the calculation dashboard."
  )
else:
  grand_total_volume = sum(
      data["volume"] for data in st.session_state.survey_data.values()
  )
  buffered_volume = grand_total_volume * 1.15
  total_rooms_counted = len(st.session_state.survey_data)

  # Box calculations
  small_boxes = total_rooms_counted * 8
  medium_boxes = total_rooms_counted * 12
  large_boxes = total_rooms_counted * 5
  wardrobe_boxes = max(2, total_rooms_counted)

  # Truck recommendation logic
  if buffered_volume <= 550:
    truck = "Small Van / 10-12 ft Box Truck (Studio / 1-Bed)"
  elif buffered_volume <= 1050:
    truck = "Medium Truck / 16-20 ft Box Truck (2-3 Bed House)"
  elif buffered_volume <= 1800:
    truck = "Large Truck / 24-26 ft Moving Lorry (4+ Bed House)"
  else:
    truck = "Extra Large / Multiple Vehicles Needed (Large Estate)"

  # Display Metrics in Beautiful Columns
  m1, m2, m3 = st.columns(3)
  m1.metric("Base Total Volume", f"{grand_total_volume:.1f} FT³")
  m2.metric("Buffered Volume (+15%)", f"{buffered_volume:.1f} FT³")
  m3.metric("Recommended Vehicle", truck)

  st.subheader("📦 Required Packing Materials Estimation")
  pm1, pm2, pm3, pm4 = st.columns(4)
  pm1.metric("Small Boxes (1.5 ft³)", f"~{small_boxes}")
  pm2.metric("Medium Boxes (3.0 ft³)", f"~{medium_boxes}")
  pm3.metric("Large Boxes (4.5 ft³)", f"~{large_boxes}")
  pm4.metric("Wardrobe Boxes", f"~{wardrobe_boxes}")

  st.subheader("📂 Detailed Itemized Room Breakdown")
  report_text_list = []
  report_text_list.append("==================================================")
  report_text_list.append("            REMOVALS ESTIMATE REPORT             ")
  report_text_list.append("==================================================")

  for room_name, data in st.session_state.survey_data.items():
    st.markdown(f"### 📂 {room_name} — *{data['volume']} FT³*")
    report_text_list.append(f"\n{room_name} (Subtotal: {data['volume']} FT³)")

    if data["comment"]:
      st.markdown(f"> **Notes:** {data['comment']}")
      report_text_list.append(f"    Notes: {data['comment']}")

    for item_key, details in data["items"].items():
      name = item_key.replace("_", " ").title()
      st.text(f"    • {name}: {details['qty']}x = {details['subtotal']} FT³")
      report_text_list.append(
          f"    - {name}: {details['qty']}x = {details['subtotal']} FT³"
      )

  report_text_list.append("\n--------------------------------------------------")
  report_text_list.append(f"Base Total Volume      : {grand_total_volume:.1f} FT³")
  report_text_list.append(f"Buffered Volume (+15%) : {buffered_volume:.1f} FT³")
  report_text_list.append(f"Recommended Vehicle    : {truck}")
  report_text_list.append(
      f"Packing Materials      : Small: {small_boxes}, Med: {medium_boxes},"
      f" Large: {large_boxes}, Wardrobe: {wardrobe_boxes}"
  )
  report_text_list.append("==================================================")

  full_report_string = "\n".join(report_text_list)

  # --- EMAIL & EXPORT SECTION ---
  st.markdown("---")
  st.subheader("✉️ Email Estimate Report")

  with st.expander("Click here to configure and send email report"):
    sender_email = st.text_input("Company Email Address")
    sender_password = st.text_input("App Password (16-digit)", type="password")
    recipient_email = st.text_input("Recipient Email Address")

    if st.button("🚀 Send Email Report"):
      if not sender_email or not sender_password or not recipient_email:
        st.error("Please fill in all email fields.")
      else:
        try:
          msg = MIMEMultipart()
          msg["From"] = sender_email
          msg["To"] = recipient_email
          msg["Subject"] = "Removals Volume & Packing Estimate Report"
          msg.attach(MIMEText(full_report_string, "plain"))

          server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
          server.login(sender_email, sender_password)
          server.sendmail(sender_email, recipient_email, msg.as_string())
          server.quit()
          st.success(f"Successfully emailed report to {recipient_email}!")
        except Exception as e:
          st.error(f"Failed to send email. Error: {e}")