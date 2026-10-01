import tkinter as tk
from tkinter import ttk, messagebox

from database.connection import get_connection
from ai.ai_service import OllamaAI
from utils.sql_validator import SQLValidator

from database.query_history import QueryHistory
from gui.history import HistoryWindow


class AIAssistant:

    def __init__(self, parent, username=None):

        self.parent = parent

        # Logged-in username
        self.username = username if username else "UNKNOWN"

        # Ollama AI
        self.ai = OllamaAI(
            model="mistral:latest"
        )

        # Main frame
        self.frame = tk.Frame(
            parent,
            bg="#f5f7fb"
        )

        self.frame.pack(
            fill="both",
            expand=True
        )

        self.create_interface()

    # =========================================================
    # INTERFACE
    # =========================================================

    def create_interface(self):

        # -----------------------------------------------------
        # TITLE
        # -----------------------------------------------------

        title = tk.Label(
            self.frame,
            text="🤖 AI Database Assistant",
            font=("Segoe UI", 24, "bold"),
            bg="#f5f7fb",
            fg="#1f2937"
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=(20, 3)
        )

        # -----------------------------------------------------
        # SUBTITLE
        # -----------------------------------------------------

        subtitle = tk.Label(
            self.frame,
            text=(
                "Ask questions about your Oracle database "
                "using natural language."
            ),
            font=("Segoe UI", 11),
            bg="#f5f7fb",
            fg="#6b7280"
        )

        subtitle.pack(
            anchor="w",
            padx=30,
            pady=(0, 8)
        )

        # -----------------------------------------------------
        # OLLAMA STATUS
        # -----------------------------------------------------

        status_frame = tk.Frame(
            self.frame,
            bg="#f5f7fb"
        )

        status_frame.pack(
            fill="x",
            padx=30
        )

        self.connection_label = tk.Label(
            status_frame,
            text="● Checking Ollama...",
            font=("Segoe UI", 10, "bold"),
            bg="#f5f7fb",
            fg="#f59e0b"
        )

        self.connection_label.pack(
            anchor="w"
        )

        self.check_ollama()

        # =====================================================
        # QUESTION SECTION
        # =====================================================

        question_frame = tk.Frame(
            self.frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        question_frame.pack(
            fill="x",
            padx=30,
            pady=8
        )

        question_title = tk.Label(
            question_frame,
            text="Ask your database",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg="#111827"
        )

        question_title.pack(
            anchor="w",
            padx=20,
            pady=(12, 4)
        )

        self.question_text = tk.Text(
            question_frame,
            height=3,
            font=("Segoe UI", 11),
            wrap="word",
            bd=1,
            relief="solid"
        )

        self.question_text.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.question_text.insert(
            "1.0",
            "Example: Show all employees"
        )

        # -----------------------------------------------------
        # QUESTION BUTTONS
        # -----------------------------------------------------

        button_frame = tk.Frame(
            question_frame,
            bg="white"
        )

        button_frame.pack(
            anchor="e",
            padx=20,
            pady=(0, 12)
        )

        # Generate SQL
        generate_button = tk.Button(
            button_frame,
            text="✨ Generate SQL",
            command=self.generate_sql,
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            padx=20,
            pady=7,
            bd=0,
            cursor="hand2"
        )

        generate_button.pack(
            side="left",
            padx=5
        )

        # Clear
        clear_button = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_all,
            font=("Segoe UI", 10),
            padx=20,
            pady=7,
            cursor="hand2"
        )

        clear_button.pack(
            side="left",
            padx=5
        )

        # History
        history_button = tk.Button(
            button_frame,
            text="📜 History",
            command=self.open_history,
            font=("Segoe UI", 10, "bold"),
            bg="#7c3aed",
            fg="white",
            activebackground="#6d28d9",
            activeforeground="white",
            padx=20,
            pady=7,
            bd=0,
            cursor="hand2"
        )

        history_button.pack(
            side="left",
            padx=5
        )

        # =====================================================
        # GENERATED SQL SECTION
        # =====================================================

        sql_frame = tk.Frame(
            self.frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        sql_frame.pack(
            fill="x",
            padx=30,
            pady=8
        )

        sql_title = tk.Label(
            sql_frame,
            text="Generated SQL",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg="#111827"
        )

        sql_title.pack(
            anchor="w",
            padx=20,
            pady=(12, 4)
        )

        # -----------------------------------------------------
        # SQL TEXT
        # -----------------------------------------------------

        sql_text_frame = tk.Frame(
            sql_frame,
            bg="#111827",
            height=110
        )

        sql_text_frame.pack(
            fill="x",
            padx=20,
            pady=8
        )

        sql_text_frame.pack_propagate(False)

        self.sql_text = tk.Text(
            sql_text_frame,
            height=5,
            font=("Consolas", 11),
            bg="#111827",
            fg="#e5e7eb",
            insertbackground="white",
            wrap="word",
            bd=0,
            padx=10,
            pady=8
        )

        self.sql_text.pack(
            fill="both",
            expand=True
        )

        # -----------------------------------------------------
        # SQL BUTTON
        # -----------------------------------------------------

        sql_button_frame = tk.Frame(
            sql_frame,
            bg="white"
        )

        sql_button_frame.pack(
            anchor="e",
            padx=20,
            pady=(0, 12)
        )

        execute_button = tk.Button(
            sql_button_frame,
            text="▶ Execute SQL",
            command=self.execute_sql,
            font=("Segoe UI", 10, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            padx=20,
            pady=7,
            bd=0,
            cursor="hand2"
        )

        execute_button.pack(
            side="left",
            padx=5
        )

        # =====================================================
        # QUERY RESULT SECTION
        # =====================================================

        self.result_frame = tk.Frame(
            self.frame,
            bg="white",
            bd=1,
            relief="solid",
            height=300
        )

        self.result_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 15)
        )

        self.result_frame.pack_propagate(False)

        # -----------------------------------------------------
        # RESULT TITLE
        # -----------------------------------------------------

        result_title = tk.Label(
            self.result_frame,
            text="Query Result",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg="#111827"
        )

        result_title.pack(
            anchor="w",
            padx=20,
            pady=(12, 4)
        )

        # -----------------------------------------------------
        # TREE CONTAINER
        # -----------------------------------------------------

        tree_container = tk.Frame(
            self.result_frame,
            bg="white"
        )

        tree_container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=8
        )

        # -----------------------------------------------------
        # TREEVIEW
        # -----------------------------------------------------

        self.result_tree = ttk.Treeview(
            tree_container,
            show="headings"
        )

        self.result_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        # -----------------------------------------------------
        # VERTICAL SCROLLBAR
        # -----------------------------------------------------

        vertical_scrollbar = ttk.Scrollbar(
            tree_container,
            orient="vertical",
            command=self.result_tree.yview
        )

        vertical_scrollbar.pack(
            side="right",
            fill="y"
        )

        # -----------------------------------------------------
        # HORIZONTAL SCROLLBAR
        # -----------------------------------------------------

        horizontal_scrollbar = ttk.Scrollbar(
            self.result_frame,
            orient="horizontal",
            command=self.result_tree.xview
        )

        horizontal_scrollbar.pack(
            side="bottom",
            fill="x",
            padx=20
        )

        self.result_tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        self.status_label = tk.Label(
            self.result_frame,
            text="Ready",
            font=("Segoe UI", 9),
            bg="white",
            fg="#6b7280"
        )

        self.status_label.pack(
            anchor="w",
            padx=20,
            pady=(4, 8)
        )

    # =========================================================
    # CHECK OLLAMA
    # =========================================================

    def check_ollama(self):

        if self.ai.check_connection():

            self.connection_label.config(
                text="● Ollama Connected  |  Mistral Ready",
                fg="#16a34a"
            )

        else:

            self.connection_label.config(
                text="● Ollama Not Connected",
                fg="#dc2626"
            )

    # =========================================================
    # GET DATABASE SCHEMA
    # =========================================================

    def get_database_schema(self):

        connection = None
        cursor = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    TABLE_NAME,
                    COLUMN_NAME,
                    DATA_TYPE
                FROM USER_TAB_COLUMNS
                ORDER BY
                    TABLE_NAME,
                    COLUMN_ID
            """)

            rows = cursor.fetchall()

            schema = {}

            for (
                table_name,
                column_name,
                data_type
            ) in rows:

                if table_name not in schema:

                    schema[table_name] = []

                schema[table_name].append(
                    f"{column_name} ({data_type})"
                )

            return schema

        except Exception as e:

            messagebox.showerror(
                "Schema Error",
                str(e),
                parent=self.parent
            )

            return {}

        finally:

            try:

                if cursor:
                    cursor.close()

                if connection:
                    connection.close()

            except Exception:
                pass

    # =========================================================
    # GENERATE SQL USING MISTRAL
    # =========================================================

    def generate_sql(self):

        question = (
            self.question_text
            .get(
                "1.0",
                "end"
            )
            .strip()
        )

        if not question:

            messagebox.showwarning(
                "Missing Question",
                "Please enter a database question.",
                parent=self.parent
            )

            return

        self.status_label.config(
            text="Reading Oracle database schema..."
        )

        self.parent.update_idletasks()

        schema = self.get_database_schema()

        if not schema:

            self.status_label.config(
                text="No database schema found."
            )

            return

        self.status_label.config(
            text="Mistral is generating SQL..."
        )

        self.parent.update_idletasks()

        success, result = self.ai.generate_sql(
            question,
            schema
        )

        if not success:

            messagebox.showerror(
                "AI Error",
                result,
                parent=self.parent
            )

            self.status_label.config(
                text="AI generation failed."
            )

            return

        # -----------------------------------------------------
        # DISPLAY GENERATED SQL
        # -----------------------------------------------------

        self.sql_text.delete(
            "1.0",
            "end"
        )

        self.sql_text.insert(
            "1.0",
            result
        )

        self.status_label.config(
            text="SQL generated. Review it before execution."
        )

    # =========================================================
    # EXECUTE SQL WITH VALIDATION
    # =========================================================

    def execute_sql(self):

        sql = (
            self.sql_text
            .get(
                "1.0",
                "end"
            )
            .strip()
        )

        if not sql:

            messagebox.showwarning(
                "No SQL",
                "Generate SQL first.",
                parent=self.parent
            )

            return

        # =====================================================
        # GET CURRENT DATABASE SCHEMA
        # =====================================================

        self.status_label.config(
            text="Validating SQL..."
        )

        self.parent.update_idletasks()

        schema = self.get_database_schema()

        if not schema:

            self.status_label.config(
                text="Unable to retrieve database schema."
            )

            return

        # =====================================================
        # SQL VALIDATION
        # =====================================================

        valid, validation_message = SQLValidator.validate(
            sql,
            schema
        )

        if not valid:

            self.status_label.config(
                text="SQL validation failed."
            )

            # Save validation failure to history
            try:

                QueryHistory.save_history(
                    username=self.username,
                    question=self.question_text.get(
                        "1.0",
                        "end"
                    ).strip(),
                    sql_query=sql,
                    status="VALIDATION_FAILED",
                    rows_affected=0
                )

            except Exception:
                pass

            messagebox.showerror(
                "SQL Validation Failed",
                (
                    "The generated SQL could not be validated.\n\n"
                    f"Reason:\n{validation_message}\n\n"
                    "Please edit the SQL and try again."
                ),
                parent=self.parent
            )

            return

        # =====================================================
        # CLEAN SQL
        # =====================================================

        clean_sql = sql.rstrip(";").strip()

        upper_sql = clean_sql.upper()

        # =====================================================
        # CONFIRM EXECUTION
        # =====================================================

        if upper_sql.startswith("SELECT"):

            answer = messagebox.askyesno(
                "Confirm SQL Execution",
                (
                    "✓ SQL validation successful.\n\n"
                    "Do you want to execute this query?\n\n"
                    f"{sql}"
                ),
                parent=self.parent
            )

        else:

            answer = messagebox.askyesno(
                "Confirm Database Modification",
                (
                    "⚠ This SQL may modify your database.\n\n"
                    "✓ SQL validation successful.\n\n"
                    "Do you want to continue?\n\n"
                    f"{sql}"
                ),
                parent=self.parent
            )

        if not answer:

            self.status_label.config(
                text="Execution cancelled by user."
            )

            # Save cancelled query
            try:

                QueryHistory.save_history(
                    username=self.username,
                    question=self.question_text.get(
                        "1.0",
                        "end"
                    ).strip(),
                    sql_query=clean_sql,
                    status="CANCELLED",
                    rows_affected=0
                )

            except Exception:
                pass

            return

        # =====================================================
        # EXECUTE SQL
        # =====================================================

        connection = None
        cursor = None

        try:

            self.status_label.config(
                text="Executing SQL..."
            )

            self.parent.update_idletasks()

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute(
                clean_sql
            )

            # =================================================
            # SELECT QUERY
            # =================================================

            if cursor.description:

                columns = [
                    column[0]
                    for column in cursor.description
                ]

                rows = cursor.fetchall()

                self.display_results(
                    columns,
                    rows
                )

                # Save successful SELECT query
                try:

                    QueryHistory.save_history(
                        username=self.username,
                        question=self.question_text.get(
                            "1.0",
                            "end"
                        ).strip(),
                        sql_query=clean_sql,
                        status="SUCCESS",
                        rows_affected=len(rows)
                    )

                except Exception:
                    pass

                self.status_label.config(
                    text=(
                        "✓ Query successful — "
                        f"{len(rows)} row(s) returned."
                    )
                )

            # =================================================
            # INSERT / UPDATE / DELETE / DDL
            # =================================================

            else:

                connection.commit()

                self.clear_results()

                affected = cursor.rowcount

                # Save successful modification
                try:

                    QueryHistory.save_history(
                        username=self.username,
                        question=self.question_text.get(
                            "1.0",
                            "end"
                        ).strip(),
                        sql_query=clean_sql,
                        status="SUCCESS",
                        rows_affected=affected
                    )

                except Exception:
                    pass

                self.status_label.config(
                    text=(
                        "✓ SQL executed successfully — "
                        f"{affected} row(s) affected."
                    )
                )

                messagebox.showinfo(
                    "Success",
                    (
                        "SQL executed successfully.\n\n"
                        f"Rows affected: {affected}"
                    ),
                    parent=self.parent
                )

        except Exception as e:

            if connection:

                try:

                    connection.rollback()

                except Exception:
                    pass

            # Save failed query
            try:

                QueryHistory.save_history(
                    username=self.username,
                    question=self.question_text.get(
                        "1.0",
                        "end"
                    ).strip(),
                    sql_query=clean_sql,
                    status="FAILED",
                    rows_affected=0
                )

            except Exception:
                pass

            messagebox.showerror(
                "SQL Execution Error",
                str(e),
                parent=self.parent
            )

            self.status_label.config(
                text="SQL execution failed."
            )

        finally:

            try:

                if cursor:
                    cursor.close()

                if connection:
                    connection.close()

            except Exception:
                pass

    # =========================================================
    # OPEN QUERY HISTORY
    # =========================================================

    def open_history(self):

        try:

            HistoryWindow(
                self.parent,
                username=self.username
            )

        except Exception as e:

            messagebox.showerror(
                "History Error",
                (
                    "Unable to open Query History.\n\n"
                    f"{e}"
                ),
                parent=self.parent
            )

    # =========================================================
    # DISPLAY RESULTS
    # =========================================================

    def display_results(
        self,
        columns,
        rows
    ):

        # -----------------------------------------------------
        # Clear old results
        # -----------------------------------------------------

        self.clear_results()

        # -----------------------------------------------------
        # Set Treeview columns
        # -----------------------------------------------------

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
                anchor="center",
                stretch=True
            )

        # -----------------------------------------------------
        # Insert rows
        # -----------------------------------------------------

        for row in rows:

            self.result_tree.insert(
                "",
                "end",
                values=row
            )

        # -----------------------------------------------------
        # Scroll to first result
        # -----------------------------------------------------

        children = self.result_tree.get_children()

        if children:

            self.result_tree.see(
                children[0]
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
    # CLEAR EVERYTHING
    # =========================================================

    def clear_all(self):

        self.question_text.delete(
            "1.0",
            "end"
        )

        self.sql_text.delete(
            "1.0",
            "end"
        )

        self.clear_results()

        self.status_label.config(
            text="Ready"
        )

        self.question_text.insert(
            "1.0",
            "Example: Show all employees"
        )