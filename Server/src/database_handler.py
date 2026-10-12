import aiofiles

import csv
import re
import os
import io

from models import Patient, DeletePatient

def get_data_dir() -> str:
    path = (os.environ.get("NURSE_DATA_DIR")
            or os.environ.get("FLET_APP_STORAGE_DATA")
            or os.path.dirname(os.path.abspath(__file__)))
    os.makedirs(path, exist_ok=True)
    return path

def banned_file() -> str:
    return os.path.join(get_data_dir(), "Banned.dat")

def init_csv(csv_file: str):
	output = io.StringIO()
	writer = csv.writer(output)

	writer.writerow(
		["Bed no.", "Pt.Name", "NID", "SP", "DIET", "RES", "Dx", "Cx"]
	)
	csv_content = output.getvalue()
	output.close()

	with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
		file.write(csv_content)

def get_csv_path() -> str:
  FILE = os.path.join(get_data_dir(), "nurse_data.csv")
  if not os.path.exists(FILE):
    init_csv(FILE)
  return FILE
    

def get_banned() -> set:
    FILE = banned_file()
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as file:
            rows = file.read()
        return {line.strip() for line in rows.splitlines() if line.strip()}
    with open(FILE, "w", encoding='utf-8'):
        pass
    return set()


async def ban(ip: str, banned_set: set):
  FILE = banned_file()
  banned_set.add(ip)
  async with aiofiles.open(FILE, "w", encoding="utf-8") as file:
    await file.write("\n".join(banned_set))


async def unban(ip: str, banned_set: set):
  if ip in banned_set:
    banned_set.remove(ip)
  FILE = banned_file()
  async with aiofiles.open(FILE, "w", encoding="utf-8") as file:
    await file.write("\n".join(banned_set))



# ------------ Files are used ---------
CSV_FILE = get_csv_path()

async def fetch_patients() -> list[list[str]]:
  if not os.path.exists(CSV_FILE):
    return []

  async with aiofiles.open(CSV_FILE, mode="r", encoding="utf-8") as file:
    content = await file.read()

  lines = content.splitlines()
  reader = csv.reader(lines)
  next(reader, None)

  all_rows: list[list[str]] = [row for row in reader if row]

  def bed_sort_key(row):
    bed = row[0]
    value = re.match(r"([A-Za-z]*)\s*(\d*)", bed)
    if value:
      letter = value.group(1).upper()
      number = int(value.group(2)) if value.group(2) else 0
      return (letter, number)
    return (bed, 0)

  all_rows.sort(key=bed_sort_key)
  return all_rows


async def insert_patient(patient: Patient) -> bool:
  async with aiofiles.open(CSV_FILE, mode="r", encoding="utf-8") as file:
    content = await file.read()

  lines = content.splitlines()
  reader = csv.reader(lines)
  rows = list(reader)

  for row in rows:
    if row and row[0].strip().upper() == patient.Bed_Number.strip().upper():
      return False

  output = io.StringIO()
  writer = csv.writer(output)
  for row in rows:
    if row:
      writer.writerow(row)

  writer.writerow([
      patient.Bed_Number,
      patient.Name,
      patient.NID,
      patient.Specialist,
      patient.Diet,
      patient.Respiration_System,
      patient.Diagnosis,
      patient.Consultation,
  ])

  csv_content = output.getvalue()
  output.close()

  async with aiofiles.open(
      CSV_FILE, mode="w", newline="", encoding="utf-8"
  ) as file:
    await file.write(csv_content)

  return True


async def alert_patient(patient: Patient) -> bool:
    async with aiofiles.open(CSV_FILE, mode='r', encoding='utf-8') as file:
        content = await file.read()

    lines = content.splitlines() # split the patient data to can read it as CSV data
    reader = csv.reader(lines) # Read data in Memory for better performance
    rows = list(reader) # Make a list of CSV data to can make iteration on it
    output = io.StringIO()
    writer = csv.writer(output)

    found: bool = False
    for row in rows:
      if row and row[0].strip().upper() == patient.Bed_Number:
        found = True
        writer.writerow([
          patient.Bed_Number,
          patient.Name, patient.NID,
          patient.Specialist,
          patient.Diet,
          patient.Respiration_System,
          patient.Diagnosis,
          patient.Consultation
        ])
      elif row:
        writer.writerow(row)

    if not found:
        return False

    csv_content = output.getvalue()
    output.close()
    async with aiofiles.open(CSV_FILE, mode='w', encoding='utf-8') as file:
        await file.write(csv_content)
    return True


async def delete_data(bed_number: str):
    async with aiofiles.open(CSV_FILE, mode='r', encoding='utf-8') as file:
        content = await file.read()

    lines = content.splitlines()
    reader = csv.reader(lines)
    rows = list(reader)

    output = io.StringIO()
    writer = csv.writer(output)

    for row in rows:
        if row and row[0] != bed_number:
            writer.writerow(row)

    csv_content = output.getvalue()
    output.close()

    async with aiofiles.open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        await file.write(csv_content)