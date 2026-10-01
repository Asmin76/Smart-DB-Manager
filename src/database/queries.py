from database.connection import get_connection


def execute_query(query, params=None):
    """
    Execute INSERT, UPDATE, DELETE, CREATE TABLE,
    or other non-SELECT SQL statements.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        connection.commit()

        return True, "Query executed successfully."

    except Exception as error:

        if connection:
            connection.rollback()

        return False, str(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def fetch_all(query, params=None):
    """
    Execute a SELECT query and return all records.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        rows = cursor.fetchall()

        columns = [
            column[0]
            for column in cursor.description
        ]

        return True, columns, rows

    except Exception as error:

        return False, [], str(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def fetch_one(query, params=None):
    """
    Execute SELECT and return one record.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        row = cursor.fetchone()

        columns = [
            column[0]
            for column in cursor.description
        ]

        return True, columns, row

    except Exception as error:

        return False, [], str(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def insert_record(table_name, data):
    """
    Insert a record into a table.

    Example:

    data = {
        "NAME": "John",
        "EMAIL": "john@example.com",
        "BRANCH": "IT",
        "MARKS": 85
    }
    """

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        columns = list(data.keys())

        column_string = ", ".join(columns)

        placeholders = ", ".join(
            f":{i + 1}"
            for i in range(len(columns))
        )

        query = f"""
            INSERT INTO {table_name}
            ({column_string})
            VALUES ({placeholders})
        """

        values = list(data.values())

        cursor.execute(query, values)

        connection.commit()

        return True, "Record inserted successfully."

    except Exception as error:

        if connection:
            connection.rollback()

        return False, str(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def update_record(
    table_name,
    update_data,
    where_column,
    where_value
):
    """
    Update records.

    Example:

    update_data = {
        "SALARY": 60000,
        "DEPARTMENT": "IT"
    }
    """

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        set_parts = []

        values = []

        for column, value in update_data.items():

            set_parts.append(
                f"{column} = :{len(values) + 1}"
            )

            values.append(value)

        where_placeholder = len(values) + 1

        values.append(where_value)

        set_clause = ", ".join(set_parts)

        query = f"""
            UPDATE {table_name}
            SET {set_clause}
            WHERE {where_column} = :{where_placeholder}
        """

        cursor.execute(query, values)

        affected_rows = cursor.rowcount

        connection.commit()

        return (
            True,
            f"{affected_rows} record(s) updated successfully."
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


def delete_record(
    table_name,
    where_column,
    where_value
):
    """
    Delete records using a WHERE condition.
    """

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        query = f"""
            DELETE FROM {table_name}
            WHERE {where_column} = :1
        """

        cursor.execute(
            query,
            [where_value]
        )

        affected_rows = cursor.rowcount

        connection.commit()

        return (
            True,
            f"{affected_rows} record(s) deleted successfully."
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


def get_table_data(table_name):
    """
    Fetch all records from a table.
    """

    query = f"""
        SELECT *
        FROM {table_name}
    """

    return fetch_all(query)