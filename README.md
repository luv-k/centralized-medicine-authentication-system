# Technology Driven Detection and Prevention of Medicine Adulteration

A nationwide centralized medicine authentication system for generating, distributing, and verifying secure batch serials and QR codes.  The repository combines a Python backend, a small Tkinter management UI and a React/Vite frontend to cover manufacturer batch creation, QR code generation, and pharmacy/hospital scanning & verification.

## 📁 Repository layout

- `back_end/` – FastAPI‑based service and support scripts for QR scanning and database lookup.
- `managment_side/` – Tkinter GUI, serial/QR generation logic and the local serial‑hash database used by manufacturers.
- `frontend/` – React + Vite application for a browser‑based user interface.
- Various `database/`, `generated_qrs/` and `output_json/` directories hold runtime data and should be ignored by Git (see `.gitignore`).

## 🛠 Prerequisites

- **Python 3.8+** (use a virtual environment)  
- **Node.js 16+ / npm** (for the frontend)  
- Python packages: `Pillow`, `pyzbar`, `qrcode` (or install via `requirements.txt`)  
- Optional: `sqlite3` CLI to inspect the SQLite databases.

### Setting up the project

```powershell
# clone & prepare environment
git clone https://github.com/luv-k/centralized-medicine-authentication-system.git
cd Technology_Driven_Detection_and_Prevention_of_Medicine_Adulteration
python -m venv .venv
.venv\Scripts\Activate.ps1      # Windows
# or `source .venv/bin/activate` on macOS/Linux

# install Python dependencies
pip install Pillow pyzbar qrcode
# (alternatively maintain a requirements.txt and run `pip install -r requirements.txt`)

# prepare front‑end
cd frontend
npm install
```

## 🚀 Running components

### Backend API / QR verification

```powershell
cd back_end
uvicorn app:app --reload --host 0.0.0.0 --port 8000
# or use the helper pipeline script:
python piplines.py  # reads a QR image, looks up the hash, and writes JSON output
```

### Management UI (serial & QR generator)

```powershell
cd managment_side
python app.py
``` 
This starts a simple Tkinter window where you can enter batch info, generate serials and create QR images.  Generated QR files appear in `managment_side/generated_qrs/` and their hashes are stored in both local and backend databases.

### Frontend application

```powershell
cd frontend
npm run dev -- --host
``` 
Open a browser to the printed local URL to interact with the React UI.  (The frontend is optional; the management UI and backend functions all work without it.)

## 🔒 Security & data notes

- **Keep the HMAC secret safe.**  The `generate_batch` function uses this secret to derive hashes from serials; leaking it compromises the system.
- `.gitignore` already excludes virtual environments, logs, generated JSON, QR images, and the SQLite files listed above.  Do **not** commit these artifacts.
- The management tool writes to both `managment_side/database_serials_hashing/serials_hashes.db` and `back_end/database/serials_hashes.db` as a simple redundancy/centralization method.

## 🧩 Architecture overview

- **Serial & hash generation** – runs in `managment_side/services_mang/hashing_encoding.py`.
- **Product info storage** – handled by `managment_side/services_mang/info_service.py`.
- **QR creation** – `managment_side/services_mang/qr_generator.py` produces PNGs from hashes.
- **Scanning & lookup** – the backend decodes QR images in `back_end/services/qr_scan.py` and queries databases via `back_end/services/db_lookup.py`.

## 🧑‍💻 Development notes

- You can use the functions in `services_mang/` and `back_end/services/` directly for automation or testing.
- Consider adding automated end‑to‑end tests that call generation and scanning routines.
- API endpoints can be extended in `back_end/app.py` to serve hospitals/pharmacies directly.

## ✅ Next steps (suggestions)

1. Add a `requirements.txt` and/or `package.json` scripts for easier setup.  
2. Write sample configuration or `.env.example` with guidance on secrets.  
3. Harden the backend with TLS and authentication if exposed over a network.  
4. Implement CI to run linting/tests on each PR.

## 🤝 Contributing

Feel free to open issues or pull requests.  Maintainer contact details are in the repository metadata.

---
*This README was expanded to include frontend instructions, setup guidance, and repository structure notes.*
