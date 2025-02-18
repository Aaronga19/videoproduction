import uuid

def generate_folio_uuid():
  """Genera un folio único usando UUID."""
  uid =  str(uuid.uuid4()).split("-")[0:2]
  new_uid = "-".join(uid).upper()
  return new_uid

def generate_folio(date:str):
  uid = generate_folio_uuid()
  folio = f"C{date}-{uid}"
  return folio