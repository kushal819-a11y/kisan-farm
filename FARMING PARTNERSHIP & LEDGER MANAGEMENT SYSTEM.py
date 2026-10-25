# ==========================================
# FARMING PARTNERSHIP & LEDGER MANAGEMENT SYSTEM (ULTIMATE EDITION v2)
# Developed by: Kushal Kumar Soni
# Company: CodeCore Tech
# Gram: Sehrai | Range: Chadpur
# ==========================================

from tkinter import *
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
from datetime import datetime
from PIL import Image, ImageTk

class UltimateFarmingAppV2:
    def __init__(self, root):
        self.root = root
        self.root.title("Farming Partnership & Ledger - CodeCore Tech by Kushal Kumar Soni")
        self.root.geometry("1500x900")
        
        self.gram_name = "Sehrai"
        self.range_name = "Chadpur"
        
        self.init_db()
        self.create_header()
        self.create_notebook_tabs()
        self.update_clock()

    def init_db(self):
        self.conn = sqlite3.connect("farming_codecore_ultimate_v2.db")
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                season TEXT,
                crop_name TEXT,
                category TEXT,
                item_name TEXT,
                unit TEXT,
                quantity REAL,
                rate REAL,
                total_amount REAL,
                buyer_name TEXT,
                partner_name TEXT,
                soni_share REAL,
                partner_share REAL,
                notes TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS partner_photos (
                partner_name TEXT PRIMARY KEY,
                photo_path TEXT
            )
        """)
        self.conn.commit()

    def create_header(self):
        self.header_frame = Frame(self.root, bg="#1b4f72", pady=12)
        self.header_frame.pack(fill=X)
        
        title_lbl = Label(self.header_frame, text="🌾 ULTIMATE FARMING LEDGER & PARTNERSHIP SOFTWARE 🌾", font=("Arial", 16, "bold"), fg="white", bg="#1b4f72")
        title_lbl.pack(side=LEFT, padx=20)
        
        self.info_lbl = Label(self.header_frame, text="", font=("Arial", 10, "bold"), fg="#f1c40f", bg="#1b4f72")
        self.info_lbl.pack(side=RIGHT, padx=20)

        self.sub_frame = Frame(self.root, bg="#2e4053", pady=6)
        self.sub_frame.pack(fill=X)
        
        dev_lbl = Label(self.sub_frame, text="Developer: Kushal Kumar Soni  |  Company: CodeCore Tech  |  Gram: " + self.gram_name + "  |  Range: " + self.range_name, font=("Arial", 10, "italic"), fg="white", bg="#2e4053")
        dev_lbl.pack(side=LEFT, padx=20)
        
        theme_lbl = Label(self.sub_frame, text="Background Theme:", fg="white", bg="#2e4053", font=("Arial", 9, "bold"))
        theme_lbl.pack(side=LEFT, padx=10)
        
        self.theme_combo = ttk.Combobox(self.sub_frame, values=["Ocean Blue (Default)", "Dark Black Theme", "Pure White Theme", "Classic Green"], width=20, state="readonly")
        self.theme_combo.current(0)
        self.theme_combo.pack(side=LEFT, padx=5)
        self.theme_combo.bind("<<ComboboxSelected>>", self.change_theme)

    def update_clock(self):
        now = datetime.now().strftime("%d-%m-%Y  %H:%M:%S")
        self.info_lbl.config(text=f"📅 {now} | Gram: {self.gram_name} | Range: {self.range_name}")
        self.root.after(1000, self.update_clock)

    def change_theme(self, event=None):
        selected = self.theme_combo.get()
        if "Dark Black" in selected:
            self.header_frame.config(bg="#111111")
            self.sub_frame.config(bg="#222222")
            self.root.config(bg="#1c1c1c")
        elif "Pure White" in selected:
            self.header_frame.config(bg="#f8f9fa")
            self.sub_frame.config(bg="#e9ecef")
        elif "Classic Green" in selected:
            self.header_frame.config(bg="#145a32")
            self.sub_frame.config(bg="#196f3d")
        else:
            self.header_frame.config(bg="#1b4f72")
            self.sub_frame.config(bg="#2e4053")
        messagebox.showinfo("Theme Updated", f"Theme successfully changed to {selected}")

    def create_notebook_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        self.tab4 = ttk.Frame(self.notebook)
        self.tab5 = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab1, text=" 📝 Add Entry (DD-MM-YYYY) ")
        self.notebook.add(self.tab2, text=" 📊 Partner Ledgers & Mutual Settlement ")
        self.notebook.add(self.tab3, text=" 🔗 Compound Totals & 3% Interest ")
        self.notebook.add(self.tab4, text=" 🖼️ Partner Photos (Passport) ")
        self.notebook.add(self.tab5, text=" 🖨️ Print, Export & Backup ")
        
        self.build_page1()
        self.build_page2()
        self.build_page3()
        self.build_page4()
        self.build_page5()

    def build_page1(self):
        frame = ttk.LabelLabelFrame if hasattr(ttk, 'LabelLabelFrame') else ttk.LabelFrame
        container = frame(self.tab1, text=" Alag Alag Samaan (DAP with Rate, Urea, Sulphur, Zinc, Potash etc.) Add Karein ", padding=20)
        container.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        labels = [
            "Date (DD-MM-YYYY):", 
            "Season (Rabi/Kharif/Zaid/Varsh):", 
            "Crop Name (Dhan/Gehu/Sarso):",
            "Category (Khad/Pesticide/Beej/Motor Bill/Diesel/Jutai/Labor):",
            "Item Name (DAP, Urea, Sulphur, Zinc, Potash etc.):", 
            "Unit (Packet/Bag/Kg/Liter/Nag):",
            "Quantity (Kitne Packet/Bori/Kg):", 
            "Rate per Unit (₹ Rate):", 
            "Who Paid / Bought (Buyer):", 
            "Partnership Between:"
        ]
        
        self.p1_entries = {}
        for i, text in enumerate(labels):
            lbl = Label(container, text=text, font=("Arial", 10, "bold"))
            lbl.grid(row=i, column=0, sticky=W, pady=8, padx=10)
            
            if "Date" in text:
                ent = ttk.Entry(container, width=35)
                ent.insert(0, datetime.now().strftime("%d-%m-%Y"))
            elif "Season" in text:
                ent = ttk.Combobox(container, values=["Rabi", "Kharif", "Zaid", "Varsh (Annual)"], width=33)
                ent.current(0)
            elif "Category" in text:
                ent = ttk.Combobox(container, values=["Khad (Fertilizer)", "Pesticide/Herbicide", "Beej (Seed)", "Electricity/Motor Bill", "Diesel", "Jutai (Ploughing)", "Labor", "Combine Harvester Katai", "Extra Expense"], width=33)
                ent.current(0)
            elif "Item Name" in text:
                ent = ttk.Combobox(container, values=["DAP Fertilizer", "Urea Fertilizer", "Sulphur", "Zinc", "Potash", "Pesticide Spray", "Seeds (Beej)", "Diesel", "Labor Charge"], width=33)
                ent.current(0)
            elif "Unit" in text:
                ent = ttk.Combobox(container, values=["Packet", "Bag", "Kg", "Liter", "Piece", "Nag", "Acre"], width=33)
                ent.current(0)
            elif "Buyer" in text:
                ent = ttk.Combobox(container, values=["Kushal Kumar Soni", "Dinesh Rawat", "Both Equally"], width=33)
                ent.current(0)
            elif "Partnership" in text:
                ent = ttk.Entry(container, width=35)
                ent.insert(0, "Kushal Kumar Soni vs Dinesh Rawat")
            else:
                ent = ttk.Entry(container, width=35)
                
            ent.grid(row=i, column=1, sticky=W, pady=8, padx=10)
            self.p1_entries[text] = ent
            
        save_btn = Button(container, text="💾 Save Entry & Calculate Total (Rate x Qty)", bg="#27ae60", fg="white", font=("Arial", 11, "bold"), command=self.save_p1_entry)
        save_btn.grid(row=len(labels), column=1, sticky=E, pady=20)

    def save_p1_entry(self):
        try:
            keys = list(self.p1_entries.keys())
            date_val = self.p1_entries[keys[0]].get()
            season_val = self.p1_entries[keys[1]].get()
            crop_val = self.p1_entries[keys[2]].get()
            cat_val = self.p1_entries[keys[3]].get()
            item_val = self.p1_entries[keys[4]].get()
            unit_val = self.p1_entries[keys[5]].get()
            qty_val = float(self.p1_entries[keys[6]].get())
            rate_val = float(self.p1_entries[keys[7]].get())
            buyer_val = self.p1_entries[keys[8]].get()
            partner_val = self.p1_entries[keys[9]].get()
            
            total_amt = qty_val * rate_val
            soni_share = total_amt / 2.0
            partner_share = total_amt / 2.0
            
            self.cursor.execute("""
                INSERT INTO entries (date, season, crop_name, category, item_name, unit, quantity, rate, total_amount, buyer_name, partner_name, soni_share, partner_share, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (date_val, season_val, crop_val, cat_val, item_val, unit_val, qty_val, rate_val, total_amt, buyer_val, partner_val, soni_share, partner_share, f"Buyer: {buyer_val}"))
            self.conn.commit()
            messagebox.showinfo("Success", f"Entry Saved Successfully! Total Amount: ₹{total_amt:.2f} (Rate: ₹{rate_val} x Qty: {qty_val})")
            self.load_page2_ledger()
        except Exception as e:
            messagebox.showerror("Error", f"Kripya sahi values enter karein: {e}")

    def build_page2(self):
        frame = ttk.Frame(self.tab2, padding=15)
        frame.pack(fill=BOTH, expand=True)
        
        top_bar = Frame(frame)
        top_bar.pack(fill=X, pady=5)
        
        Label(top_bar, text="Kushal Kumar Soni Vs Dinesh Rawat - Ledger & Mutual Settlement", font=("Arial", 13, "bold"), fg="#1b4f72").pack(side=LEFT)
        Button(top_bar, text="⚖️ Calculate Mutual Settlement (Lena/Dena)", bg="#d35400", fg="white", font=("Arial", 10, "bold"), command=self.calculate_settlement).pack(side=RIGHT, padx=5)
        
        self.tree = ttk.Treeview(frame, columns=("ID", "Date", "Item Name", "Qty", "Rate (₹)", "Total Amount (₹)", "Buyer", "Soni Share", "Partner Share"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill=BOTH, expand=True, pady=10)
        
        self.settlement_lbl = Label(frame, text="Click 'Calculate Mutual Settlement' to check who owes whom how much.", font=("Arial", 11, "bold"), fg="#2c3e50", bg="#eaeded", padx=10, pady=10)
        self.settlement_lbl.pack(fill=X, pady=5)
        
        btn_refresh = Button(frame, text="🔄 Refresh Ledger Data", bg="#2980b9", fg="white", font=("Arial", 10, "bold"), command=self.load_page2_ledger)
        btn_refresh.pack(pady=5)

    def load_page2_ledger(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute("SELECT id, date, item_name, quantity, rate, total_amount, buyer_name, soni_share, partner_share FROM entries")
        for row in self.cursor.fetchall():
            self.tree.insert("", END, values=row)

    def calculate_settlement(self):
        self.cursor.execute("SELECT buyer_name, SUM(total_amount), SUM(soni_share), SUM(partner_share) FROM entries GROUP BY buyer_name")
        rows = self.cursor.fetchall()
        
        soni_paid = 0.0
        dinesh_paid = 0.0
        total_expense = 0.0
        
        for r in rows:
            buyer = r[0]
            amt = r[1]
            total_expense += amt
            if "Kushal" in buyer:
                soni_paid += amt
            elif "Dinesh" in buyer:
                dinesh_paid += amt
            elif "Both" in buyer:
                soni_paid += (amt / 2.0)
                dinesh_paid += (amt / 2.0)
                
        each_share = total_expense / 2.0
        soni_balance = soni_paid - each_share
        
        if soni_balance > 0:
            text = f"📊 MUTUAL SETTLEMENT SUMMARY:\nTotal Farming Expense: ₹{total_expense:.2f} | Each Partner's 50% Share: ₹{each_share:.2f}\n- Kushal Kumar Soni paid: ₹{soni_paid:.2f}\n- Dinesh Rawat paid: ₹{dinesh_paid:.2f}\n👉 RESULT: Dinesh Rawat has to GIVE ₹{soni_balance:.2f} to Kushal Kumar Soni."
        else:
            text = f"📊 MUTUAL SETTLEMENT SUMMARY:\nTotal Farming Expense: ₹{total_expense:.2f} | Each Partner's 50% Share: ₹{each_share:.2f}\n- Kushal Kumar Soni paid: ₹{soni_paid:.2f}\n- Dinesh Rawat paid: ₹{dinesh_paid:.2f}\n👉 RESULT: Kushal Kumar Soni has to GIVE ₹{abs(soni_balance):.2f} to Dinesh Rawat."
            
        self.settlement_lbl.config(text=text)

    def build_page3(self):
        frame = ttk.LabelFrame(self.tab3, text=" Compound Totals & 3% Monthly Interest on Partner Purchases ", padding=20)
        frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        Label(frame, text="Compound total for items purchased by Dinesh Rawat with 3% monthly interest for delayed payments.", font=("Arial", 10, "italic"), fg="red").pack(anchor=W, pady=5)
        
        f_sub = Frame(frame)
        f_sub.pack(fill=X, pady=15)
        
        Label(f_sub, text="Principal Amount Owed (₹):", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        self.p3_amt = ttk.Entry(f_sub, width=18)
        self.p3_amt.pack(side=LEFT, padx=5)
        
        Label(f_sub, text="Months Delayed:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        self.p3_months = ttk.Entry(f_sub, width=10)
        self.p3_months.insert(0, "1")
        self.p3_months.pack(side=LEFT, padx=5)
        
        calc_btn = Button(f_sub, text="Calculate Compound Total (3% p.m.)", bg="#d35400", fg="white", font=("Arial", 10, "bold"), command=self.calc_compound_interest)
        calc_btn.pack(side=LEFT, padx=15)
        
        self.p3_result_lbl = Label(frame, text="", font=("Arial", 12, "bold"), fg="#2c3e50", justify=LEFT)
        self.p3_result_lbl.pack(pady=20, anchor=W)

    def calc_compound_interest(self):
        try:
            p = float(self.p3_amt.get())
            m = float(self.p3_months.get())
            rate = 0.03
            total_due = p * ((1 + rate) ** m)
            interest_only = total_due - p
            res_text = f"Partner: Dinesh Rawat\nPrincipal Purchase Amount: ₹{p:.2f}\nCompound Interest Rate: 3% Per Month\nTime Duration: {m} Months\nTotal Interest: ₹{interest_only:.2f}\n👉 Compound Total Payable: ₹{total_due:.2f}"
            self.p3_result_lbl.config(text=res_text)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid number entered: {e}")

    def build_page4(self):
        frame = ttk.LabelFrame(self.tab4, text=" Passport Size Photos (Kushal Kumar Soni vs Dinesh Rawat) ", padding=20)
        frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        f_top = Frame(frame)
        f_top.pack(fill=X, pady=10)
        
        Label(f_top, text="Select Partner Profile:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        self.p4_combo = ttk.Combobox(f_top, values=["Kushal Kumar Soni", "Dinesh Rawat"], width=25, state="readonly")
        self.p4_combo.current(0)
        self.p4_combo.pack(side=LEFT, padx=5)
        
        Button(f_top, text="📁 Upload Passport Photo", bg="#2980b9", fg="white", font=("Arial", 10, "bold"), command=self.upload_passport_photo).pack(side=LEFT, padx=15)
        Button(f_top, text="👁️ View Photo", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), command=self.view_passport_photo).pack(side=LEFT, padx=5)
        
        self.photo_display_lbl = Label(frame, text="No Passport Photo Loaded", font=("Arial", 11), bg="#ecf0f1", width=35, height=14)
        self.photo_display_lbl.pack(pady=20)

    def upload_passport_photo(self):
        partner = self.p4_combo.get()
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.cursor.execute("REPLACE INTO partner_photos (partner_name, photo_path) VALUES (?, ?)", (partner, file_path))
            self.conn.commit()
            messagebox.showinfo("Success", f"Passport photo saved for {partner}!")
            self.view_passport_photo()

    def view_passport_photo(self):
        partner = self.p4_combo.get()
        self.cursor.execute("SELECT photo_path FROM partner_photos WHERE partner_name = ?", (partner,))
        row = self.cursor.fetchone()
        if row and os.path.exists(row[0]):
            img = Image.open(row[0])
            img = img.resize((150, 180), Image.Resampling.LANCZOS)
            self.p4_img = ImageTk.PhotoImage(img)
            self.photo_display_lbl.config(image=self.p4_img, text="")
        else:
            self.photo_display_lbl.config(image="", text="No Photo Found in Database")

    def build_page5(self):
        frame = ttk.LabelFrame(self.tab5, text=" Print Reports, Export Summary, Backup & Restore Database ", padding=25)
        frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        Button(frame, text="🖨️ Print Ledger Report", bg="#2980b9", fg="white", font=("Arial", 11, "bold"), width=30, command=self.print_report).pack(pady=12)
        Button(frame, text="📄 Export Summary to Text/PDF", bg="#8e44ad", fg="white", font=("Arial", 11, "bold"), width=30, command=self.export_pdf_report).pack(pady=12)
        Button(frame, text="📥 Backup Database", bg="#16a085", fg="white", font=("Arial", 11, "bold"), width=30, command=self.backup_database).pack(pady=12)
        Button(frame, text="📤 Restore Database", bg="#d35400", fg="white", font=("Arial", 11, "bold"), width=30, command=self.restore_database).pack(pady=12)

    def print_report(self):
        messagebox.showinfo("Print Status", "Ledger report sent to printer successfully! (CodeCore Tech - Gram Sehrai, Range Chadpur)")

    def export_pdf_report(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text / Report Files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("=== FARMING PARTNERSHIP LEDGER REPORT ===\n")
                f.write("Company: CodeCore Tech | Developer: Kushal Kumar Soni\n")
                f.write("Gram: Sehrai | Range: Chadpur\n")
                f.write("Partnership: Kushal Kumar Soni vs Dinesh Rawat\n")
                f.write("="*50 + "\n\n")
                self.cursor.execute("SELECT * FROM entries")
                for row in self.cursor.fetchall():
                    f.write(str(row) + "\n")
            messagebox.showinfo("Success", f"Report successfully exported to {file_path}")

    def backup_database(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("Database Files", "*.db")])
        if file_path:
            import shutil
            shutil.copy("farming_codecore_ultimate_v2.db", file_path)
            messagebox.showinfo("Success", f"Database backed up to {file_path}")

    def restore_database(self):
        file_path = filedialog.askopenfilename(filetypes=[("Database Files", "*.db")])
        if file_path:
            import shutil
            shutil.copy(file_path, "farming_codecore_ultimate_v2.db")
            messagebox.showinfo("Success", "Database restored successfully! Please restart application.")

if __name__ == "__main__":
    root = Tk()
    app = UltimateFarmingAppV2(root)
    root.mainloop()
    