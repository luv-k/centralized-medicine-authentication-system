import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime

from services_mang.hashing_encoding import generate_batch
from services_mang.qr_generator import generate_qrs
from services_mang.info_service import store_product_info


class ModernApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Batch Serial & QR Generator")
        self.root.geometry("900x720")
        self.root.configure(bg="#f0f2f5")

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.configure_styles()
        self.create_widgets()

    # ---------------- STYLING ---------------- #

    def configure_styles(self):

        # Frames
        self.style.configure("TFrame", background="#f0f2f5")

        # Card Frame Style
        self.style.configure("Card.TFrame",
                             background="#ffffff",
                             relief="flat")

        # Header
        self.style.configure("Header.TLabel",
                             background="#f0f2f5",
                             foreground="#111b21",
                             font=("Segoe UI", 24, "bold"))

        # Labels
        self.style.configure("TLabel",
                             background="#ffffff",
                             foreground="#3b4a54",
                             font=("Segoe UI", 11))

        # Entry
        self.style.configure("TEntry",
                             padding=6)

        # Button
        self.style.configure("Accent.TButton",
                             background="#25D366",
                             foreground="white",
                             font=("Segoe UI", 11, "bold"),
                             padding=10,
                             borderwidth=0)

        self.style.map("Accent.TButton",
                       background=[("active", "#1ebe5d")])

        # Progressbar
        self.style.configure("green.Horizontal.TProgressbar",
                             troughcolor="#e9edef",
                             background="#25D366",
                             thickness=14)

    # ---------------- UI LAYOUT ---------------- #

    def create_widgets(self):

        # Header
        ttk.Label(self.root,
                  text="Batch Serial & QR Generator",
                  style="Header.TLabel",
                  background="#f0f2f5").pack(pady=25)

        # Main Card Container
        card = ttk.Frame(self.root, style="Card.TFrame")
        card.pack(padx=40, pady=10, fill="both", expand=True)

        inner = ttk.Frame(card, style="Card.TFrame")
        inner.pack(padx=40, pady=30, fill="both", expand=True)

        # ---------------- Core Section ---------------- #

        ttk.Label(inner, text="Batch Size:").grid(row=0, column=0, sticky="w", pady=8)
        self.batch_entry = ttk.Entry(inner, width=30)
        self.batch_entry.grid(row=0, column=1, pady=8)

        ttk.Label(inner, text="Secret Formula:").grid(row=1, column=0, sticky="w", pady=8)
        self.secret_entry = ttk.Entry(inner, width=30, show="*")
        self.secret_entry.grid(row=1, column=1, pady=8)

        ttk.Separator(inner).grid(row=2, columnspan=3, sticky="ew", pady=20)

        # ---------------- Product Info ---------------- #

        ttk.Label(inner, text="Batch No:").grid(row=3, column=0, sticky="w", pady=6)
        self.batch_no_entry = ttk.Entry(inner, width=30)
        self.batch_no_entry.grid(row=3, column=1)

        ttk.Label(inner, text="Manufacture Date:").grid(row=4, column=0, sticky="w", pady=6)
        self.mfg_date_entry = ttk.Entry(inner, width=30)
        self.mfg_date_entry.grid(row=4, column=1)
        ttk.Label(inner, text="(DD/MM/YYYY)", foreground="#8696a0").grid(row=4, column=2)

        ttk.Label(inner, text="Expiry Date:").grid(row=5, column=0, sticky="w", pady=6)
        self.expiry_date_entry = ttk.Entry(inner, width=30)
        self.expiry_date_entry.grid(row=5, column=1)
        ttk.Label(inner, text="(DD/MM/YYYY)", foreground="#8696a0").grid(row=5, column=2)

        ttk.Label(inner, text="Colour:").grid(row=6, column=0, sticky="w", pady=6)
        self.colour_entry = ttk.Entry(inner, width=30)
        self.colour_entry.grid(row=6, column=1)

        ttk.Label(inner, text="Manufactured By:").grid(row=7, column=0, sticky="w", pady=6)
        self.manufacturer_entry = ttk.Entry(inner, width=30)
        self.manufacturer_entry.grid(row=7, column=1)

        ttk.Label(inner, text="License No:").grid(row=8, column=0, sticky="w", pady=6)
        self.license_entry = ttk.Entry(inner, width=30)
        self.license_entry.grid(row=8, column=1)

        # ---------------- Generate Button ---------------- #

        self.generate_btn = ttk.Button(inner,
                                       text="Generate Complete Batch",
                                       style="Accent.TButton",
                                       command=self.start_process)
        self.generate_btn.grid(row=9, columnspan=3, pady=25)

        # ---------------- Progress ---------------- #

        self.progress = ttk.Progressbar(inner,
                                        style="green.Horizontal.TProgressbar",
                                        length=600,
                                        mode="determinate")
        self.progress.grid(row=10, columnspan=3, pady=10)

        self.status_label = ttk.Label(inner,
                                      text="Waiting for input...",
                                      background="#ffffff")
        self.status_label.grid(row=11, columnspan=3, pady=5)

        # ---------------- Log ---------------- #

        self.log_box = tk.Text(inner,
                               height=8,
                               bg="#f7f9fa",
                               fg="#111b21",
                               insertbackground="#111b21",
                               font=("Consolas", 10),
                               relief="flat",
                               borderwidth=5)
        self.log_box.grid(row=12, columnspan=3, pady=15, sticky="ew")

    # ---------------- VALIDATION ---------------- #

    def validate_date(self, date_string):
        try:
            parsed = datetime.strptime(date_string, "%d/%m/%Y")
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            return None

    # ---------------- PROCESS ---------------- #

    def log(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)

    def start_process(self):

        try:
            count = int(self.batch_entry.get())
            secret = self.secret_entry.get()

            if count <= 0 or not secret:
                raise ValueError

            mfg_date = self.validate_date(self.mfg_date_entry.get().strip())
            expiry_date = self.validate_date(self.expiry_date_entry.get().strip())

            if not mfg_date or not expiry_date:
                messagebox.showerror("Invalid Date",
                                     "Dates must be in DD/MM/YYYY format.")
                return

            if expiry_date <= mfg_date:
                messagebox.showerror("Date Error",
                                     "Expiry date must be later than manufacture date.")
                return

            self.valid_mfg_date = mfg_date
            self.valid_expiry_date = expiry_date

        except:
            messagebox.showerror("Error",
                                 "Please enter valid batch size and secret.")
            return

        self.generate_btn.config(state="disabled")
        threading.Thread(target=self.run_generation,
                         args=(count, secret),
                         daemon=True).start()

    def run_generation(self, count, secret):

        self.log("Starting batch generation...")
        self.status_label.config(text="Generating databases...")

        records = generate_batch(count, secret)

        self.log(f"{len(records)} serials created.")

        store_product_info(
            records=records,
            batch_no=self.batch_no_entry.get(),
            date_expire=self.valid_expiry_date,
            date_manufacture=self.valid_mfg_date,
            colour=self.colour_entry.get(),
            manufactured_by=self.manufacturer_entry.get(),
            license_no=self.license_entry.get()
        )

        self.log("Product info stored.")

        self.progress["maximum"] = len(records)
        self.status_label.config(text="Generating QR Codes...")

        for current, total in generate_qrs(records):
            self.progress["value"] = current
            self.status_label.config(text=f"QR {current}/{total}")
            self.root.update_idletasks()

        self.log("QR generation completed.")
        self.status_label.config(text="Completed Successfully.")
        self.generate_btn.config(state="normal")

        messagebox.showinfo("Success",
                            f"{count} records generated successfully!")


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernApp(root)
    root.mainloop()
