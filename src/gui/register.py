import tkinter as tk
from tkinter import ttk, messagebox

from database.connection import get_connection
from utils.security import hash_password


class RegisterWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)

        self.window.title("Smart DB Manager - Register")

        self.window.geometry("500x500")

        self.window.resizable(False, False)

        self.window.configure(bg="#0f172a")

        self.build_gui()

    def build_gui(self):

        # Main container
        container = tk.Frame(
            self.window,
            bg="#0f172a"
        )

        container.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=30
        )

        # Title
        title = tk.Label(
            container,
            text="Create Account",
            font=("Segoe UI", 26, "bold"),
            fg="#f8fafc",
            bg="#0f172a"
        )

        title.pack(pady=(10, 5))

        subtitle = tk.Label(
            container,
            text="Create your Smart DB Manager account",
            font=("Segoe UI", 11),
            fg="#94a3b8",
            bg="#0f172a"
        )

        subtitle.pack(pady=(0, 30))

        # Username
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
            ipady=7
        )

        # Password
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
            pady=(5, 20),
            ipady=7
        )

        # Confirm password
        confirm_label = tk.Label(
            container,
            text="Confirm Password",
            font=("Segoe UI", 11, "bold"),
            fg="#e2e8f0",
            bg="#0f172a"
        )

        confirm_label.pack(
            anchor="w"
        )

        self.confirm_entry = ttk.Entry(
            container,
            show="*",
            font=("Segoe UI", 12)
        )

        self.confirm_entry.pack(
            fill="x",
            pady=(5, 30),
            ipady=7
        )

        # Register button
        register_button = tk.Button(
            container,
            text="CREATE ACCOUNT",
            font=("Segoe UI", 11, "bold"),
            fg="white",
            bg="#2563eb",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.register
        )

        register_button.pack(
            fill="x",
            ipady=10
        )

    def register(self):

        username = self.username_entry.get().strip()

        password = self.password_entry.get()

        confirm_password = self.confirm_entry.get()

        # Validation
        if not username:

            messagebox.showwarning(
                "Validation",
                "Please enter a username.",
                parent=self.window
            )

            return

        if len(username) < 3:

            messagebox.showwarning(
                "Validation",
                "Username must contain at least 3 characters.",
                parent=self.window
            )

            return

        if not password:

            messagebox.showwarning(
                "Validation",
                "Please enter a password.",
                parent=self.window
            )

            return

        if len(password) < 6:

            messagebox.showwarning(
                "Validation",
                "Password must contain at least 6 characters.",
                parent=self.window
            )

            return

        if password != confirm_password:

            messagebox.showerror(
                "Password Error",
                "Passwords do not match.",
                parent=self.window
            )

            return

        connection = None
        cursor = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            # Check username
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM app_users
                WHERE username = :username
                """,
                {
                    "username": username
                }
            )

            count = cursor.fetchone()[0]

            if count > 0:

                messagebox.showerror(
                    "Registration Error",
                    "Username already exists.",
                    parent=self.window
                )

                return

            # Hash password
            password_hash = hash_password(password)

            # Insert user
            cursor.execute(
                """
                INSERT INTO app_users
                (
                    username,
                    password_hash
                )
                VALUES
                (
                    :username,
                    :password_hash
                )
                """,
                {
                    "username": username,
                    "password_hash": password_hash
                }
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Account created successfully!",
                parent=self.window
            )

            self.window.destroy()

        except Exception as error:

            if connection:
                connection.rollback()

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