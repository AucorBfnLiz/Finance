import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

def import_deposits():
    st.title("🏦 Deposit Import to 9500 Cashbook")

    with st.expander("ℹ️ Instructions"):
        st.markdown("""
**Step 1: Prepare your Excel file**  
- The file must include the following columns:  
  `Date`, `Reference 2`, `Code`, `Reference`, `Description`, `Credit`

**Step 2: Upload the Excel file**  
- The data will be processed and converted into a format compatible with the Central Cashbook.

**Step 3: Download the formatted CSV**  
- You can import this file directly into Evolution.
        """)

    uploaded_file = st.file_uploader("Upload your Excel file:", type=["xlsx", "xls"])

    if uploaded_file:
        try:
            # Handle multiple sheets
            xls = pd.ExcelFile(uploaded_file)
            sheet_names = xls.sheet_names
            selected_sheet = st.selectbox("Select a sheet:", sheet_names)

            df = pd.read_excel(xls, sheet_name=selected_sheet)
            df.columns = df.columns.str.strip()

            cols_to_check = ["Date", "Reference 2", "Code", "Reference"]

            if all(col in df.columns for col in cols_to_check):
                df = df[~(
                    df[cols_to_check].apply(
                        lambda row: all(
                            pd.isna(val) or str(val).strip() in ["", "0", "0.0", "nan", "None"] or val == 0
                            for val in row
                        ),
                        axis=1
                    )
                )]

            required_columns = ["Date", "Description", "Credit", "Code", "Reference"]
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                st.error(f"Missing required column(s): {', '.join(missing_columns)}")
                return

            df['Reference'] = df['Reference'].astype(str).str.strip()

            # ✅ Format for Evolution import
            modified_df = pd.DataFrame()
            modified_df["TxDate"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
            modified_df["Description"] = df["Description"]
            modified_df["Reference"] = df["Code"].astype(str) + df["Reference"].astype(str)
            modified_df["Amount"] = df["Credit"]
            modified_df["UseTax"] = "N"
            modified_df["TaxType"] = ""
            modified_df["TaxAccount"] = ""
            modified_df["TaxAmount"] = 0
            modified_df["Project"] = ""
            modified_df["Account"] = "9500/BLM/027"
            modified_df["IsDebit"] = "Y"
            modified_df["SplitType"] = 0
            modified_df["SplitGroup"] = 0
            modified_df["Reconcile"] = "N"
            modified_df["PostDated"] = "N"
            modified_df["UseDiscount"] = "N"
            modified_df["DiscPerc"] = 0
            modified_df["DiscTrCode"] = ""
            modified_df["DiscDesc"] = ""
            modified_df["UseDiscTax"] = "N"
            modified_df["DiscTaxType"] = ""
            modified_df["DiscTaxAcc"] = ""
            modified_df["DiscTaxAmt"] = 0
            modified_df["PayeeName"] = ""
            modified_df["PrintCheque"] = "N"
            modified_df["SalesRep"] = ""
            modified_df["Module"] = 0
            modified_df["SagePayExtra1"] = ""
            modified_df["SagePayExtra2"] = ""
            modified_df["SagePayExtra3"] = ""

          


            # 🔍 Clean up description and reference
            phrases_to_remove = [
                "FNB APP PAYMENT FROM", "DIGITAL PAYMENT CR ABSA BANK", "CAPITEC",
                "ACB CREDIT CAPITEC", "FNB OB PMT", "PayShap Ext Credit",
                "INT-BANKING PMT FRM", "IMMEDIATE TRF CR CAPITEC",
                "IMMEDIATE TRF CR", "ACB CREDIT", "INVESTECPB"
            ]
            modified_df["Description"] = modified_df["Description"].replace(phrases_to_remove, '', regex=True).str.strip()
            modified_df["Reference"] = modified_df["Reference"].str.strip().str.replace(r"\.0$", "", regex=True)

            


            # ✅ Preview data
            st.success("File processed successfully. Preview below:")
            st.dataframe(modified_df)

            total_amount = modified_df["Amount"].sum()
            st.markdown(f"**💰 Total Amount:** R {total_amount:,.2f}")


            # 📥 Download CSV
            csv_data = modified_df.to_csv(index=False).encode("utf-8")
            today_date = datetime.today().strftime("%Y-%m-%d")
            default_filename = f"IMPORT_{today_date}.csv"

            st.download_button(
                label="📥 Download CSV for Evolution",
                data=csv_data,
                file_name=default_filename,
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"An error occurred: {e}")
