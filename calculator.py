def recommend_truck(buffered_volume):
  if buffered_volume <= 550:
    return "Small Van / 10-12 ft Box Truck (Studio / 1-Bed)"
  if buffered_volume <= 1050:
    return "Medium Truck / 16-20 ft Box Truck (2-3 Bed House)"
  if buffered_volume <= 1800:
    return "Large Truck / 24-26 ft Moving Lorry (4+ Bed House)"
  return "Extra Large / Multiple Vehicles Needed (Large Estate)"


def build_report(survey_data, customer_info=None):
  grand_total_volume = sum(data["volume"] for data in survey_data.values())
  buffered_volume = grand_total_volume * 1.15
  total_rooms_counted = len(survey_data)

  small_boxes = total_rooms_counted * 8
  medium_boxes = total_rooms_counted * 12
  large_boxes = total_rooms_counted * 5
  wardrobe_boxes = max(2, total_rooms_counted)

  truck = recommend_truck(buffered_volume)

  lines = []
  lines.append("==================================================")
  lines.append("            REMOVALS ESTIMATE REPORT             ")
  lines.append("==================================================")

  if customer_info:
    lines.append("\nCustomer Information")
    lines.append(f"    Full Name     : {customer_info['full_name']}")
    lines.append(f"    Email         : {customer_info['email']}")
    if customer_info["phone"]:
      lines.append(f"    Phone         : {customer_info['phone']}")
    if customer_info["move_date"]:
      lines.append(f"    Move Date     : {customer_info['move_date']}")
    if customer_info["postcode_from"]:
      lines.append(f"    Moving From   : {customer_info['postcode_from']}")
    if customer_info["postcode_to"]:
      lines.append(f"    Moving To     : {customer_info['postcode_to']}")
    if customer_info["access_notes"]:
      lines.append(f"    Access Notes  : {customer_info['access_notes']}")

  for room_name, data in survey_data.items():
    lines.append(f"\n{room_name} (Subtotal: {data['volume']} FT³)")
    if data["comment"]:
      lines.append(f"    Notes: {data['comment']}")
    for item_key, details in data["items"].items():
      name = item_key.replace("_", " ").title()
      lines.append(f"    - {name}: {details['qty']}x = {details['subtotal']} FT³")

  lines.append("\n--------------------------------------------------")
  lines.append(f"Base Total Volume      : {grand_total_volume:.1f} FT³")
  lines.append(f"Buffered Volume (+15%) : {buffered_volume:.1f} FT³")
  lines.append(f"Recommended Vehicle    : {truck}")
  lines.append(
      f"Packing Materials      : Small: {small_boxes}, Med: {medium_boxes},"
      f" Large: {large_boxes}, Wardrobe: {wardrobe_boxes}"
  )
  lines.append("==================================================")

  return "\n".join(lines)
