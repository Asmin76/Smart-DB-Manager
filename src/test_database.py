from database.schema import get_tables, get_columns


def main():

    print("=" * 60)
    print("SMART DB MANAGER - SCHEMA TEST")
    print("=" * 60)

    success, tables = get_tables()

    if not success:
        print("Error:", tables)
        return

    print("\nDATABASE TABLES")
    print("-" * 60)

    for table in tables:

        print(f"\nTABLE: {table}")

        success, columns = get_columns(table)

        if success:

            for column in columns:

                column_name = column[0]
                data_type = column[1]
                length = column[2]
                nullable = column[3]

                print(
                    f"   {column_name:<20}"
                    f"{data_type:<15}"
                    f"Length: {str(length):<8}"
                    f"Nullable: {nullable}"
                )

        else:

            print("   Error:", columns)


if __name__ == "__main__":
    main()