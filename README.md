# Pt.info & Pt.Server: Medical Patient Management System

A comprehensive, asynchronous client-server application designed for hospital wards and medical professionals to manage patient records, track bed assignments, utilize medical shorthand, generate PDF reports with full Arabic text support, and monitor server security.

---

## Project Overview

The project is split into two primary components:
1. **The Client App (`main_temp.py`)**: A Flet-based user interface (`Pt.info`) allowing nurses and medical staff to input, edit, delete, and view patient bed logs, as well as export data into a neatly formatted PDF report.
2. **The Server & Dashboard (`api.py` & `main.py`)**: A FastAPI backend coupled with a desktop server dashboard (`Pt.Server`) that manages CSV-based persistence, handles client requests asynchronously, monitors connected/reactive IP addresses, and provides IP banning capabilities for security.

---

## File Structure & Architecture

* **`main_temp.py`**: The primary client-side Flet application. Manages form inputs (Bed No., Name, NID, Specialist, Diet, Respiration, Diagnosis, Consultation), communicates with the backend API via `httpx`, and handles client-side PDF compilation and file sharing.
* **`api.py`**: The FastAPI backend application. Exposes REST endpoints for patient CRUD operations and includes an HTTP middleware that tracks client IPs, blocks banned IPs, and runs Uvicorn inside a background thread via `ServerManager`.
* **`database_handler.py`**: Asynchronous data access layer using `aiofiles` and `csv`. Manages `nurse_data.csv` (with intelligent bed sorting) and handles persistence for blocked IP addresses (`Banned.dat`).
* **`models.py`**: Pydantic data models (`Patient`, `DeletePatient`) enforcing strict payload validation for API requests.
* **`constants.py`**: A massive, categorized repository of standardized medical abbreviations (`MEDICAL_ABBREVIATIONS`) spanning ICU/ER, Cardiology, Surgery, Pediatrics, Oncology, Neurology, Pharmacology, Labs, and more.
* **`utils.py`**: Text utility functions (`clear_shortcut_inputs`) that check input shorthand against medical abbreviations to automatically format and normalize medical notes.
* **`ui_components.py`**: Reusable Flet UI components (`create_row_ui`), specifically generating structured, selectable patient info cards with action triggers for editing and deletion.
* **`main.py`**: The server administration dashboard (`Pt.Server`). Features a server control toggle (Start/Stop), a live reactive IP monitor with instant ban/unban actions, a heartbeat checker, and an anti-burn-in screensaver mode.

---

## Key Features

### 1. Patient Record Management
* Track essential bed metadata: Bed Number, Patient Name, National ID (NID), Specialist (SP), Diet, Respiration System (RES), Diagnosis (Dx), and Consultation (Cx).
* Real-time validation, duplicate bed conflict checks (`409 Conflict`), and smooth edit/change mode transitions.

### 2. Medical Shorthand & Abbreviations
* Integrates an extensive dictionary (`constants.py`) covering over 12 medical specialties.
* Automatically processes and cleans up shorthand inputs to maintain standardized charting.

### 3. Professional PDF Report Generation
* Exports the entire patient database into a clean, structured PDF report using ReportLab.
* Includes full Arabic text reshaping (`arabic_reshaper`) and bidirectional algorithm support (`bidi.algorithm`) using the Amiri TrueType font.
* Seamlessly shares reports via Flet's cross-platform sharing utility.

### 4. Security & IP Management Middleware
* FastAPI middleware inspects incoming client headers and IP addresses.
* Automatically records reactive client IPs and enforces blacklists via a persistent ban file (`Banned.dat`).
* Server dashboard (`Pt.Server`) lets administrators review reactive IPs and instantly ban or unban clients.

### 5. Advanced Server Dashboard
* Built-in server lifecycle management via `ServerManager`.
* Features an Anti-Burn-In Screensaver Mode with dynamic layout repositioning, designed for permanent display on hospital station monitors.

---

## Technology Stack

* **Frontend Framework:** Flet
* **Backend API:** FastAPI & Uvicorn
* **Data Validation:** Pydantic
* **File Operations:** `aiofiles`, `csv`
* **Network Client:** `httpx`
* **PDF Export:** ReportLab, `arabic_reshaper`, `python-bidi`
