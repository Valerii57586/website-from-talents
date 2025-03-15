import sqlite3


def create_table(dbname, table_name: str, columns: tuple) -> None:
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    columns_str = ", ".join([f"{col[0]} {col[1]}" for col in columns])
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")
    connection.commit()


def add_record(table_name: str, values: dict, dbname: str) -> None:
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    columns = ", ".join(values.keys())
    placeholders = ", ".join(["?" for _ in values.keys()])
    cursor.execute(f"INSERT INTO {table_name} ({columns})"
                   f"VALUES ({placeholders})", tuple(values.values()))
    connection.commit()


def exists_in_table(table_name: str, condition: tuple, dbname: str) -> bool:
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    cursor.execute(f"SELECT 1 FROM {table_name} WHERE {condition[0]} = ?",
                   (condition[1],))
    result = cursor.fetchone()
    return result is not None


def get_column_value_by_name(table_name: str, column_to_get: str,
                             condition: tuple, dbname: str):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    cursor.execute(f"SELECT {column_to_get} FROM {table_name} "
                   f"WHERE {condition[0]} = ?", (condition[1],))
    result = cursor.fetchall()
    if len(result) != 0:
        return result
    else:
        return None


def update_column_value(table_name: str, columns_and_values: dict,
                        condition: tuple, dbname: str) -> None:
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    set_string = ', '.join([f"{col} = ?" for col in columns_and_values.keys()])
    values = list(columns_and_values.values())
    values.append(condition[1])
    query = f'UPDATE {table_name} SET {set_string} WHERE {condition[0]} = ?'
    cursor.execute(query, values)
    connection.commit()


def delete_record(table_name: str, condition: tuple, dbname: str):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM {table_name} WHERE {condition[0]} = ?', (condition[1],))
    connection.commit()
