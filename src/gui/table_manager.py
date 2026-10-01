import tkinter as tk
from tkinter import ttk, messagebox
import re

from database.connection import get_connection


class TableManager:

    def __init__(
        self,
        parent,
        table_name
    ):

        self.parent = parent
        self.table_name = table_name.upper()

        self.columns = []
        self.primary_key = None
        self.identity_columns = []

        # Validate table name
        if not self.valid_identifier(
            self.table_name
        ):

            messagebox.showerror(
                "Error",
                "Invalid table name.",
                parent=parent
            )

            return

        self.window = tk.Toplevel(
            parent
        )

        self.window.title(
            f"Smart DB Manager - {self.table_name}"
        )

        self.window.geometry(
            "1100x650"
        )

        self.window.minsize(
            900,
            550
        )

        self.window.configure(
            bg="#f1f5f9"
        )

        self.load_schema()

        self.build_gui()

        self.load_data()

    # =========================================================
    # VALIDATE IDENTIFIER
    # =========================================================

    def valid_identifier(
        self,
        value
    ):

        return bool(
            re.fullmatch(
                r"[A-Z][A-Z0-9_$#]*",
                value
            )
        )

    # =========================================================
    # LOAD ORACLE TABLE STRUCTURE
    # =========================================================

    def load_schema(self):

        connection = None
        cursor = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            # -------------------------------------------------
            # Columns
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    column_name
                FROM
                    user_tab_columns
                WHERE
                    table_name = :table_name
                ORDER BY
                    column_id
                """,
                {
                    "table_name": self.table_name
                }
            )

            result = cursor.fetchall()

            self.columns = [
                row[0]
                for row in result
            ]

            if not self.columns:

                raise Exception(
                    f"Table {self.table_name} does not exist."
                )

            # -------------------------------------------------
            # Primary key
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    cols.column_name
                FROM
                    user_constraints cons
                    JOIN user_cons_columns cols
                    ON cons.constraint_name =
                       cols.constraint_name
                WHERE
                    cons.constraint_type = 'P'
                    AND cons.table_name = :table_name
                ORDER BY
                    cols.position
                """,
                {
                    "table_name": self.table_name
                }
            )

            pk_result = cursor.fetchone()

            if pk_result:

                self.primary_key = pk_result[0]

            # -------------------------------------------------
            # Identity columns
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    column_name
                FROM
                    user_tab_identity_cols
                WHERE
                    table_name = :table_name
                """,
                {
                    "table_name": self.table_name
                }
            )

            identity_result = cursor.fetchall()

            self.identity_columns = [
                row[0]
                for row in identity_result
            ]

        finally:

            if cursor:

                cursor.close()

            if connection:

                connection.close()

    # =========================================================
    # BUILD GUI
    # =========================================================

    def build_gui(self):

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        header = tk.Frame(
            self.window,
            bg="white",
            height=75
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title = tk.Label(
            header,
            text=f"Table: {self.table_name}",
            font=("Segoe UI", 20, "bold"),
            fg="#0f172a",
            bg="white"
        )

        title.pack(
            side="left",
            padx=25
        )

        # -----------------------------------------------------
        # Toolbar
        # -----------------------------------------------------

        toolbar = tk.Frame(
            self.window,
            bg="#f1f5f9"
        )

        toolbar.pack(
            fill="x",
            padx=25,
            pady=15
        )

        self.create_button(
            toolbar,
            "➕ Insert",
            self.open_insert_window,
            "#16a34a"
        )

        self.create_button(
            toolbar,
            "✏ Update",
            self.open_update_window,
            "#2563eb"
        )

        self.create_button(
            toolbar,
            "🗑 Delete",
            self.delete_selected,
            "#dc2626"
        )

        self.create_button(
            toolbar,
            "↻ Refresh",
            self.load_data,
            "#475569"
        )

        # -----------------------------------------------------
        # Table container
        # -----------------------------------------------------

        table_container = tk.Frame(
            self.window,
            bg="white"
        )

        table_container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
        )

        self.tree = ttk.Treeview(
            table_container,
            columns=self.columns,
            show="headings"
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        vertical_scrollbar = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.tree.yview
        )

        vertical_scrollbar.pack(
            side="right",
            fill="y"
        )

        horizontal_scrollbar = ttk.Scrollbar(
            self.window,
            orient="horizontal",
            command=self.tree.xview
        )

        horizontal_scrollbar.pack(
            fill="x",
            padx=25,
            pady=(0, 10)
        )

        self.tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        for column in self.columns:

            self.tree.heading(
                column,
                text=column
            )

            self.tree.column(
                column,
                width=160,
                minwidth=100,
                anchor="center"
            )

        # Double click = Update
        self.tree.bind(
            "<Double-1>",
            lambda event: self.open_update_window()
        )

    # =========================================================
    # BUTTON
    # =========================================================

    def create_button(
        self,
        parent,
        text,
        command,
        color
    ):

        button = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg=color,
            activebackground=color,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=command
        )

        button.pack(
            side="left",
            padx=(0, 10),
            ipadx=12,
            ipady=7
        )

    # =========================================================
    # LOAD DATA
    # =========================================================

    def load_data(self):

        if not hasattr(
            self,
            "tree"
        ):

            return

        connection = None
        cursor = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            query = (
                f"SELECT * FROM {self.table_name}"
            )

            cursor.execute(
                query
            )

            rows = cursor.fetchall()

            # Clear old records
            for item in self.tree.get_children():

                self.tree.delete(
                    item
                )

            # Insert records
            for row in rows:

                values = []

                for value in row:

                    if value is None:

                        values.append("")

                    else:

                        values.append(
                            str(value)
                        )

                self.tree.insert(
                    "",
                    "end",
                    values=values
                )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error),
                parent=self.window
            )

        finally:

            if cursor:

                cursor.close()

            if connection:

                connection.close()

    # =========================================================
    # INSERT WINDOW
    # =========================================================

    def open_insert_window(self):

        window = tk.Toplevel(
            self.window
        )

        window.title(
            f"Insert - {self.table_name}"
        )

        window.geometry(
            "600x650"
        )

        window.configure(
            bg="#f1f5f9"
        )

        title = tk.Label(
            window,
            text=f"Insert into {self.table_name}",
            font=("Segoe UI", 20, "bold"),
            fg="#0f172a",
            bg="#f1f5f9"
        )

        title.pack(
            pady=20
        )

        form = tk.Frame(
            window,
            bg="#f1f5f9"
        )

        form.pack(
            fill="both",
            expand=True,
            padx=35
        )

        entries = {}

        row_number = 0

        for column in self.columns:

            label = tk.Label(
                form,
                text=column,
                font=("Segoe UI", 10, "bold"),
                fg="#334155",
                bg="#f1f5f9"
            )

            label.grid(
                row=row_number,
                column=0,
                sticky="w",
                pady=6
            )

            entry = ttk.Entry(
                form,
                font=("Segoe UI", 11)
            )

            entry.grid(
                row=row_number,
                column=1,
                sticky="ew",
                padx=(20, 0),
                pady=6,
                ipady=5
            )

            entries[column] = entry

            # Identity columns are generated by Oracle
            if column in self.identity_columns:

                entry.insert(
                    0,
                    "(AUTO)"
                )

                entry.configure(
                    state="disabled"
                )

            row_number += 1

        form.columnconfigure(
            1,
            weight=1
        )

        # -----------------------------------------------------
        # INSERT
        # -----------------------------------------------------

        def insert_record():

            connection = None
            cursor = None

            try:

                data_columns = []
                data_values = []
                bind_values = {}

                for column in self.columns:

                    # Skip identity column
                    if column in self.identity_columns:

                        continue

                    value = entries[
                        column
                    ].get().strip()

                    # Skip empty values
                    if value == "":

                        continue

                    data_columns.append(
                        column
                    )

                    bind_name = (
                        f"v{len(bind_values)}"
                    )

                    data_values.append(
                        f":{bind_name}"
                    )

                    bind_values[
                        bind_name
                    ] = value

                if not data_columns:

                    messagebox.showwarning(
                        "Insert",
                        "Please enter at least one value.",
                        parent=window
                    )

                    return

                connection = get_connection()

                cursor = connection.cursor()

                query = (
                    f"INSERT INTO {self.table_name} "
                    f"({', '.join(data_columns)}) "
                    f"VALUES "
                    f"({', '.join(data_values)})"
                )

                cursor.execute(
                    query,
                    bind_values
                )

                connection.commit()

                messagebox.showinfo(
                    "Success",
                    "Record inserted successfully.",
                    parent=window
                )

                window.destroy()

                self.load_data()

            except Exception as error:

                if connection:

                    connection.rollback()

                messagebox.showerror(
                    "Insert Error",
                    str(error),
                    parent=window
                )

            finally:

                if cursor:

                    cursor.close()

                if connection:

                    connection.close()

        button = tk.Button(
            window,
            text="INSERT RECORD",
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#16a34a",
            relief="flat",
            cursor="hand2",
            command=insert_record
        )

        button.pack(
            pady=20,
            ipadx=25,
            ipady=9
        )

    # =========================================================
    # SELECTED ROW
    # =========================================================

    def get_selected_row(self):

        selection = self.tree.selection()

        if not selection:

            messagebox.showwarning(
                "Select Record",
                "Please select a record first.",
                parent=self.window
            )

            return None

        item = self.tree.item(
            selection[0]
        )

        return item["values"]

    # =========================================================
    # UPDATE WINDOW
    # =========================================================

    def open_update_window(self):

        selected_row = self.get_selected_row()

        if selected_row is None:

            return

        if not self.primary_key:

            messagebox.showerror(
                "Update",
                "This table does not have a primary key.",
                parent=self.window
            )

            return

        try:

            primary_index = self.columns.index(
                self.primary_key
            )

        except ValueError:

            messagebox.showerror(
                "Update",
                "Primary key column not found.",
                parent=self.window
            )

            return

        primary_value = selected_row[
            primary_index
        ]

        window = tk.Toplevel(
            self.window
        )

        window.title(
            f"Update - {self.table_name}"
        )

        window.geometry(
            "600x650"
        )

        window.configure(
            bg="#f1f5f9"
        )

        title = tk.Label(
            window,
            text=f"Update {self.table_name}",
            font=("Segoe UI", 20, "bold"),
            fg="#0f172a",
            bg="#f1f5f9"
        )

        title.pack(
            pady=20
        )

        form = tk.Frame(
            window,
            bg="#f1f5f9"
        )

        form.pack(
            fill="both",
            expand=True,
            padx=35
        )

        entries = {}

        for index, column in enumerate(
            self.columns
        ):

            label = tk.Label(
                form,
                text=column,
                font=("Segoe UI", 10, "bold"),
                fg="#334155",
                bg="#f1f5f9"
            )

            label.grid(
                row=index,
                column=0,
                sticky="w",
                pady=6
            )

            entry = ttk.Entry(
                form,
                font=("Segoe UI", 11)
            )

            entry.grid(
                row=index,
                column=1,
                sticky="ew",
                padx=(20, 0),
                pady=6,
                ipady=5
            )

            value = selected_row[index]

            if value is not None:

                entry.insert(
                    0,
                    str(value)
                )

            entries[column] = entry

            # Primary key cannot be changed
            if column == self.primary_key:

                entry.configure(
                    state="disabled"
                )

        form.columnconfigure(
            1,
            weight=1
        )

        # -----------------------------------------------------
        # UPDATE
        # -----------------------------------------------------

        def update_record():

            connection = None
            cursor = None

            try:

                set_parts = []
                bind_values = {}

                for column in self.columns:

                    if column == self.primary_key:

                        continue

                    value = entries[
                        column
                    ].get().strip()

                    bind_name = (
                        f"v{len(bind_values)}"
                    )

                    set_parts.append(
                        f"{column} = :{bind_name}"
                    )

                    bind_values[
                        bind_name
                    ] = value

                bind_values[
                    "primary_value"
                ] = primary_value

                query = (
                    f"UPDATE {self.table_name} "
                    f"SET {', '.join(set_parts)} "
                    f"WHERE {self.primary_key} "
                    f"= :primary_value"
                )

                connection = get_connection()

                cursor = connection.cursor()

                cursor.execute(
                    query,
                    bind_values
                )

                connection.commit()

                messagebox.showinfo(
                    "Success",
                    "Record updated successfully.",
                    parent=window
                )

                window.destroy()

                self.load_data()

            except Exception as error:

                if connection:

                    connection.rollback()

                messagebox.showerror(
                    "Update Error",
                    str(error),
                    parent=window
                )

            finally:

                if cursor:

                    cursor.close()

                if connection:

                    connection.close()

        button = tk.Button(
            window,
            text="UPDATE RECORD",
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#2563eb",
            relief="flat",
            cursor="hand2",
            command=update_record
        )

        button.pack(
            pady=20,
            ipadx=25,
            ipady=9
        )

    # =========================================================
    # DELETE
    # =========================================================

    def delete_selected(self):

        selected_row = self.get_selected_row()

        if selected_row is None:

            return

        if not self.primary_key:

            messagebox.showerror(
                "Delete",
                "This table does not have a primary key.",
                parent=self.window
            )

            return

        try:

            primary_index = self.columns.index(
                self.primary_key
            )

        except ValueError:

            messagebox.showerror(
                "Delete",
                "Primary key column not found.",
                parent=self.window
            )

            return

        primary_value = selected_row[
            primary_index
        ]

        answer = messagebox.askyesno(
            "Confirm Delete",
            (
                "Are you sure you want to delete "
                "this record?\n\n"
                f"{self.primary_key}: "
                f"{primary_value}"
            ),
            parent=self.window
        )

        if not answer:

            return

        connection = None
        cursor = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            query = (
                f"DELETE FROM {self.table_name} "
                f"WHERE {self.primary_key} "
                f"= :primary_value"
            )

            cursor.execute(
                query,
                {
                    "primary_value": primary_value
                }
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Record deleted successfully.",
                parent=self.window
            )

            self.load_data()

        except Exception as error:

            if connection:

                connection.rollback()

            messagebox.showerror(
                "Delete Error",
                str(error),
                parent=self.window
            )

        finally:

            if cursor:

                cursor.close()

            if connection:

                connection.close()