import os
import oracledb
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    user = os.getenv("ORACLE_USER")
    password = os.getenv("ORACLE_PASSWORD")
    host = os.getenv("ORACLE_HOST")
    port = os.getenv("ORACLE_PORT")
    service_name = os.getenv("ORACLE_SERVICE_NAME")

    dsn = oracledb.makedsn(
        host,
        int(port),
        service_name=service_name
    )

    connection = oracledb.connect(
        user=user,
        password=password,
        dsn=dsn
    )

    return connection