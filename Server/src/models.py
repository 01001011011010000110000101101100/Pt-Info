from pydantic import BaseModel

from typing import Optional

class Patient(BaseModel):
    Bed_Number: str
    Name: str
    NID: str = ""
    Specialist: str = ""
    Diet: str = ""
    Respiration_System: str = ""
    Diagnosis: str = ""
    Consultation: str = ""

class DeletePatient(BaseModel):
    Bed_Number: str