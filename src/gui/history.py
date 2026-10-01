import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox


# =========================================================
# ADD SRC FOLDER TO PYTHON PATH
# =========================================================

SRC_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


# Now Python can find the database package
from database.query_history import QueryHistory


class HistoryWindow:

    def __init__(self, parent, username=None):

        self.parent = parent
        self.username = username

        self.window = tk.Toplevel(parent)

        self.window.title("📜 Query History")
        self.window.geometry("1100x600")
        self.window.minsize(900, 500)

        self.create_ui()
        self.load_history()

    # =========================================================
    # CREATE USER INTERFACE
    # =========================================================

    def create_ui(self):

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        header = tk.Frame(
            self.window,
            bg="#1f2937",
            height=70
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="📜 Query History",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#1f2937"
        )

        title.pack(
            side="left",
            padx=20,
            pady=15
        )

        # -----------------------------------------------------
        # Main Frame
        # -----------------------------------------------------

        main_frame = tk.Frame(
            self.window,
            bg="#f5f5f5"
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # -----------------------------------------------------
        # Table Frame
        # -----------------------------------------------------

        table_frame = tk.Frame(
            main_frame
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        columns = (
            "id",
            "question",
            "sql",
            "status",
            "rows",
            "date"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        # -----------------------------------------------------
        # Headings
        # -----------------------------------------------------

        self.tree.heading(
            "id",
            text="ID"
        )

        self.tree.heading(
            "question",
            text="Question"
        )

        self.tree.heading(
            "sql",
            text="SQL Query"
        )

        self.tree.heading(
            "status",
            text="Status"
        )

        self.tree.heading(
            "rows",
            text="Rows"
        )

        self.tree.heading(
            "date",
            text="Created At"
        )

        # -----------------------------------------------------
        # Column Widths
        # -----------------------------------------------------

        self.tree.column(
            "id",
            width=60,
            anchor="center"
        )

        self.tree.column(
            "question",
            width=280
        )

        self.tree.column(
            "sql",
            width=350
        )

        self.tree.column(
            "status",
            width=100,
            anchor="center"
        )

        self.tree.column(
            "rows",
            width=80,
            anchor="center"
        )

        self.tree.column(
            "date",
            width=180
        )

        # -----------------------------------------------------
        # Scrollbars
        # -----------------------------------------------------

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scrollbar.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_frame.grid_rowconfigure(
            0,
            weight=1
        )

        table_frame.grid_columnconfigure(
            0,
            weight=1
        )

        # Double click
        self.tree.bind(
            "<Double-1>",
            self.view_details
        )

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        button_frame = tk.Frame(
            main_frame,
            bg="#f5f5f5"
        )

        button_frame.pack(
            fill="x",
            pady=(10, 0)
        )

        # View Details
        view_button = tk.Button(
            button_frame,
            text="👁 View Details",
            command=self.view_details,
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8
        )

        view_button.pack(
            side="left",
            padx=5
        )

        # Delete
        delete_button = tk.Button(
            button_frame,
            text="🗑 Delete Selected",
            command=self.delete_selected,
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8
        )

        delete_button.pack(
            side="left",
            padx=5
        )

        # Clear
        clear_button = tk.Button(
            button_frame,
            text="🧹 Clear History",
            command=self.clear_history,
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8
        )

        clear_button.pack(
            side="left",
            padx=5
        )

        # Refresh
        refresh_button = tk.Button(
            button_frame,
            text="🔄 Refresh",
            command=self.load_history,
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8
        )

        refresh_button.pack(
            side="right",
            padx=5
        )

        # Close
        close_button = tk.Button(
            button_frame,
            text="Close",
            command=self.window.destroy,
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8
        )

        close_button.pack(
            side="right",
            padx=5
        )

    # =========================================================
    # LOAD HISTORY
    # =========================================================

    def load_history(self):

        # Remove old records from Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        history = QueryHistory.get_history(
            self.username
        )

        for row in history:

            history_id = row[0]
            username = row[1]
            question = row[2]
            sql_query = row[3]
            status = row[4]
            rows_affected = row[5]
            created_at = row[6]

            self.tree.insert(
                "",
                "end",
                values=(
                    history_id,
                    question,
                    sql_query,
                    status,
                    rows_affected,
                    created_at
                )
            )

    # =========================================================
    # GET SELECTED RECORD
    # =========================================================

    def get_selected_record(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a history record first."
            )

            return None

        item = self.tree.item(
            selected[0]
        )

        return item["values"]

    # =========================================================
    # VIEW DETAILS
    # =========================================================

    def view_details(self, event=None):

        record = self.get_selected_record()

        if not record:
            return

        history_id = record[0]
        question = record[1]
        sql_query = record[2]
        status = record[3]
        rows_affected = record[4]
        created_at = record[5]

        detail_window = tk.Toplevel(
            self.window
        )

        detail_window.title(
            "Query Details"
        )

        detail_window.geometry(
            "800x550"
        )

        # -----------------------------------------------------
        # Question
        # -----------------------------------------------------

        tk.Label(
            detail_window,
            text="Natural Language Question",
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        question_text = tk.Text(
            detail_window,
            height=4,
            wrap="word",
            font=("Consolas", 10)
        )

        question_text.pack(
            fill="x",
            padx=15
        )

        question_text.insert(
            "1.0",
            str(question)
        )

        question_text.config(
            state="disabled"
        )

        # -----------------------------------------------------
        # SQL
        # -----------------------------------------------------

        tk.Label(
            detail_window,
            text="Generated SQL",
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        sql_text = tk.Text(
            detail_window,
            height=12,
            wrap="none",
            font=("Consolas", 10)
        )

        sql_text.pack(
            fill="both",
            expand=True,
            padx=15
        )

        sql_text.insert(
            "1.0",
            str(sql_query)
        )

        sql_text.config(
            state="disabled"
        )

        # -----------------------------------------------------
        # Information
        # -----------------------------------------------------

        info = (
            f"History ID: {history_id}\n"
            f"Status: {status}\n"
            f"Rows: {rows_affected}\n"
            f"Created: {created_at}"
        )

        tk.Label(
            detail_window,
            text=info,
            justify="left",
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=15,
            pady=10
        )

        # -----------------------------------------------------
        # Close Button
        # -----------------------------------------------------

        tk.Button(
            detail_window,
            text="Close",
            command=detail_window.destroy,
            padx=20,
            pady=7
        ).pack(
            pady=(0, 15)
        )

    # =========================================================
    # DELETE SELECTED HISTORY
    # =========================================================

    def delete_selected(self):

        record = self.get_selected_record()

        if not record:
            return

        history_id = record[0]

        confirm = messagebox.askyesno(
            "Delete History",
            "Are you sure you want to delete this history record?"
        )

        if not confirm:
            return

        success = QueryHistory.delete_history(
            history_id
        )

        if success:

            messagebox.showinfo(
                "Success",
                "History record deleted successfully."
            )

            self.load_history()

        else:

            messagebox.showerror(
                "Error",
                "Could not delete the history record."
            )

    # =========================================================
    # CLEAR HISTORY
    # =========================================================

    def clear_history(self):

        confirm = messagebox.askyesno(
            "Clear History",
            "Are you sure you want to delete all query history?"
        )

        if not confirm:
            return

        success = QueryHistory.clear_history(
            self.username
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Query history cleared successfully."
            )

            self.load_history()

        else:

            messagebox.showerror(
                "Error",
                "Could not clear query history."
            )


# =========================================================
# TEST THE HISTORY WINDOW
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    HistoryWindow(
        root,
        username="TEST_USER"
    )

    root.mainloop()