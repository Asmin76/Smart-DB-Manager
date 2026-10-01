import json
import re
import urllib.request
import urllib.error


class OllamaAI:

    def __init__(
        self,
        model="mistral:latest",
        host="http://localhost:11434"
    ):

        self.model = model
        self.host = host.rstrip("/")

    # =========================================================
    # CHECK OLLAMA
    # =========================================================

    def check_connection(self):

        try:

            url = f"{self.host}/api/tags"

            request = urllib.request.Request(
                url,
                method="GET"
            )

            with urllib.request.urlopen(
                request,
                timeout=10
            ) as response:

                return response.status == 200

        except Exception:

            return False

    # =========================================================
    # SEND PROMPT TO OLLAMA
    # =========================================================

    def ask(self, prompt):

        url = f"{self.host}/api/generate"

        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        json_data = json.dumps(data).encode("utf-8")

        request = urllib.request.Request(
            url,
            data=json_data,
            headers={
                "Content-Type": "application/json"
            },
            method="POST"
        )

        try:

            with urllib.request.urlopen(
                request,
                timeout=120
            ) as response:

                result = json.loads(
                    response.read().decode("utf-8")
                )

                return True, result.get(
                    "response",
                    ""
                )

        except urllib.error.URLError as e:

            return False, (
                "Unable to connect to Ollama.\n\n"
                "Make sure Ollama is running.\n\n"
                f"Error: {e}"
            )

        except Exception as e:

            return False, str(e)

    # =========================================================
    # GENERATE SQL
    # =========================================================

    def generate_sql(
        self,
        question,
        schema
    ):

        schema_text = self.format_schema(
            schema
        )

        prompt = f"""
You are an Oracle Database SQL assistant.

Your task is to convert the user's natural-language
database question into ONE valid Oracle SQL statement.

DATABASE SCHEMA:
{schema_text}

USER QUESTION:
{question}

IMPORTANT RULES:

1. Use ONLY tables and columns provided in the schema.
2. Do not invent table names.
3. Do not invent column names.
4. Generate Oracle-compatible SQL.
5. Return ONLY the SQL statement.
6. Do not use markdown code fences.
7. Do not explain the SQL.
8. Do not include comments.
9. Do not use DROP DATABASE.
10. Do not use TRUNCATE DATABASE.
11. For SELECT questions, generate SELECT SQL.
12. For INSERT questions, generate INSERT SQL.
13. For UPDATE questions, generate UPDATE SQL.
14. For DELETE questions, generate DELETE SQL.
15. If the request cannot be answered using the provided schema,
    return:
    CANNOT_GENERATE_SQL

Generate the SQL now.
"""

        success, response = self.ask(prompt)

        if not success:

            return False, response

        sql = self.clean_sql(response)

        if not sql:

            return False, "AI returned an empty SQL statement."

        if sql.upper() == "CANNOT_GENERATE_SQL":

            return False, (
                "The AI could not generate SQL using "
                "the available database schema."
            )

        return True, sql

    # =========================================================
    # FORMAT DATABASE SCHEMA
    # =========================================================

    def format_schema(self, schema):

        if not schema:

            return "No tables were found."

        lines = []

        for table_name, columns in schema.items():

            lines.append(
                f"TABLE: {table_name}"
            )

            for column in columns:

                lines.append(
                    f"  - {column}"
                )

            lines.append("")

        return "\n".join(lines)

    # =========================================================
    # CLEAN AI RESPONSE
    # =========================================================

    def clean_sql(self, response):

        if not response:

            return ""

        sql = response.strip()

        # Remove markdown code fences
        sql = re.sub(
            r"```(?:sql)?",
            "",
            sql,
            flags=re.IGNORECASE
        )

        sql = sql.replace(
            "```",
            ""
        )

        sql = sql.strip()

        # Remove common AI prefixes
        prefixes = [
            "SQL:",
            "QUERY:",
            "ORACLE SQL:",
            "HERE IS THE SQL:",
            "HERE'S THE SQL:"
        ]

        for prefix in prefixes:

            if sql.upper().startswith(prefix):

                sql = sql[
                    len(prefix):
                ].strip()

        # Find SQL beginning
        match = re.search(
            r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE)\b",
            sql,
            flags=re.IGNORECASE
        )

        if match:

            sql = sql[
                match.start():
            ]

        # Remove explanation after semicolon
        if ";" in sql:

            sql = sql.split(
                ";",
                1
            )[0] + ";"

        return sql.strip()