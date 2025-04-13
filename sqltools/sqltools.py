import sqlite3
import re
from typing import List


def guard(query: str, allowed_keywords: List[str] = None) -> bool:
    if allowed_keywords is None:
        allowed_keywords = [
            'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'FROM', 'WHERE',
            'JOIN', 'AND', 'OR', 'LIKE', 'IN', 'VALUES', 'SET',
            'ORDER BY', 'GROUP BY', 'LIMIT', 'OFFSET'
        ]

    dangerous_patterns = [
        r';.*--',
        r'(DROP|ALTER|TRUNCATE|CREATE|EXEC(UTE)?)',
        r'UNION.*SELECT',
        r'(OR|AND)\s+[\d\w]+\s*=\s*[\d\w]+',
        r'/\*.*\*/',
        r'WAITFOR\s+DELAY',
        r'BENCHMARK',
        r'LOAD_FILE|INTO\s+(OUT|DUMP)FILE',
    ]

    query_upper = query.upper()

    words_in_query = re.findall(r'\b[A-Z]+\b', query_upper)
    for word in words_in_query:
        if word not in allowed_keywords:
            return False

    for pattern in dangerous_patterns:
        if re.search(pattern, query_upper, re.IGNORECASE | re.DOTALL):
            return False

    if query.count("'") % 2 != 0 or query.count('"') % 2 != 0:
        return False

    return True


def validate_identifier(identifier: str) -> str:
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', identifier):
        raise ValueError(f"Invalid identifier: {identifier}")
    return identifier


def create_table(dbname, table_name: str, columns: tuple) -> None:
    table_name = validate_identifier(table_name)
    safe_columns = [(validate_identifier(col[0]), col[1]) for col in columns]

    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    columns_str = ", ".join([f"{col[0]} {col[1]}" for col in safe_columns])
    query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"

    if guard(query):
        cursor.execute(query)
        connection.commit()
    else:
        raise ValueError("Potentially dangerous SQL query")
    connection.close()


def add_record(table_name: str, values: dict, dbname: str) -> None:
    table_name = validate_identifier(table_name)
    safe_columns = [validate_identifier(col) for col in values.keys()]

    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    columns = ", ".join(safe_columns)
    placeholders = ", ".join(["?" for _ in values])
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    if guard(query):
        cursor.execute(query, tuple(values.values()))
        connection.commit()
    else:
        raise ValueError("Potentially dangerous SQL query")
    connection.close()


def exists_in_table(table_name: str, condition: tuple, dbname: str) -> bool:
    table_name = validate_identifier(table_name)
    column = validate_identifier(condition[0])

    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    query = f"SELECT 1 FROM {table_name} WHERE {column} = ?"

    if guard(query):
        cursor.execute(query, (condition[1],))
        result = cursor.fetchone()
        connection.close()
        return result is not None
    else:
        connection.close()
        raise ValueError("Potentially dangerous SQL query")


def get_column_value_by_name(table_name: str, column_to_get: str,
                           condition: tuple, dbname: str):
    table_name = validate_identifier(table_name)
    column_to_get = ", ".join([validate_identifier(col.strip())
                             for col in column_to_get.split(",")])
    column = validate_identifier(condition[0])

    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    query = f"SELECT {column_to_get} FROM {table_name} WHERE {column} = ?"

    if guard(query):
        cursor.execute(query, (condition[1],))
        result = cursor.fetchall()
        connection.close()
        return result if result else None
    else:
        connection.close()
        raise ValueError("Potentially dangerous SQL query")


def update_column_value(table_name: str, columns_and_values: dict,
                      condition: tuple, dbname: str) -> None:
    table_name = validate_identifier(table_name)
    safe_columns = {validate_identifier(k): v for k, v in columns_and_values.items()}
    column = validate_identifier(condition[0])

    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    set_string = ', '.join([f"{col} = ?" for col in safe_columns])
    query = f'UPDATE {table_name} SET {set_string} WHERE {column} = ?'

    if guard(query):
        values = list(safe_columns.values())
        values.append(condition[1])
        cursor.execute(query, values)
        connection.commit()
    else:
        raise ValueError("Potentially dangerous SQL query")
    connection.close()


def delete_record(table_name: str, condition: tuple, dbname: str):
    table_name = validate_identifier(table_name)
    column = validate_identifier(condition[0])

    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    query = f'DELETE FROM {table_name} WHERE {column} = ?'

    if guard(query):
        cursor.execute(query, (condition[1],))
        connection.commit()
    else:
        raise ValueError("Potentially dangerous SQL query")
    connection.close()
