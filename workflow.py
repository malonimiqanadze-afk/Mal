from room_data import ROOM_DATABASE
from calculator import build_report
from email_report import send_email_report
from customer_info import collect_customer_info


def prompt_int(prompt, default=0):
  raw = input(prompt).strip()
  if not raw:
    return default
  try:
    value = int(raw)
  except ValueError:
    print("  Invalid number, using 0.")
    return 0
  return max(0, value)


def survey_room(room_name, items):
  answer = input(f"\nSurvey '{room_name}'? (y/N): ").strip().lower()
  if answer != "y":
    return None

  room_items = {}
  room_volume = 0
  for item_key, vol in items.items():
    name = item_key.replace("_", " ").title()
    qty = prompt_int(f"  {name} ({vol} FT³) qty [0]: ")
    if qty > 0:
      room_items[item_key] = {"qty": qty, "subtotal": qty * vol}
      room_volume += qty * vol

  comment = input("  Notes (fragile items, tight access, etc.) []: ").strip()

  if not room_items and not comment:
    return None

  return {"items": room_items, "volume": room_volume, "comment": comment}


def main():
  print("Removals Company Estimate & Volume Calculator")
  print("Answer the prompts for each room you want to survey.\n")

  customer_info = collect_customer_info()

  survey_data = {}
  for room_name, items in ROOM_DATABASE.items():
    result = survey_room(room_name, items)
    if result is not None:
      survey_data[room_name] = result
      print(f"  Saved {room_name}! Subtotal: {result['volume']} FT³")

  if not survey_data:
    print("\nNo rooms surveyed. Nothing to report.")
    return

  report_text = build_report(survey_data, customer_info)
  print("\n" + report_text)

  send_email_report(report_text, customer_info["email"])


if __name__ == "__main__":
  main()
