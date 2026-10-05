import webview

from room_data import ROOM_DATABASE
from calculator import build_report, build_room_entry
from email_report import send_email_report


class Api:
  def get_room_database(self):
    return ROOM_DATABASE

  def submit_quote(self, customer_info, rooms_payload):
    """rooms_payload: { room_name: { item_key: qty, ... }, ... }"""
    if not customer_info.get("full_name") or not customer_info.get("email"):
      return {"ok": False, "message": "Full name and email are required."}

    survey_data = {}
    for room_name, quantities in rooms_payload.items():
      items_data = ROOM_DATABASE.get(room_name)
      if not items_data:
        continue
      entry = build_room_entry(items_data, quantities)
      if entry:
        survey_data[room_name] = entry

    if not survey_data:
      return {"ok": False, "message": "Add at least one item before saving."}

    report_text = build_report(survey_data, customer_info)
    send_email_report(report_text, customer_info["email"])

    return {"ok": True, "report": report_text}


def main():
  api = Api()
  webview.create_window(
      "Removals Volume & Packing Calculator",
      "web/index.html",
      js_api=api,
      width=1100,
      height=800,
      min_size=(800, 600),
  )
  webview.start()


if __name__ == "__main__":
  main()
