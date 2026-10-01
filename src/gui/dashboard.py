import tkinter as tk
from tkinter import ttk, messagebox

from database.connection import get_connection
from database.schema import get_tables, create_table

from gui.table_manager import TableManager
from gui.sql_editor import SQLEditor
from gui.ai_assistant import AIAssistant


class DashboardWindow:

    def __init__(
        self,
        root,
        username,
        logout_callback
    ):

        self.root = root
        self.username = username
        self.logout_callback = logout_callback

        self.tables = []

        self.root.title(
            "Smart DB Manager - Dashboard"
        )

        self.root.geometry(
            "1200x750"
        )

        self.root.minsize(
            1000,
            650
        )

        self.root.configure(
            bg="#f1f5f9"
        )

        self.build_gui()
        self.load_tables()

    # =========================================================
    # MAIN GUI
    # =========================================================

    def build_gui(self):

        self.main_frame = tk.Frame(
            self.root,
            bg="#f1f5f9"
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        # Sidebar
        self.create_sidebar()

        # Content area
        self.content = tk.Frame(
            self.main_frame,
            bg="#f1f5f9"
        )

        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Header
        self.create_header()

        # Dashboard
        self.create_dashboard_content()

    # =========================================================
    # SIDEBAR
    # =========================================================

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.main_frame,
            width=230,
            bg="#0f172a"
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # Logo
        logo = tk.Label(
            self.sidebar,
            text="🗄 SMART DB",
            font=("Segoe UI", 18, "bold"),
            fg="#38bdf8",
            bg="#0f172a"
        )

        logo.pack(
            pady=(30, 40)
        )

        # Dashboard
        self.create_sidebar_button(
            "Dashboard",
            self.show_dashboard
        )

        # Tables
        self.create_sidebar_button(
            "Tables",
            self.show_tables
        )

        # SQL Editor
        self.create_sidebar_button(
            "SQL Editor",
            self.show_sql_editor
        )

        # AI Assistant
        self.create_sidebar_button(
            "🤖 AI Assistant",
            self.show_ai_assistant
        )

        # Create Table
        self.create_sidebar_button(
            "Create Table",
            self.show_create_table
        )

        # Spacer
        spacer = tk.Frame(
            self.sidebar,
            bg="#0f172a"
        )

        spacer.pack(
            fill="both",
            expand=True
        )

        # Logout
        self.create_sidebar_button(
            "Logout",
            self.logout
        )

    # =========================================================
    # SIDEBAR BUTTON
    # =========================================================

    def create_sidebar_button(
        self,
        text,
        command
    ):

        button = tk.Button(
            self.sidebar,
            text=text,
            font=("Segoe UI", 11),
            anchor="w",
            padx=25,
            fg="#cbd5e1",
            bg="#0f172a",
            activebackground="#1e293b",
            activeforeground="#38bdf8",
            relief="flat",
            cursor="hand2",
            command=command
        )

        button.pack(
            fill="x",
            ipady=12
        )

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):

        header = tk.Frame(
            self.content,
            bg="white",
            height=75
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="Smart Database Dashboard",
            font=("Segoe UI", 18, "bold"),
            fg="#0f172a",
            bg="white"
        )

        title.pack(
            side="left",
            padx=30
        )

        user_label = tk.Label(
            header,
            text=f"👤 {self.username}",
            font=("Segoe UI", 11),
            fg="#475569",
            bg="white"
        )

        user_label.pack(
            side="right",
            padx=30
        )

    # =========================================================
    # DASHBOARD CONTENT
    # =========================================================

    def create_dashboard_content(self):

        self.dashboard_frame = tk.Frame(
            self.content,
            bg="#f1f5f9"
        )

        self.dashboard_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=30
        )

        # Welcome
        welcome = tk.Label(
            self.dashboard_frame,
            text=f"Welcome, {self.username}!",
            font=("Segoe UI", 24, "bold"),
            fg="#0f172a",
            bg="#f1f5f9"
        )

        welcome.pack(
            anchor="w"
        )

        subtitle = tk.Label(
            self.dashboard_frame,
            text="Manage your Oracle database from one place.",
            font=("Segoe UI", 11),
            fg="#64748b",
            bg="#f1f5f9"
        )

        subtitle.pack(
            anchor="w",
            pady=(5, 30)
        )

        # =====================================================
        # CARDS
        # =====================================================

        self.card_frame = tk.Frame(
            self.dashboard_frame,
            bg="#f1f5f9"
        )

        self.card_frame.pack(
            fill="x"
        )

        # Tables card
        self.table_count_label = self.create_card(
            "Tables",
            "0",
            0
        )

        # Database card
        self.status_label = self.create_card(
            "Database",
            "Connected",
            1
        )

        # AI card
        self.feature_label = self.create_card(
            "AI Assistant",
            "Ready",
            2
        )

        # =====================================================
        # QUICK ACTIONS
        # =====================================================

        actions_title = tk.Label(
            self.dashboard_frame,
            text="Quick Actions",
            font=("Segoe UI", 16, "bold"),
            fg="#0f172a",
            bg="#f1f5f9"
        )

        actions_title.pack(
            anchor="w",
            pady=(40, 15)
        )

        actions_frame = tk.Frame(
            self.dashboard_frame,
            bg="#f1f5f9"
        )

        actions_frame.pack(
            fill="x"
        )

        # Manage Tables
        self.create_action_button(
            actions_frame,
            "📋 Manage Tables",
            self.show_tables
        )

        # SQL Editor
        self.create_action_button(
            actions_frame,
            "⌨ SQL Editor",
            self.show_sql_editor
        )

        # AI Assistant
        self.create_action_button(
            actions_frame,
            "🤖 AI Assistant",
            self.show_ai_assistant
        )

        # Create Table
        self.create_action_button(
            actions_frame,
            "➕ Create Table",
            self.show_create_table
        )

    # =========================================================
    # DASHBOARD CARD
    # =========================================================

    def create_card(
        self,
        title,
        value,
        column
    ):

        card = tk.Frame(
            self.card_frame,
            bg="white",
            width=260,
            height=140
        )

        card.grid(
            row=0,
            column=column,
            padx=(0, 20),
            pady=10
        )

        card.grid_propagate(False)

        title_label = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 10),
            fg="#64748b",
            bg="white"
        )

        title_label.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 22, "bold"),
            fg="#2563eb",
            bg="white"
        )

        value_label.pack(
            anchor="w",
            padx=20
        )

        return value_label

    # =========================================================
    # QUICK ACTION BUTTON
    # =========================================================

    def create_action_button(
        self,
        parent,
        text,
        command
    ):

        button = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 11, "bold"),
            fg="#0f172a",
            bg="white",
            activebackground="#e2e8f0",
            relief="flat",
            cursor="hand2",
            command=command
        )

        button.pack(
            side="left",
            padx=(0, 15),
            ipadx=20,
            ipady=12
        )

    # =========================================================
    # LOAD TABLES
    # =========================================================

    def load_tables(self):

        success, result = get_tables()

        if success:

            self.tables = result

            if hasattr(
                self,
                "table_count_label"
            ):

                self.table_count_label.config(
                    text=str(len(result))
                )

        else:

            self.tables = []

            messagebox.showerror(
                "Database Error",
                str(result),
                parent=self.root
            )

    # =========================================================
    # TABLE PAGE
    # =========================================================

    def show_tables(self):

        self.clear_content()

        title = tk.Label(
            self.content,
            text="Database Tables",
            font=("Segoe UI", 24, "bold"),
            fg="#0f172a",
            bg="#f1f5f9"
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=(30, 5)
        )

        subtitle = tk.Label(
            self.content,
            text="Select a table to view, insert, update or delete records.",
            font=("Segoe UI", 11),
            fg="#64748b",
            bg="#f1f5f9"
        )

        subtitle.pack(
            anchor="w",
            padx=30
        )

        # =====================================================
        # TABLE CONTAINER
        # =====================================================

        table_frame = tk.Frame(
            self.content,
            bg="#f1f5f9"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        self.table_listbox = tk.Listbox(
            table_frame,
            font=("Consolas", 13),
            bg="white",
            fg="#0f172a",
            selectbackground="#2563eb",
            selectforeground="white",
            relief="flat",
            activestyle="none"
        )

        self.table_listbox.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table_listbox.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.table_listbox.config(
            yscrollcommand=scrollbar.set
        )

        # Add tables
        for table in self.tables:

            self.table_listbox.insert(
                "end",
                table
            )

        # Double click
        self.table_listbox.bind(
            "<Double-1>",
            lambda event: self.view_selected_table()
        )

        # =====================================================
        # BUTTONS
        # =====================================================

        button_frame = tk.Frame(
            self.content,
            bg="#f1f5f9"
        )

        button_frame.pack(
            padx=30,
            pady=(0, 30),
            anchor="w"
        )

        view_button = tk.Button(
            button_frame,
            text="VIEW / MANAGE",
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#2563eb",
            activebackground="#1d4ed8",
            relief="flat",
            cursor="hand2",
            command=self.view_selected_table
        )

        view_button.pack(
            side="left",
            ipadx=20,
            ipady=8
        )

        refresh_button = tk.Button(
            button_frame,
            text="↻ REFRESH",
            font=("Segoe UI", 10, "bold"),
            fg="#0f172a",
            bg="white",
            relief="flat",
            cursor="hand2",
            command=self.refresh_tables
        )

        refresh_button.pack(
            side="left",
            padx=10,
            ipadx=20,
            ipady=8
        )

    # =========================================================
    # VIEW / MANAGE SELECTED TABLE
    # =========================================================

    def view_selected_table(self):

        selection = self.table_listbox.curselection()

        if not selection:

            messagebox.showwarning(
                "Select Table",
                "Please select a table first.",
                parent=self.root
            )

            return

        table_name = self.table_listbox.get(
            selection[0]
        )

        TableManager(
            self.root,
            table_name
        )

    # =========================================================
    # SQL EDITOR
    # =========================================================

    def show_sql_editor(self):

        self.clear_content()

        SQLEditor(
            self.content
        )

    # =========================================================
    # AI DATABASE ASSISTANT
    # =========================================================

    def show_ai_assistant(self):

        self.clear_content()

        AIAssistant(
            self.content
        )

    # =========================================================
    # CREATE TABLE
    # =========================================================

    def show_create_table(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Create New Table"
        )

        window.geometry(
            "600x600"
        )

        window.minsize(
            550,
            500
        )

        window.configure(
            bg="#f1f5f9"
        )

        # =====================================================
        # TITLE
        # =====================================================

        title = tk.Label(
            window,
            text="Create New Table",
            font=("Segoe UI", 22, "bold"),
            fg="#0f172a",
            bg="#f1f5f9"
        )

        title.pack(
            pady=25
        )

        # =====================================================
        # TABLE NAME
        # =====================================================

        name_label = tk.Label(
            window,
            text="Table Name",
            font=("Segoe UI", 11, "bold"),
            fg="#334155",
            bg="#f1f5f9"
        )

        name_label.pack(
            anchor="w",
            padx=40
        )

        table_entry = ttk.Entry(
            window,
            font=("Segoe UI", 12)
        )

        table_entry.pack(
            fill="x",
            padx=40,
            pady=(5, 20),
            ipady=6
        )

        # =====================================================
        # INSTRUCTIONS
        # =====================================================

        instruction = tk.Label(
            window,
            text=(
                "Enter columns one per line.\n"
                "Format: COLUMN_NAME DATA_TYPE"
            ),
            font=("Segoe UI", 10),
            fg="#64748b",
            bg="#f1f5f9",
            justify="left"
        )

        instruction.pack(
            anchor="w",
            padx=40
        )

        # =====================================================
        # COLUMNS
        # =====================================================

        columns_text = tk.Text(
            window,
            height=12,
            font=("Consolas", 11)
        )

        columns_text.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=15
        )

        columns_text.insert(
            "1.0",
            "ID NUMBER PRIMARY KEY\n"
            "NAME VARCHAR2(100)\n"
            "EMAIL VARCHAR2(150)"
        )

        # =====================================================
        # CREATE
        # =====================================================

        def create():

            table_name = (
                table_entry
                .get()
                .strip()
                .upper()
            )

            column_lines = (
                columns_text
                .get(
                    "1.0",
                    "end"
                )
                .strip()
                .splitlines()
            )

            if not table_name:

                messagebox.showwarning(
                    "Validation",
                    "Enter a table name.",
                    parent=window
                )

                return

            if not column_lines:

                messagebox.showwarning(
                    "Validation",
                    "Enter at least one column.",
                    parent=window
                )

                return

            columns = {}

            for line in column_lines:

                parts = line.strip().split(
                    None,
                    1
                )

                if len(parts) != 2:

                    messagebox.showerror(
                        "Validation",
                        f"Invalid column definition:\n{line}",
                        parent=window
                    )

                    return

                columns[
                    parts[0].upper()
                ] = parts[1].upper()

            success, message = create_table(
                table_name,
                columns
            )

            if success:

                messagebox.showinfo(
                    "Success",
                    message,
                    parent=window
                )

                window.destroy()

                self.load_tables()

            else:

                messagebox.showerror(
                    "Database Error",
                    message,
                    parent=window
                )

        create_button = tk.Button(
            window,
            text="CREATE TABLE",
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#2563eb",
            activebackground="#1d4ed8",
            relief="flat",
            cursor="hand2",
            command=create
        )

        create_button.pack(
            pady=(0, 25),
            ipadx=30,
            ipady=8
        )

    # =========================================================
    # SHOW DASHBOARD
    # =========================================================

    def show_dashboard(self):

        self.clear_content()

        self.create_header()

        self.create_dashboard_content()

        self.load_tables()

    # =========================================================
    # CLEAR CONTENT
    # =========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():

            widget.destroy()

    # =========================================================
    # REFRESH TABLES
    # =========================================================

    def refresh_tables(self):

        self.load_tables()

        self.show_tables()

    # =========================================================
    # LOGOUT
    # =========================================================

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?",
            parent=self.root
        )

        if answer:

            self.main_frame.destroy()

            self.logout_callback()
