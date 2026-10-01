from database.connection import get_connection


def get_tables():
    """
    Get all tables owned by the current Oracle user.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT table_name
            FROM user_tables
            ORDER BY table_name
        """

        cursor.execute(query)

        tables = [row[0] for row in cursor.fetchall()]

        return True, tables

    except Exception as error:
        return False, str(error)

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def get_columns(table_name):
    """
    Get column information for a table.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                column_name,
                data_type,
                data_length,
                nullable
            FROM user_tab_columns
            WHERE table_name = :table_name
            ORDER BY column_id
        """

        cursor.execute(
            query,
            {"table_name": table_name.upper()}
        )

        columns = cursor.fetchall()

        return True, columns

    except Exception as error:
        return False, str(error)

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

def create_table(table_name, columns):
    """
    Create a new Oracle table.

    Example:

    columns = {
        "ID": "NUMBER PRIMARY KEY",
        "NAME": "VARCHAR2(100)",
        "AGE": "NUMBER"
    }
    """

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        column_definitions = []

        for column_name, column_type in columns.items():

            column_definitions.append(
                f"{column_name} {column_type}"
            )

        column_string = ", ".join(
            column_definitions
        )

        query = f"""
            CREATE TABLE {table_name}
            (
                {column_string}
            )
        """

        cursor.execute(query)

        connection.commit()

        return True, (
            f"Table '{table_name}' "
            f"created successfully."
        )

    except Exception as error:

        if connection:
            connection.rollback()

        return False, str(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

def get_primary_key(table_name):
    """
    Get the primary key column of a table.
    """

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                cols.column_name
            FROM
                user_constraints cons
                JOIN user_cons_columns cols
                ON cons.constraint_name = cols.constraint_name
            WHERE
                cons.constraint_type = 'P'
                AND cons.table_name = :table_name
            ORDER BY
                cols.position
        """

        cursor.execute(
            query,
            {
                "table_name": table_name.upper()
            }
        )

        result = cursor.fetchone()

        if result:
            return True, result[0]

        return True, None

    except Exception as error:

        return False, str(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()