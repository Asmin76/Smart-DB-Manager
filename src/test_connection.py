print("TEST FILE IS RUNNING")
from database.connection import get_connection


def main():
    try:
        connection = get_connection()

        print("Oracle database connected successfully!")

        cursor = connection.cursor()

        cursor.execute("SELECT SYSDATE FROM dual")

        result = cursor.fetchone()

        print("Oracle server date:", result[0])

        cursor.close()
        connection.close()

    except Exception as error:
        print("Database connection failed!")
        print("Error:", error)


if __name__ == "__main__":
    main()