from database.connection import get_connection


class QueryHistory:

    @staticmethod
    def save_history(
        username,
        question,
        sql_query,
        status,
        rows_affected=0
    ):
        """Save a query execution record into QUERY_HISTORY."""

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
                INSERT INTO QUERY_HISTORY
                (
                    USERNAME,
                    QUESTION,
                    SQL_QUERY,
                    STATUS,
                    ROWS_AFFECTED
                )
                VALUES
                (
                    :username,
                    :question,
                    :sql_query,
                    :status,
                    :rows_affected
                )
            """

            cursor.execute(
                query,
                {
                    "username": username,
                    "question": question,
                    "sql_query": sql_query,
                    "status": status,
                    "rows_affected": rows_affected
                }
            )

            connection.commit()

            return True

        except Exception as e:
            print("Error saving query history:", e)
            return False

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    @staticmethod
    def get_history(username=None):
        """Get query history."""

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            if username:
                query = """
                    SELECT
                        HISTORY_ID,
                        USERNAME,
                        QUESTION,
                        SQL_QUERY,
                        STATUS,
                        ROWS_AFFECTED,
                        CREATED_AT
                    FROM QUERY_HISTORY
                    WHERE USERNAME = :username
                    ORDER BY CREATED_AT DESC
                """

                cursor.execute(query, {"username": username})

            else:
                query = """
                    SELECT
                        HISTORY_ID,
                        USERNAME,
                        QUESTION,
                        SQL_QUERY,
                        STATUS,
                        ROWS_AFFECTED,
                        CREATED_AT
                    FROM QUERY_HISTORY
                    ORDER BY CREATED_AT DESC
                """

                cursor.execute(query)

            return cursor.fetchall()

        except Exception as e:
            print("Error loading query history:", e)
            return []

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    @staticmethod
    def delete_history(history_id):
        """Delete one history record."""

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM QUERY_HISTORY
                WHERE HISTORY_ID = :history_id
                """,
                {"history_id": history_id}
            )

            connection.commit()

            return True

        except Exception as e:
            print("Error deleting history:", e)
            return False

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    @staticmethod
    def clear_history(username=None):
        """Delete all history."""

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            if username:
                cursor.execute(
                    """
                    DELETE FROM QUERY_HISTORY
                    WHERE USERNAME = :username
                    """,
                    {"username": username}
                )
            else:
                cursor.execute(
                    """
                    DELETE FROM QUERY_HISTORY
                    """
                )

            connection.commit()

            return True

        except Exception as e:
            print("Error clearing history:", e)
            return False

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()