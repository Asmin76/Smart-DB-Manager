import sys
import os

# Add src folder to Python path
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src")
    )
)

from database.query_history import QueryHistory


print("Testing Query History...")

success = QueryHistory.save_history(
    username="TEST_USER",
    question="Show all students",
    sql_query="SELECT * FROM students",
    status="SUCCESS",
    rows_affected=5
)

print("Save result:", success)


history = QueryHistory.get_history("TEST_USER")

print("\nHistory:")

for row in history:
    print(row)