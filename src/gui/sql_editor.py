import tkinter as tk
from tkinter import ttk, messagebox

from database.connection import get_connection


class SQLEditor:

    def __init__(self, parent):

        self.parent = parent

        self.history = []

        self.build_gui()

    # =========================================================
    # MAIN GUI
    # =========================================================

    def build_gui(self):

        self.main = tk.Frame(
            self.parent,
            bg="#f1f5f9"
        )

        self.main.pack(
            fill="both",
            expand=True
        )

        # -----------------------------------------------------
        # TITLE
        # -----------------------------------------------------

        title = tk.Label(
            self.main,
            text="SQL Editor",
            font=("Segoe UI", 24, "bold"),
            fg="#0f172a",
            bg="#f1f5f9"
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=(25, 3)
        )

        subtitle = tk.Label(
            self.main,
            text="Write and execute Oracle SQL queries",
            font=("Segoe UI", 11),
            fg="#64748b",
            bg="#f1f5f9"
        )

        subtitle.pack(
            anchor="w",
            padx=30,
            pady=(0, 15)
        )

        # -----------------------------------------------------
        # QUERY EDITOR
        # -----------------------------------------------------

        editor_frame = tk.Frame(
            self.main,
            bg="#0f172a"
        )

        editor_frame.pack(
            fill="x",
            padx=30
        )

        editor_header = tk.Frame(
            editor_frame,
            bg="#1e293b",
            height=40
        )

        editor_header.pack(
            fill="x"
        )

        editor_header.pack_propagate(False)

        editor_title = tk.Label(
            editor_header,
            text="  SQL QUERY",
            font=("Segoe UI", 10, "bold"),
            fg="#cbd5e1",
            bg="#1e293b"
        )

        editor_title.pack(
            side="left",
            pady=8
        )

        self.query_text = tk.Text(
            editor_frame,
            height=9,
            font=("Consolas", 12),
            bg="#0f172a",
            fg="#e2e8f0",
            insertbackground="white",
            selectbackground="#334155",
            selectforeground="white",
            relief="flat",
            wrap="none",
            padx=15,
            pady=12
        )

        self.query_text.pack(
            fill="x"
        )

        # Default query
        self.query_text.insert(
            "1.0",
            "SELECT * FROM EMPLOYEE;"
        )

        # -----------------------------------------------------
        # BUTTON BAR
        # -----------------------------------------------------

        button_frame = tk.Frame(
            self.main,
            bg="#f1f5f9"
        )

        button_frame.pack(
            fill="x",
            padx=30,
            pady=12
        )

        execute_button = tk.Button(
            button_frame,
            text="▶  EXECUTE",
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#2563eb",
            activebackground="#1d4ed8",
            relief="flat",
            cursor="hand2",
            command=self.execute_query
        )

        execute_button.pack(
            side="left",
            ipadx=15,
            ipady=7
        )

        clear_button = tk.Button(
            button_frame,
            text="CLEAR",
            font=("Segoe UI", 10, "bold"),
            fg="#0f172a",
            bg="white",
            relief="flat",
            cursor="hand2",
            command=self.clear_query
        )

        clear_button.pack(
            side="left",
            padx=8,
            ipadx=15,
            ipady=7
        )

        example_button = tk.Button(
            button_frame,
            text="EXAMPLES",
            font=("Segoe UI", 10, "bold"),
            fg="#0f172a",
            bg="white",
            relief="flat",
            cursor="hand2",
            command=self.show_examples
        )

        example_button.pack(
            side="left",
            ipadx=15,
            ipady=7
        )

        # Status
        self.status_label = tk.Label(
            button_frame,
            text="Ready",
            font=("Segoe UI", 10),
            fg="#64748b",
            bg="#f1f5f9"
        )

        self.status_label.pack(
            side="right"
        )

        # -----------------------------------------------------
        # RESULT TITLE
        # -----------------------------------------------------

        result_header = tk.Frame(
            self.main,
            bg="#f1f5f9"
        )

        result_header.pack(
            fill="x",
            padx=30
        )

        result_title = tk.Label(
            result_header,
            text="Query Results",
            font=("Segoe UI", 14, "bold"),
            fg="#0f172a",
            bg="#f1f5f9"
        )

        result_title.pack(
            side="left"
        )

        self.result_info = tk.Label(
            result_header,
            text="",
            font=("Segoe UI", 9),
            fg="#64748b",
            bg="#f1f5f9"
        )

        self.result_info.pack(
            side="right"
        )

        # -----------------------------------------------------
        # RESULT TABLE
        # -----------------------------------------------------

        result_frame = tk.Frame(
            self.main,
            bg="white"
        )

        result_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(8, 25)
        )

        self.result_tree = ttk.Treeview(
            result_frame,
            show="headings"
        )

        self.result_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        vertical_scrollbar = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=self.result_tree.yview
        )

        vertical_scrollbar.pack(
            side="right",
            fill="y"
        )

        horizontal_scrollbar = ttk.Scrollbar(
            self.main,
            orient="horizontal",
            command=self.result_tree.xview
        )

        horizontal_scrollbar.pack(
            fill="x",
            padx=30,
            pady=(0, 5)
        )

        self.result_tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

    # =========================================================
    # EXECUTE QUERY
    # =========================================================

    def execute_query(self):

        query = self.query_text.get(
            "1.0",
            "end"
        ).strip()

        if not query:

            messagebox.showwarning(
                "SQL Editor",
                "Please enter a SQL query.",
                parent=self.parent
            )

            return

        # Remove final semicolon
        query = query.rstrip(";").strip()

        if not query:

            return

        connection = None
        cursor = None

        try:

            self.status_label.config(
                text="Executing..."
            )

            self.parent.update_idletasks()

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute(
                query
            )

            # -------------------------------------------------
            # SELECT / RETURNING
            # -------------------------------------------------

            if cursor.description:

                columns = [
                    column[0]
                    for column in cursor.description
                ]

                rows = cursor.fetchall()

                self.show_results(
                    columns,
                    rows
                )

                self.result_info.config(
                    text=f"{len(rows)} row(s)"
                )

                self.status_label.config(
                    text="✓ Query executed successfully"
                )

            # -------------------------------------------------
            # INSERT / UPDATE / DELETE / DDL
            # -------------------------------------------------

            else:

                connection.commit()

                affected = cursor.rowcount

                self.clear_results()

                self.status_label.config(
                    text="✓ Query executed successfully"
                )

                self.result_info.config(
                    text=f"Rows affected: {affected}"
                )

                self.show_message_result(
                    f"Query executed successfully.\n\n"
                    f"Rows affected: {affected}"
                )

            # Add history
            self.add_history(
                query
            )

        except Exception as error:

            if connection:

                connection.rollback()

            self.clear_results()

            self.show_message_result(
                f"SQL ERROR\n\n{error}"
            )

            self.status_label.config(
                text="✗ SQL execution failed"
            )

            self.result_info.config(
                text="Error"
            )

        finally:

            if cursor:

                cursor.close()

            if connection:

                connection.close()

    # =========================================================
    # SHOW RESULTS
    # =========================================================

    def show_results(
        self,
        columns,
        rows
    ):

        self.clear_results()

        self.result_tree["columns"] = columns

        for column in columns:

            self.result_tree.heading(
                column,
                text=column
            )

            self.result_tree.column(
                column,
                width=150,
                minwidth=100,
                anchor="center"
            )

        for row in rows:

            values = []

            for value in row:

                if value is None:

                    values.append("NULL")

                else:

                    values.append(
                        str(value)
                    )

            self.result_tree.insert(
                "",
                "end",
                values=values
            )

    # =========================================================
    # CLEAR RESULTS
    # =========================================================

    def clear_results(self):

        for item in self.result_tree.get_children():

            self.result_tree.delete(
                item
            )

        self.result_tree["columns"] = ()

    # =========================================================
    # MESSAGE RESULT
    # =========================================================

    def show_message_result(
        self,
        message
    ):

        self.clear_results()

        self.result_tree["columns"] = (
            "MESSAGE",
        )

        self.result_tree.heading(
            "MESSAGE",
            text="MESSAGE"
        )

        self.result_tree.column(
            "MESSAGE",
            width=800,
            anchor="w"
        )

        self.result_tree.insert(
            "",
            "end",
            values=(message,)
        )

    # =========================================================
    # CLEAR QUERY
    # =========================================================

    def clear_query(self):

        self.query_text.delete(
            "1.0",
            "end"
        )

        self.clear_results()

        self.status_label.config(
            text="Ready"
        )

        self.result_info.config(
            text=""
        )

    # =========================================================
    # EXAMPLES
    # =========================================================

    def show_examples(self):

        window = tk.Toplevel(
            self.parent
        )

        window.title(
            "SQL Examples"
        )

        window.geometry(
            "750x550"
        )

        window.configure(
            bg="#f1f5f9"
        )

        title = tk.Label(
            window,
            text="SQL Examples",
            font=("Segoe UI", 20, "bold"),
            fg="#0f172a",
            bg="#f1f5f9"
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=20
        )

        examples = tk.Text(
            window,
            font=("Consolas", 11),
            bg="#0f172a",
            fg="#e2e8f0",
            relief="flat",
            padx=15,
            pady=15,
            wrap="word"
        )

        examples.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
        )

        example_text = """SELECT * FROM EMPLOYEE;

SELECT NAME, SALARY
FROM EMPLOYEE
WHERE SALARY > 40000;

SELECT *
FROM STUDENTS
WHERE MARKS > 80;

SELECT COUNT(*)
FROM EMPLOYEE;

SELECT DEPARTMENT, AVG(SALARY)
FROM EMPLOYEE
GROUP BY DEPARTMENT;

INSERT INTO EMPLOYEE
(EMPLOYEE_ID, NAME, EMAIL, DEPARTMENT, SALARY)
VALUES
(10, 'Test User', 'test@example.com', 'IT', 50000);

UPDATE EMPLOYEE
SET SALARY = 60000
WHERE EMPLOYEE_ID = 10;

DELETE FROM EMPLOYEE
WHERE EMPLOYEE_ID = 10;
"""

        examples.insert(
            "1.0",
            example_text
        )

        examples.configure(
            state="disabled"
        )

    # =========================================================
    # QUERY HISTORY
    # =========================================================

    def add_history(
        self,
        query
    ):

        self.history.insert(
            0,
            query
        )

        # Keep last 20 queries
        self.history = self.history[:20]