from database.schema import create_table


def main():

    columns = {
        "PRODUCT_ID": "NUMBER PRIMARY KEY",
        "PRODUCT_NAME": "VARCHAR2(100)",
        "PRICE": "NUMBER(10,2)",
        "CATEGORY": "VARCHAR2(100)"
    }

    success, message = create_table(
        "PRODUCTS",
        columns
    )

    print(message)


if __name__ == "__main__":
    main()