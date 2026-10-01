import tkinter as tk
from tkinter import ttk, messagebox

from database.connection import get_connection
from utils.security import verify_password

from gui.register import RegisterWindow
from gui.dashboard import DashboardWindow


class LoginWindow:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Smart DB Manager - Login"
        )

        # Login window size
        self.root.geometry(
            "500x700"
        )

        self.root.resizable(
            False,
            False
        )

        self.root.configure(
            bg="#0f172a"
        )

        self.build_gui()

    # =========================================================
    # LOGIN GUI
    # =========================================================

    def build_gui(self):

        container = tk.Frame(
            self.root,
            bg="#0f172a"
        )

        container.pack(
            fill="both",
            expand=True,
            padx=50,
            pady=30
        )

        # -----------------------------------------------------
        # Logo
        # -----------------------------------------------------

        logo = tk.Label(
            container,
            text="🗄",
            font=("Segoe UI Emoji", 45),
            fg="#38bdf8",
            bg="#0f172a"
        )

        logo.pack(
            pady=(10, 5)
        )

        # -----------------------------------------------------
        # Title
        # -----------------------------------------------------

        title = tk.Label(
            container,
            text="SMART DB MANAGER",
            font=("Segoe UI", 24, "bold"),
            fg="#f8fafc",
            bg="#0f172a"
        )

        title.pack()

        # -----------------------------------------------------
        # Subtitle
        # -----------------------------------------------------

        subtitle = tk.Label(
            container,
            text="Smart Database Management System",
            font=("Segoe UI", 10),
            fg="#94a3b8",
            bg="#0f172a"
        )

        subtitle.pack(
            pady=(5, 35)
        )

        # -----------------------------------------------------
        # Username
        # -----------------------------------------------------

        username_label = tk.Label(
            container,
            text="Username",
            font=("Segoe UI", 11, "bold"),
            fg="#e2e8f0",
            bg="#0f172a"
        )

        username_label.pack(
            anchor="w"
        )

        self.username_entry = ttk.Entry(
            container,
            font=("Segoe UI", 12)
        )

        self.username_entry.pack(
            fill="x",
            pady=(5, 20),
            ipady=8
        )

        # -----------------------------------------------------
        # Password
        # -----------------------------------------------------

        password_label = tk.Label(
            container,
            text="Password",
            font=("Segoe UI", 11, "bold"),
            fg="#e2e8f0",
            bg="#0f172a"
        )

        password_label.pack(
            anchor="w"
        )

        self.password_entry = ttk.Entry(
            container,
            show="*",
            font=("Segoe UI", 12)
        )

        self.password_entry.pack(
            fill="x",
            pady=(5, 25),
            ipady=8
        )

        # -----------------------------------------------------
        # Login Button
        # -----------------------------------------------------

        login_button = tk.Button(
            container,
            text="LOGIN",
            font=("Segoe UI", 11, "bold"),
            fg="white",
            bg="#2563eb",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.login
        )

        login_button.pack(
            fill="x",
            ipady=8
        )

        # -----------------------------------------------------
        # Register Section
        # -----------------------------------------------------

        register_frame = tk.Frame(
            container,
            bg="#0f172a"
        )

        register_frame.pack(
            pady=15
        )

        text = tk.Label(
            register_frame,
            text="Don't have an account?",
            font=("Segoe UI", 10),
            fg="#94a3b8",
            bg="#0f172a"
        )

        text.pack(
            side="left"
        )

        register_button = tk.Button(
            register_frame,
            text="Register",
            font=("Segoe UI", 10, "bold"),
            fg="#38bdf8",
            bg="#0f172a",
            activebackground="#0f172a",
            activeforeground="#7dd3fc",
            relief="flat",
            cursor="hand2",
            command=self.open_register
        )

        register_button.pack(
            side="left",
            padx=5
        )

        # -----------------------------------------------------
        # Enter Key
        # -----------------------------------------------------

        self.root.bind(
            "<Return>",
            lambda event: self.login()
        )

    # =========================================================
    # OPEN REGISTER
    # =========================================================

    def open_register(self):

        RegisterWindow(self.root)

    # =========================================================
    # LOGIN
    # =========================================================

    def login(self):

        username = self.username_entry.get().strip()

        password = self.password_entry.get()

        # -----------------------------------------------------
        # Validation
        # -----------------------------------------------------

        if not username or not password:

            messagebox.showwarning(
                "Login",
                "Please enter username and password.",
                parent=self.root
            )

            return

        connection = None
        cursor = None

        try:

            # -------------------------------------------------
            # Connect to Oracle
            # -------------------------------------------------

            connection = get_connection()

            cursor = connection.cursor()

            # -------------------------------------------------
            # Find User
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT password_hash
                FROM app_users
                WHERE username = :username
                """,
                {
                    "username": username
                }
            )

            result = cursor.fetchone()

            # -------------------------------------------------
            # User Not Found
            # -------------------------------------------------

            if result is None:

                messagebox.showerror(
                    "Login Failed",
                    "Invalid username or password.",
                    parent=self.root
                )

                return

            # -------------------------------------------------
            # Verify Password
            # -------------------------------------------------

            password_hash = result[0]

            if verify_password(
                password,
                password_hash
            ):

                self.open_dashboard(username)

            else:

                messagebox.showerror(
                    "Login Failed",
                    "Invalid username or password.",
                    parent=self.root
                )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error),
                parent=self.root
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # =========================================================
    # OPEN DASHBOARD
    # =========================================================

    def open_dashboard(self, username):

        # -----------------------------------------------------
        # Change window size for dashboard
        # -----------------------------------------------------

        self.root.resizable(
            True,
            True
        )

        self.root.minsize(
            1000,
            650
        )

        # -----------------------------------------------------
        # Center Dashboard
        # -----------------------------------------------------

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        dashboard_width = 1200
        dashboard_height = 750

        x = (
            screen_width - dashboard_width
        ) // 2

        y = (
            screen_height - dashboard_height
        ) // 2

        self.root.geometry(
            f"{dashboard_width}x{dashboard_height}+{x}+{y}"
        )

        # -----------------------------------------------------
        # Remove Login Widgets
        # -----------------------------------------------------

        for widget in self.root.winfo_children():

            widget.destroy()

        # -----------------------------------------------------
        # Open Dashboard
        # -----------------------------------------------------

        DashboardWindow(
            self.root,
            username,
            self.logout
        )

    # =========================================================
    # LOGOUT
    # =========================================================

    def logout(self):

        # -----------------------------------------------------
        # Remove Dashboard Widgets
        # -----------------------------------------------------

        for widget in self.root.winfo_children():

            widget.destroy()

        # -----------------------------------------------------
        # Restore Login Window
        # -----------------------------------------------------

        self.root.resizable(
            False,
            False
        )

        login_width = 500
        login_height = 700

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (
            screen_width - login_width
        ) // 2

        y = (
            screen_height - login_height
        ) // 2

        self.root.geometry(
            f"{login_width}x{login_height}+{x}+{y}"
        )

        self.root.title(
            "Smart DB Manager - Login"
        )

        self.root.configure(
            bg="#0f172a"
        )

        # -----------------------------------------------------
        # Rebuild Login GUI
        # -----------------------------------------------------

        self.build_gui()