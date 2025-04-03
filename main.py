import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Notebook

import pandas as pd
from tkinter import filedialog
import tkinter as tk

def open_compare_9500_window():
    win = ttk.Toplevel(title="Compare 9500 Tool")


    win.geometry("1000x600")

    def load_excel(tree, path_var):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            path_var.set(file_path)
            df = pd.read_excel(file_path).iloc[:, :9]
            update_treeview(tree, df)

    def update_treeview(tree, df):
        tree.delete(*tree.get_children())
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

    # Excel A
    file_a_var = tk.StringVar()
    ttk.Label(win, text="Upload Excel A (9500 from Evolution)").pack(anchor="w", padx=10, pady=(10, 0))
    ttk.Entry(win, textvariable=file_a_var, width=80, state="readonly").pack(padx=10)
    tree_a = ttk.Treeview(win)
    tree_a.pack(padx=10, pady=5, fill="both", expand=True)
    ttk.Button(win, text="Browse A", bootstyle="primary", command=lambda: load_excel(tree_a, file_a_var)).pack(padx=10, pady=5)

    # Excel B
    file_b_var = tk.StringVar()
    ttk.Label(win, text="Upload Excel B (9500 Reconciliation)").pack(anchor="w", padx=10, pady=(20, 0))
    ttk.Entry(win, textvariable=file_b_var, width=80, state="readonly").pack(padx=10)
    tree_b = ttk.Treeview(win)
    tree_b.pack(padx=10, pady=5, fill="both", expand=True)
    ttk.Button(win, text="Browse B", bootstyle="primary", command=lambda: load_excel(tree_b, file_b_var)).pack(padx=10, pady=5)


# Create the main window with a Bootstrap theme
root = ttk.Window(themename="cosmo")
root.title("Finance Team")
root.geometry("800x400")

# Create the Notebook (tabbed interface)
notebook = Notebook(root, bootstyle="info")
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# Create frames for each tab
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)
tab5 = ttk.Frame(notebook)
tab6 = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(tab1, text="Home")
notebook.add(tab2, text="Jo-Zelle")
notebook.add(tab3, text="Christo")
notebook.add(tab4, text="Mariska")
notebook.add(tab5, text="Lizelle")
notebook.add(tab6, text="Settings")

# Add buttons to Tab One
ttk.Button(tab1, text='primary', bootstyle=PRIMARY).pack(side=LEFT, padx=5, pady=5)
ttk.Button(tab1, text='secondary', bootstyle=SECONDARY).pack(side=LEFT, padx=5, pady=5)
ttk.Button(tab1, text='success', bootstyle=SUCCESS).pack(side=LEFT, padx=5, pady=5)
ttk.Button(tab1, text='info', bootstyle=INFO).pack(side=LEFT, padx=5, pady=5)
ttk.Button(tab1, text='warning', bootstyle=WARNING).pack(side=LEFT, padx=5, pady=5)
ttk.Button(tab1, text='danger', bootstyle=DANGER).pack(side=LEFT, padx=5, pady=5)
ttk.Button(tab1, text='light', bootstyle=LIGHT).pack(side=LEFT, padx=5, pady=5)
ttk.Button(tab1, text='dark', bootstyle=DARK).pack(side=LEFT, padx=5, pady=5)

# Add different buttons to Tab Two
ttk.Button(tab2, text="Compare", bootstyle=SUCCESS).pack(side=LEFT, padx=5, pady=10)
ttk.Button(tab2, text="Outline Button", bootstyle=(SUCCESS, OUTLINE)).pack(side=LEFT, padx=5, pady=10)

# Add different buttons to Mariska
ttk.Button(tab4, text="Compare 9500", bootstyle=SUCCESS, command=open_compare_9500_window).pack(side=LEFT, padx=5, pady=10)

ttk.Button(tab4, text="9500 Import", bootstyle=(SUCCESS, OUTLINE)).pack(side=LEFT, padx=5, pady=10)

# Run the app
root.mainloop()
