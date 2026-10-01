from database.queries import (
    get_table_data,
    insert_record,
    update_record,
    delete_record
)


def print_employee_data():

    success, columns, rows = get_table_data("EMPLOYEE")

    if success:

        print("\nEMPLOYEE DATA")
        print("-" * 70)

        print(columns)

        for row in rows:
            print(row)

    else:

        print("Error:", columns)


def main():

    print("=" * 70)
    print("SMART DB MANAGER - CRUD TEST")
    print("=" * 70)

    # ---------------------------------------
    # 1. SHOW EXISTING DATA
    # ---------------------------------------

    print_employee_data()

    # ---------------------------------------
    # 2. INSERT
    # ---------------------------------------

    print("\nINSERTING NEW EMPLOYEE...")

    employee = {
        "NAME": "Test Employee",
        "EMAIL": "test@example.com",
        "DEPARTMENT": "IT",
        "SALARY": 40000
    }

    success, message = insert_record(
        "EMPLOYEE",
        employee
    )

    print(message)

    # ---------------------------------------
    # 3. SHOW DATA AFTER INSERT
    # ---------------------------------------

    print_employee_data()

    # ---------------------------------------
    # 4. UPDATE
    # ---------------------------------------

    print("\nUPDATING TEST EMPLOYEE...")

    update_data = {
        "SALARY": 50000,
        "DEPARTMENT": "Data Science"
    }

    success, message = update_record(
        "EMPLOYEE",
        update_data,
        "EMAIL",
        "test@example.com"
    )

    print(message)

    # ---------------------------------------
    # 5. SHOW DATA AFTER UPDATE
    # ---------------------------------------

    print_employee_data()

    # ---------------------------------------
    # 6. DELETE
    # ---------------------------------------

    print("\nDELETING TEST EMPLOYEE...")

    success, message = delete_record(
        "EMPLOYEE",
        "EMAIL",
        "test@example.com"
    )

    print(message)

    # ---------------------------------------
    # 7. FINAL DATA
    # ---------------------------------------

    print_employee_data()


if __name__ == "__main__":
    main()