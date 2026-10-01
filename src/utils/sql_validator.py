import re


class SQLValidator:

    # =========================================================
    # DANGEROUS COMMANDS
    # =========================================================

    FORBIDDEN_COMMANDS = [
        "DROP DATABASE",
        "DROP USER",
        "SHUTDOWN",
        "STARTUP",
        "ALTER SYSTEM",
        "GRANT",
        "REVOKE"
    ]

    # =========================================================
    # MAIN VALIDATION FUNCTION
    # =========================================================

    @classmethod
    def validate(
        cls,
        sql,
        schema
    ):

        if not sql:

            return False, "SQL query is empty."

        sql = sql.strip()

        # -----------------------------------------------------
        # Remove one final semicolon
        # -----------------------------------------------------

        if sql.endswith(";"):

            sql = sql[:-1].strip()

        if not sql:

            return False, "SQL query is empty."

        # -----------------------------------------------------
        # Check multiple statements
        # -----------------------------------------------------

        if ";" in sql:

            return (
                False,
                "Multiple SQL statements are not allowed."
            )

        # -----------------------------------------------------
        # Remove comments for validation
        # -----------------------------------------------------

        clean_sql = cls.remove_comments(sql)

        if not clean_sql:

            return False, "SQL contains only comments."

        upper_sql = clean_sql.upper().strip()

        # -----------------------------------------------------
        # Check forbidden commands
        # -----------------------------------------------------

        for command in cls.FORBIDDEN_COMMANDS:

            if re.search(
                rf"\b{re.escape(command)}\b",
                upper_sql
            ):

                return (
                    False,
                    f"Blocked command detected: {command}"
                )

        # -----------------------------------------------------
        # Check allowed SQL type
        # -----------------------------------------------------

        allowed = (
            "SELECT",
            "INSERT",
            "UPDATE",
            "DELETE",
            "CREATE"
        )

        if not upper_sql.startswith(allowed):

            return (
                False,
                "Only SELECT, INSERT, UPDATE, DELETE "
                "and CREATE statements are supported."
            )

        # -----------------------------------------------------
        # Validate table names
        # -----------------------------------------------------

        valid, message = cls.validate_tables(
            clean_sql,
            schema
        )

        if not valid:

            return False, message

        # -----------------------------------------------------
        # Validate columns
        # -----------------------------------------------------

        valid, message = cls.validate_columns(
            clean_sql,
            schema
        )

        if not valid:

            return False, message

        return True, "SQL validation successful."

    # =========================================================
    # REMOVE SQL COMMENTS
    # =========================================================

    @staticmethod
    def remove_comments(sql):

        # Remove -- comments
        sql = re.sub(
            r"--.*?(?=\n|$)",
            "",
            sql
        )

        # Remove /* */ comments
        sql = re.sub(
            r"/\*.*?\*/",
            "",
            sql,
            flags=re.DOTALL
        )

        return sql.strip()

    # =========================================================
    # VALIDATE TABLE NAMES
    # =========================================================

    @classmethod
    def validate_tables(
        cls,
        sql,
        schema
    ):

        if not schema:

            return False, "Database schema is empty."

        available_tables = {
            table.upper()
            for table in schema.keys()
        }

        # -----------------------------------------------------
        # FROM table
        # -----------------------------------------------------

        from_matches = re.findall(
            r"\bFROM\s+([A-Za-z_][A-Za-z0-9_$#]*)",
            sql,
            flags=re.IGNORECASE
        )

        # -----------------------------------------------------
        # JOIN table
        # -----------------------------------------------------

        join_matches = re.findall(
            r"\bJOIN\s+([A-Za-z_][A-Za-z0-9_$#]*)",
            sql,
            flags=re.IGNORECASE
        )

        # -----------------------------------------------------
        # INSERT INTO table
        # -----------------------------------------------------

        insert_matches = re.findall(
            r"\bINSERT\s+INTO\s+([A-Za-z_][A-Za-z0-9_$#]*)",
            sql,
            flags=re.IGNORECASE
        )

        # -----------------------------------------------------
        # UPDATE table
        # -----------------------------------------------------

        update_matches = re.findall(
            r"\bUPDATE\s+([A-Za-z_][A-Za-z0-9_$#]*)",
            sql,
            flags=re.IGNORECASE
        )

        # -----------------------------------------------------
        # DELETE FROM table
        # -----------------------------------------------------

        delete_matches = re.findall(
            r"\bDELETE\s+FROM\s+([A-Za-z_][A-Za-z0-9_$#]*)",
            sql,
            flags=re.IGNORECASE
        )

        # -----------------------------------------------------
        # CREATE TABLE
        # -----------------------------------------------------

        create_matches = re.findall(
            r"\bCREATE\s+TABLE\s+([A-Za-z_][A-Za-z0-9_$#]*)",
            sql,
            flags=re.IGNORECASE
        )

        detected_tables = (
            from_matches
            + join_matches
            + insert_matches
            + update_matches
            + delete_matches
        )

        # CREATE TABLE creates a new table,
        # so don't require it to already exist.
        if not detected_tables and create_matches:

            return True, "CREATE TABLE detected."

        if not detected_tables:

            return (
                False,
                "No database table could be detected in the SQL."
            )

        for table in detected_tables:

            if table.upper() not in available_tables:

                return (
                    False,
                    (
                        f"Table '{table}' does not exist "
                        "in the current database schema."
                    )
                )

        return True, "Table validation successful."

    # =========================================================
    # VALIDATE COLUMNS
    # =========================================================

    @classmethod
    def validate_columns(
        cls,
        sql,
        schema
    ):

        # -----------------------------------------------------
        # This validation focuses on obvious AI mistakes.
        # Oracle itself performs the final SQL validation.
        # -----------------------------------------------------

        available_columns = set()

        for columns in schema.values():

            for column in columns:

                # Schema format:
                # NAME (VARCHAR2)
                match = re.match(
                    r"([A-Za-z_][A-Za-z0-9_$#]*)",
                    column
                )

                if match:

                    available_columns.add(
                        match.group(1).upper()
                    )

        # -----------------------------------------------------
        # Extract identifiers from SELECT
        # -----------------------------------------------------

        select_match = re.search(
            r"\bSELECT\s+(.*?)\s+\bFROM\b",
            sql,
            flags=re.IGNORECASE | re.DOTALL
        )

        if select_match:

            select_part = select_match.group(1).strip()

            # SELECT *
            if select_part != "*":

                # Remove DISTINCT
                select_part = re.sub(
                    r"^\s*DISTINCT\s+",
                    "",
                    select_part,
                    flags=re.IGNORECASE
                )

                # Split columns
                selected_columns = cls.split_columns(
                    select_part
                )

                for expression in selected_columns:

                    expression = expression.strip()

                    # Ignore functions such as COUNT(*)
                    function_match = re.match(
                        r"([A-Za-z_][A-Za-z0-9_$#]*)\s*\(",
                        expression
                    )

                    if function_match:

                        continue

                    # Remove aliases
                    expression = re.split(
                        r"\s+AS\s+|\s+",
                        expression,
                        maxsplit=1,
                        flags=re.IGNORECASE
                    )[0]

                    # Remove table alias
                    if "." in expression:

                        expression = expression.split(
                            "."
                        )[-1]

                    # Remove quoted identifiers
                    expression = expression.strip(
                        "\""
                    )

                    # Ignore numbers/functions
                    if not expression:
                        continue

                    if re.match(
                        r"^[0-9]+(\.[0-9]+)?$",
                        expression
                    ):
                        continue

                    if expression.upper() not in available_columns:

                        # SQL expressions are allowed.
                        # Let Oracle perform final validation.
                        if not cls.looks_like_simple_column(
                            expression
                        ):
                            continue

                        return (
                            False,
                            (
                                f"Column '{expression}' "
                                "was not found in the database schema."
                            )
                        )

        return True, "Column validation successful."

    # =========================================================
    # SPLIT COLUMN EXPRESSIONS
    # =========================================================

    @staticmethod
    def split_columns(text):

        result = []
        current = []
        depth = 0

        for char in text:

            if char == "(":
                depth += 1

            elif char == ")":
                depth -= 1

            if char == "," and depth == 0:

                result.append(
                    "".join(current)
                )

                current = []

            else:

                current.append(char)

        if current:

            result.append(
                "".join(current)
            )

        return result

    # =========================================================
    # CHECK SIMPLE COLUMN
    # =========================================================

    @staticmethod
    def looks_like_simple_column(
        value
    ):

        return bool(
            re.match(
                r"^[A-Za-z_][A-Za-z0-9_$#]*$",
                value
            )
        )