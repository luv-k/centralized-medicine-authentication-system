# Centralized Medicine Authentication System

This repository implements a **three‑phase platform** for generating, distributing,
and verifying secure batch serials and QR codes used by licensed medicine
manufacturers, pharmacies and hospitals.  The goal is to allow products to be
scanned and authenticated in real time against a central authority.

The system comprises:

1. **Management side** – a small Python/Tkinter application used by manufacturers
to create batches, compute HMAC hashes, and generate QR codes.  Serial/hash
data are stored locally and replicated to the backend database.
2. **Backend service** – a FastAPI application that provides QR verification,
database lookup, and optional command‑line pipelines.  It can run standalone or
as part of a hosted web deployment.
3. **Frontend client** – a React + Vite web app that can capture/scan codes
client‑side and call the backend API.

All components use lightweight SQLite databases; files generated at runtime are
ignored by Git via `.gitignore`.

---

## 💡 Key Features

- HMAC‑based serial hashing for tamper‑resistant verification
- QR code generation and image output for distribution
- Central lookup API with real‑time response
- Optional/local pipeline for offline decoding (`pyzbar`) and JSON audit logs
- Simple, modular Python code easily repurposed or tested

---

## 📦 Repository Structure

```
Technology_Driven_Detection_and_Prevention_of_Medicine_Adulteration/
├─ back_end/              # FastAPI app, pipelines, database lookups
├─ managment_side/        # Tkinter GUI, serial/QR logic, local DB
├─ frontend/              # React/Vite web user interface
├─ .gitignore             # excludes venv, generated files, databases
├─ README.md              # (this file)
```

---

## ⚙️ Setup & Requirements

1. **Clone repository**
   ```powershell
   git clone https://github.com/luv-k/centralized-medicine-authentication-system.git
   cd Technology_Driven_Detection_and_Prevention_of_Medicine_Adulteration
   ```

2. **Python environment**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1   # Windows
   # or: source .venv/bin/activate  # macOS/Linux
   pip install Pillow pyzbar qrcode
   ```
   > `pyzbar` is only required if you use the backend pipeline. Remove it if
   > scanning is always done in the browser.  
   > You can also maintain a `requirements.txt` for reproducibility.

3. **Frontend dependencies**
   ```powershell
   cd frontend
   npm install
   ```

---

## 🚀 Running the System

### 1. Management UI

```powershell
cd managment_side
python app.py
```

Complete the form to generate batches, then press “Create QR” to produce PNG
images and populate both the local and central serial databases.

### 2. Backend Service

```powershell
cd back_end
uvicorn app:app --reload --host 0.0.0.0 --port 8000
``` 
This exposes HTTP endpoints for verification.  See `app.py` for route details.

Alternatively, run the pipeline CLI to decode an image and output JSON:

```powershell
python piplines.py --input path/to/qr.png
```

### 3. Frontend Client

```powershell
cd frontend
npm run dev -- --host
```
Point your browser to the printed address and use the interface to upload or
scan codes.  The decoded value is sent to the backend for verification.


---

## 🗃 Data & Storage

- **Serial hash DBs**
  - `managment_side/database_serials_hashing/serials_hashes.db` (local)
  - `back_end/database/serials_hashes.db` (central)
- **Product info DB**: `back_end/database/info_db/info.db`
- **Generated QR images**: `managment_side/generated_qrs/`
- **Verification outputs**: `back_end/output_json/`

> All of the above are ignored by Git; do not commit them.

---

## 🔐 Security Considerations

- The HMAC secret used in `generate_batch` must remain confidential.  Anyone
  with the secret can forge valid hashes.
- Use TLS and authentication when exposing the backend API in production.
- Periodically rotate secrets and revoke stale database entries as needed.

---

## 🛠 Development & Testing

- Reuse functions in `services_mang/` and `back_end/services/` for scripting.
- Add tests to exercise generation → scan → lookup paths, using the `pipline.py` Script for headless validation.
- Extend `back_end/app.py` with new API routes as project requirements evolve.

---

## 📄 Contribution & License

Contributions welcome via pull request.  Follow standard GitHub workflow and
keep changes scoped to one logical feature or fix.  This project is licensed
under the terms of the [LICENSE](LICENSE) file.

---

*Generated and maintained by the project team.*
