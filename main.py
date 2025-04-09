import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from datetime import datetime

class DepositImportApp:
    def __init__(self, frame):
        self.frame = frame
        self.df = None
        self.init_ui()

    def init_ui(self):
        tk.Label(self.frame, text="🏦 Import Deposits to 9500", font=("Arial", 16)).pack(pady=10)

        instructions = (
            "1️⃣ Upload Excel with columns:\n"
            "- Date, Reference 2, Code, Reference, Description, Credit\n\n"
            "2️⃣ It will be formatted for Evolution.\n"
            "3️⃣ You can preview and export it as CSV."
        )
        tk.Label(self.frame, text=instructions, justify="left").pack(pady=5)

        tk.Button(self.frame, text="📥 Upload Excel", command=self.load_excel).pack(pady=10)
        tk.Button(self.frame, text="⬇️ Download CSV", command=self.download_csv).pack(pady=5)
        tk.Button(self.frame, text="🔙 Back", command=self.go_back).pack(pady=10)

        self.preview = tk.Text(self.frame, height=10, width=60)
        self.preview.pack()

    def go_back(self):
        self.frame.master.main_menu()

    def load_excel(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not path:
            return

        try:
            df = pd.read_excel(path)
            df.columns = df.columns.str.strip()

            required = ["Date", "Description", "Credit", "Code", "Reference"]
            if any(col not in df.columns for col in required):
                messagebox.showerror("Missing Columns", f"File must contain: {', '.join(required)}")
                return

            df['Reference'] = df['Reference'].astype(str).str.strip()

            modified = pd.DataFrame()
            modified["TxDate"] = df["Date"]
            modified["Description"] = df["Description"]
            modified["Reference"] = df["Code"].astype(str) + df["Reference"].astype(str)
            modified["Amount"] = df["Credit"]
            modified["UseTax"] = "N"
            modified["TaxType"] = ""
            modified["TaxAccount"] = ""
            modified["TaxAmount"] = 0
            modified["Project"] = ""
            modified["Account"] = "9500/BLM/027"
            modified["IsDebit"] = "Y"
            modified["SplitType"] = 0
            modified["SplitGroup"] = 0
            modified["Reconcile"] = "N"
            modified["PostDated"] = "N"
            modified["UseDiscount"] = "N"
            modified["DiscPerc"] = 0
            modified["DiscTrCode"] = ""
            modified["DiscDesc"] = ""
            modified["UseDiscTax"] = "N"
            modified["DiscTaxType"] = ""
            modified["DiscTaxAcc"] = ""
            modified["DiscTaxAmt"] = 0
            modified["PayeeName"] = ""
            modified["PrintCheque"] = "N"
            modified["SalesRep"] = ""
            modified["Module"] = 0
            modified["SagePayExtra1"] = ""
            modified["SagePayExtra2"] = ""
            modified["SagePayExtra3"] = ""

            # Clean descriptions and references
            phrases = [
                "FNB APP PAYMENT FROM", "DIGITAL PAYMENT CR ABSA BANK", "CAPITEC",
                "ACB CREDIT CAPITEC", "FNB OB PMT", "PayShap Ext Credit",
                "INT-BANKING PMT FRM", "IMMEDIATE TRF CR CAPITEC",
                "IMMEDIATE TRF CR", "ACB CREDIT", "INVESTECPB"
            ]
            modified["Description"] = modified["Description"].replace(phrases, '', regex=True).str.strip()
            modified["Reference"] = modified["Reference"].str.strip().str.replace(r"\.0$", "", regex=True)

            self.df = modified
            self.preview.delete("1.0", tk.END)
            self.preview.insert(tk.END, str(modified.head()))

            messagebox.showinfo("Success", "Excel processed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

    def download_csv(self):
        if self.df is None:
            messagebox.showwarning("Missing", "Please upload and process a file first.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            initialfile=f"IMPORT_{datetime.today().strftime('%Y-%m-%d')}.csv")
        if path:
            self.df.to_csv(path, index=False)
            messagebox.showinfo("Exported", f"CSV saved to:\n{path}")


class Compare9500App:
    def __init__(self, frame):
        self.frame = frame
        self.df_a = None
        self.df_b = None
        self.init_ui()

    def init_ui(self):
        tk.Label(self.frame, text="📊 Compare 9500", font=("Arial", 16)).pack(pady=10)

        self.column_var = tk.IntVar(value=9)
        tk.Label(self.frame, text="Number of columns to compare:").pack()
        tk.Spinbox(self.frame, from_=1, to=50, textvariable=self.column_var).pack(pady=5)

        tk.Button(self.frame, text="Upload Excel A (from Evolution)", command=self.load_file_a).pack(pady=2)
        tk.Button(self.frame, text="Upload Excel B (Reconciliation)", command=self.load_file_b).pack(pady=2)

        tk.Button(self.frame, text="🔍 Compare", command=self.compare).pack(pady=10)

        self.result_label = tk.Label(self.frame, text="")
        self.result_label.pack()

        tk.Button(self.frame, text="⬇️ Export 'Only in A'", command=self.export_a).pack(pady=2)
        tk.Button(self.frame, text="⬇️ Export 'Only in B'", command=self.export_b).pack(pady=2)
        tk.Button(self.frame, text="🔙 Back", command=self.go_back).pack(pady=10)

    def go_back(self):
        self.frame.master.main_menu()

    def load_file_a(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not path:
            return
        self.df_a = pd.read_excel(path).iloc[:, :self.column_var.get()]
        self.clean_dataframe(self.df_a)
        messagebox.showinfo("Success", "Excel A loaded successfully.")

    def load_file_b(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not path:
            return
        xls = pd.ExcelFile(path)
        sheet = xls.sheet_names[0]
        self.df_b = pd.read_excel(path, sheet_name=sheet).iloc[:, :self.column_var.get()]
        self.clean_dataframe(self.df_b)
        messagebox.showinfo("Success", f"Excel B sheet '{sheet}' loaded.")

    def clean_dataframe(self, df):
        df.columns = df.columns.str.strip()
        for col in ["Debit", "Credit"]:
            if col in df.columns:
                df[col] = (
                    df[col].astype(str)
                    .str.replace("R", "")
                    .str.replace(",", "")
                    .str.strip()
                    .replace(["", "None", "nan"], "0")
                    .fillna("0")
                    .astype(float)
                    .round(2)
                )
        for ref_col in ["Reference", "Reference 2"]:
            if ref_col in df.columns:
                df[ref_col] = (
                    df[ref_col].astype(str)
                    .str.strip()
                    .str.lstrip("0")
                    .str.replace(r"\.0$", "", regex=True)
                )

        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date

        if "Description" in df.columns:
            df["Description"] = df["Description"].astype(str).str.lstrip("0").str.strip()

    def compare(self):
        if self.df_a is None or self.df_b is None:
            messagebox.showwarning("Missing", "Please upload both Excel files first.")
            return

        df_a_clean = self.df_a.dropna(how="all").fillna("")
        df_b_clean = self.df_b.dropna(how="all").fillna("")

        for col in df_a_clean.columns:
            if "date" in col.lower():
                df_a_clean[col] = pd.to_datetime(df_a_clean[col], errors="coerce").dt.date
                df_b_clean[col] = pd.to_datetime(df_b_clean[col], errors="coerce").dt.date
            elif col.lower() in ["debit", "credit"]:
                df_a_clean[col] = pd.to_numeric(df_a_clean[col], errors="coerce").round(2)
                df_b_clean[col] = pd.to_numeric(df_b_clean[col], errors="coerce").round(2)
            else:
                df_a_clean[col] = df_a_clean[col].astype(str)
                df_b_clean[col] = df_b_clean[col].astype(str)

        self.only_in_a = pd.merge(df_a_clean, df_b_clean, how="outer", indicator=True)\
                          .query("_merge == 'left_only'").drop(columns=["_merge"])
        self.only_in_b = pd.merge(df_b_clean, df_a_clean, how="outer", indicator=True)\
                          .query("_merge == 'left_only'").drop(columns=["_merge"])

        result = f"✅ Compared!\nOnly in A: {len(self.only_in_a)} rows\nOnly in B: {len(self.only_in_b)} rows"
        self.result_label.config(text=result)

    def export_a(self):
        if hasattr(self, "only_in_a") and not self.only_in_a.empty:
            path = filedialog.asksaveasfilename(defaultextension=".xlsx")
            if path:
                self.only_in_a.to_excel(path, index=False)
                messagebox.showinfo("Exported", f"Saved to {path}")

    def export_b(self):
        if hasattr(self, "only_in_b") and not self.only_in_b.empty:
            path = filedialog.asksaveasfilename(defaultextension=".xlsx")
            if path:
                self.only_in_b.to_excel(path, index=False)
                messagebox.showinfo("Exported", f"Saved to {path}")


class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Automation - 9500 Toolkit")
        self.main_menu()

    def main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="📁 9500 Toolkit", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="📊 Compare 9500", command=self.compare_9500_ui, width=30).pack(pady=5)
        tk.Button(self.root, text="🏦 Import Deposits", command=self.import_deposits_ui, width=30).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=20)

    def compare_9500_ui(self):
        self.clear_window()
        Compare9500App(self.root)

    def import_deposits_ui(self):
        self.clear_window()
        DepositImportApp(self.root)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x450")
    app = FinanceApp(root)
    root.mainloop()
