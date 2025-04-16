import streamlit as st
import pandas as pd
import io

def compare_9500():
    st.title("Compare 9500 from Evolution with the 9500 Reconciliation")

    with st.expander("ℹ️ Instructions"):
        st.markdown("""
    **1️⃣ Export the 9500 from Evolution as Excel**  
    - The file must include the following columns in this order:  
    Date, Reference 2, Code, Reference, Description, Debit, Credit, User Name, Contra Account

    **2️⃣ Prepare the 9500 Reconciliation Excel sheet**  
    - As soon as you export the 9500, update the reconciliation sheet with the new balance.

    **3️⃣ Upload both files below in the correct sections**  
    - Upload the 9500 from Evolution as **Excel A**  
    - Upload the 9500 Reconciliation as **Excel B**

    **4️⃣ After comparison:**  
    - **Sheet A** will show you the entries that need to be added to the recon.  
    - **Sheet B** should ideally be **empty**. If not, it means that an item exists in both sheets but differs in one or more columns, preventing a match.
        """)

    st.info("Note: Macro-enabled Excel files (.xlsm) are supported for data reading only. Macros will not be executed.")

    num_columns = st.number_input(
        " Number of columns to compare", min_value=1, max_value=50, value=9, step=1
    )

    # === Upload 9500 from Evolution
    st.subheader("📥 Step 1: Upload 9500 Excel from Evolution")
    file_a = st.file_uploader("Upload Excel A", type=["xlsx", "xlsm"], key="file_a")

    if file_a:
        df_a = pd.read_excel(file_a, engine="openpyxl").iloc[:, :num_columns]
        df_a.columns = df_a.columns.str.strip()

        for col in ["Debit", "Credit"]:
            if col in df_a.columns:
                df_a[col] = (
                    df_a[col].astype(str)
                    .str.replace("R", "", regex=False)
                    .str.replace(",", "", regex=False)
                    .str.strip()
                    .replace(["", "None", "nan"], "0")
                    .fillna("0")
                    .astype(float)
                    .round(2)
                )

        for ref_col in ["Reference", "Reference 2"]:
            if ref_col in df_a.columns:
                df_a[ref_col] = (
                    df_a[ref_col].astype(str)
                    .str.strip()
                    .str.lstrip("0")
                    .str.replace(r"\.0$", "", regex=True)
                )

        if "Date" in df_a.columns:
            df_a["Date"] = pd.to_datetime(df_a["Date"], errors="coerce").dt.date

        if "Description" in df_a.columns:
            df_a["Description"] = df_a["Description"].astype(str).str.lstrip("0").str.strip()

        for col in df_a.columns:
            if col not in ["Debit", "Credit", "Date"]:
                df_a[col] = (
                    df_a[col].astype(str)
                    .str.strip()
                    .replace(["", "None", "nan"], "0")
                    .fillna("0")
                )

        required_cols = ["Date", "Reference 2", "Code", "Reference", "Description"]
        if all(col in df_a.columns for col in required_cols):
            df_a = df_a[~(
                df_a[required_cols].apply(
                    lambda row: all(
                        pd.isna(val) or str(val).strip() in ["", "0", "0.0", "nan", "None"] or val == 0
                        for val in row
                    ),
                    axis=1
                )
            )]

        st.success("Excel A uploaded successfully.")
        st.markdown("**Preview of first 9 columns:**")
        st.dataframe(df_a)

    # === Upload 9500 Reconciliation File
    st.subheader("📥 Step 2: Upload 9500 Reconciliation and select the sheet")
    file_b = st.file_uploader("Upload Excel B", type=["xlsx", "xlsm"], key="file_b")

    if file_b:
        xls_b = pd.ExcelFile(file_b, engine="openpyxl")
        sheet_names_b = xls_b.sheet_names
        selected_sheet_b = st.selectbox("Select a sheet from Excel B:", sheet_names_b)

        df_b = pd.read_excel(file_b, sheet_name=selected_sheet_b, engine="openpyxl").iloc[:, :num_columns]
        df_b.columns = df_b.columns.str.strip()

        for col in ["Debit", "Credit"]:
            if col in df_b.columns:
                df_b[col] = (
                    df_b[col].astype(str)
                    .str.replace("R", "", regex=False)
                    .str.replace(",", "", regex=False)
                    .str.strip()
                    .replace(["", "None", "nan"], "0")
                    .fillna("0")
                    .astype(float)
                    .round(2)
                )

        for ref_col in ["Reference", "Reference 2"]:
            if ref_col in df_b.columns:
                df_b[ref_col] = (
                    df_b[ref_col].astype(str)
                    .str.strip()
                    .str.lstrip("0")
                    .str.replace(r"\.0$", "", regex=True)
                )

        if "Date" in df_b.columns:
            df_b["Date"] = pd.to_datetime(df_b["Date"], errors="coerce").dt.date

        if "Description" in df_b.columns:
            df_b["Description"] = df_b["Description"].astype(str).str.lstrip("0").str.strip()

        for col in df_b.columns:
            if col not in ["Debit", "Credit", "Date"]:
                df_b[col] = (
                    df_b[col].astype(str)
                    .str.strip()
                    .replace(["", "None", "nan"], "0")
                    .fillna("0")
                )

        required_cols = ["Date", "Reference 2", "Code", "Reference", "Description"]
        if all(col in df_b.columns for col in required_cols):
            df_b = df_b[~(
                df_b[required_cols].apply(
                    lambda row: all(
                        pd.isna(val) or str(val).strip() in ["", "0", "0.0", "nan", "None"] or val == 0
                        for val in row
                    ),
                    axis=1
                )
            )]

        st.success(f"Sheet '{selected_sheet_b}' from Excel B uploaded successfully.")
        st.markdown("**Preview of first 9 columns:**")
        st.dataframe(df_b)

    # === Comparison ===
    st.subheader("🔍 Step 3: Compare the Data")
    if file_a and file_b:
        df_a_clean = df_a.dropna(how="all").fillna("")
        df_b_clean = df_b.dropna(how="all").fillna("")

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

        only_in_a = pd.merge(df_a_clean, df_b_clean, how="outer", indicator=True)\
            .query("_merge == 'left_only'").drop(columns=["_merge"])
        st.markdown(f"### 📌 Rows that are **only in Excel A**: {len(only_in_a)}")
        st.dataframe(only_in_a)

        only_in_b = pd.merge(df_b_clean, df_a_clean, how="outer", indicator=True)\
            .query("_merge == 'left_only'").drop(columns=["_merge"])
        st.markdown(f"### 📌 Rows that are **only in Excel B**: {len(only_in_b)}")
        st.dataframe(only_in_b)

        def to_excel(df, sheet_name="Sheet1"):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name=sheet_name)
            return output.getvalue()

        st.markdown("### ⬇️ Download Differences")
        if not only_in_a.empty:
            st.download_button(
                label="📥 Download: Only in Excel A",
                data=to_excel(only_in_a, sheet_name="Only in A"),
                file_name="differences_only_in_A.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        if not only_in_b.empty:
            st.download_button(
                label="📥 Download: Only in Excel B",
                data=to_excel(only_in_b, sheet_name="Only in B"),
                file_name="differences_only_in_B.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        if st.button("🧾 Extract Code"):
            df_a_clean["Note"] = df_a_clean["Description"]
            phrases_to_remove = [
                "FNB APP PAYMENT FROM",
                "ACB CREDIT CAPITEC",
                "DIGITAL PAYMENT CR ABSA BANK"
            ]
            for phrase in phrases_to_remove:
                df_a_clean["Note"] = df_a_clean["Note"].str.replace(phrase, "", regex=False).str.strip()

            if "Debit" in df_a_clean.columns and "Credit" in df_a_clean.columns:
                df_a_clean["TOTAL"] = df_a_clean["Debit"] + df_a_clean["Credit"]

            st.success("Code extracted successfully. 'Note' and 'TOTAL' columns added.")
            st.dataframe(df_a_clean.head(10))

            st.markdown("### ⬇️ Download Extracted Data")
            st.download_button(
                label="📥 Download Extracted Excel A",
                data=to_excel(df_a_clean, sheet_name="Extracted A"),
                file_name="extracted_excel_a.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
