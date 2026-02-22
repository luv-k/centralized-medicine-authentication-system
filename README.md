# Technology Driven Detection and Prevention of Medicine Adulteration

A nationwide centralized medicine authentication system for generating, distributing, and verifying secure batch serials and QR codes. This project provides tools for manufacturers to generate batch serials and QR codes, and for pharmacies/hospitals to validate products in real time against a centralized database.

**Features**
- **Centralized database:** Stores licensed manufacturers and product records for verification.
- **Real-time batch validation:** HMAC-based serial hashing with lookup support to validate a scanned QR immediately.
- **Integration-ready:** Components for connecting with pharmacy and hospital systems.
- **Batch & QR tooling:** GUI for generating batches, persistent storage, and QR image generation.
- **Audit output:** Verification results written as JSON for logging and downstream processing.

**Quick Start**
- **Requirements:** Python 3.8+ and the packages `Pillow`, `pyzbar`, and `qrcode`.
- **Install deps:**

```bash
pip install Pillow pyzbar qrcode
```

- **Run the management UI (generate batches & QR codes):**

```bash
python managment_side/app.py
```

- **Verify a QR image (example flow):**

```bash
python back_end/piplines.py
```

This will read a QR image, look up the hash in the serial DB, then query the product info DB and save a JSON result to `back_end/output_json`.

**Architecture & Key Components**
- **Management UI:** GUI for batch creation and QR generation. See [managment_side/app.py](managment_side/app.py#L1).
- **Serial generation & hashing:** HMAC-based serial generation and dual DB writes (management + backend). See [managment_side/services_mang/hashing_encoding.py](managment_side/services_mang/hashing_encoding.py#L1).
- **QR generation:** Creates QR images from generated hashes. See [managment_side/services_mang/qr_generator.py](managment_side/services_mang/qr_generator.py#L1).
- **Product info storage:** Persists product meta (batch, dates, manufacturer) to the product info DB. See [managment_side/services_mang/info_service.py](managment_side/services_mang/info_service.py#L1).
- **QR scanning and lookup (backend):** Decode QR images and look up serials/hashes. See [back_end/services/qr_scan.py](back_end/services/qr_scan.py#L1) and [back_end/services/db_lookup.py](back_end/services/db_lookup.py#L1).

**Data & Storage**
- Management-side serial DB: `managment_side/database_serials_hashing/serials_hashes.db`
- Backend serial DB (central): `back_end/database/serials_hashes.db`
- Product info DB: `back_end/database/info_db/info.db`
- Generated QR images: `managment_side/generated_qrs/`
- Verification JSON outputs: `back_end/output_json/`

**Security Notes**
- The HMAC secret (the "secret formula") used in `generate_batch` must be kept confidential; it secures serial→hash generation.
- Database redundancy: `generate_batch` writes to both management and backend DBs for a basic backup/centralization pattern.

**Developer Notes**
- GUI generation: runs the Tkinter app in [managment_side/app.py](managment_side/app.py#L1).
- Non-GUI/automation: reuse functions in `managment_side/services_mang/` and `back_end/services/` for headless workflows.

**Next Steps / Suggestions**
- Add a `requirements.txt` and automated test for end-to-end generation→scan→lookup flows.
- Add API endpoints to expose verification results to hospital/pharmacy systems.
- Harden secrets management and add TLS + auth for any networked API.

**Contact / Contributing**
- For changes, open a PR or contact the repository maintainer.

---
_This README was generated from the project's management and backend service modules to summarize usage and architecture._
