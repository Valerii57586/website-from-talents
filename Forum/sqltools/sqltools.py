import sqlite3


def create_table(dbname, table_name: str, columns: tuple) -> None:
    """
    Creates a table with the specified name and columns.

    table_name: Table name\n
    columns: A list of tuples, where each tuple contains (column name,
    column type)
    """
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    columns_str = ", ".join([f"{col[0]} {col[1]}" for col in columns])
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")
    connection.commit()


def add_record(table_name: str, values: dict, dbname: str) -> None:
    """
    Adds an entry to the specified table.

    table_name: Table name\n
    values: A dictionary where the keys are the column names and the values are
    the corresponding values
    """
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    columns = ", ".join(values.keys())
    placeholders = ", ".join(["?" for _ in values.keys()])
    cursor.execute(f"INSERT INTO {table_name} ({columns})"
                   f"VALUES ({placeholders})", tuple(values.values()))
    connection.commit()


def exists_in_table(table_name: str, condition: tuple, dbname: str) -> bool:
    """
    Checks whether an entry exists in the specified table based on the
    specified
    conditions.

    table_name: Table name\n
    condition: A tuple where the first element is the column name and the
    second one is
    the element is the value to check \n
    True if the record exists, otherwise False
    """
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    cursor.execute(f"SELECT 1 FROM {table_name} WHERE {condition[0]} = ?",
                   (condition[1],))
    result = cursor.fetchone()
    return result is not None


def get_column_value_by_name(table_name: str, column_to_get: str,
                             condition: tuple, dbname: str) -> None:
    """
    Retrieves the value of a specific column in the table based on a condition.

    table_name: Table name \n
    column_to_get: The name of the column to extract\n
    condition: A tuple where the first element is the column name and the
    second one is
    the element is the value to check \n
    The value of the specified column, or None if not found
    """
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    cursor.execute(f"SELECT {column_to_get} FROM {table_name}"
                   f"WHERE {condition[0]} = ?", (condition[1],))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None


def update_column_value(table_name: str, column_to_update: str,
                        new_value,
                        condition: tuple, dbname: str) -> None:
    """
    Updates the value of a specific column in the table based on a condition.

    table_name: Table name \n
    column_to_update: Column name to update\n
    new_value: New value to set\n
    condition: Tuple where the first element is the column name and the second
    one is
    the value element to check
    """
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    cursor.execute(f'UPDATE {table_name} SET {column_to_update} = ?'
                   f'WHERE {condition[0]} = ?',
                   (new_value, condition[1]))
    connection.commit()
