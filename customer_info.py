def prompt_required(prompt):
  while True:
    value = input(prompt).strip()
    if value:
      return value
    print("  This field is required.")


def collect_customer_info():
  print("Save & get your reference")
  full_name = prompt_required("Full name *: ")
  email = prompt_required("Email *: ")
  phone = input("Phone []: ").strip()
  move_date = input("Move date (mm/dd/yyyy) []: ").strip()
  postcode_from = input("Moving from (postcode) []: ").strip()
  postcode_to = input("Moving to (postcode) []: ").strip()
  access_notes = input("Access notes (stairs, lift, parking) []: ").strip()

  return {
      "full_name": full_name,
      "email": email,
      "phone": phone,
      "move_date": move_date,
      "postcode_from": postcode_from,
      "postcode_to": postcode_to,
      "access_notes": access_notes,
  }
