# SQLtools RU
Данный файл предоставляет удобные функции для работы с базой данных SQLite в Python. Ниже приведено описание каждой функции:

create_table(table_name, columns)
 - Создает таблицу с указанным именем и столбцами. Принимает два параметра: table_name - имя таблицы, и columns - список кортежей, где каждый кортеж содержит имя столбца и тип столбца.


add_record(table_name, values)
 - Добавляет запись в указанную таблицу. Принимает два параметра: table_name - имя таблицы, и values - словарь, где ключи - это имена столбцов, а значения - соответствующие значения.


exists_in_table(table_name, condition)
 - Проверяет, существует ли запись в указанной таблице на основе заданного условия. Принимает два параметра: table_name - имя таблицы, и condition - кортеж, где первый элемент - это имя столбца, а второй элемент - значение для проверки. Возвращает True, если запись существует, иначе False.


get_column_value_by_name(table_name, column_to_get, condition)
 - Получает значение определенного столбца в таблице на основе условия. Принимает три параметра: table_name - имя таблицы, column_to_get - имя столбца для извлечения, и condition - кортеж, где первый элемент - это имя столбца, а второй элемент - значение для проверки. Возвращает значение указанного столбца или None, если не найдено.


update_column_value(table_name, column_to_update, new_value, condition)
 - Обновляет значение определенного столбца в таблице на основе условия. Принимает четыре параметра: table_name - имя таблицы, column_to_update - имя столбца для обновления, new_value - новое значение для установки, и condition - кортеж, где первый элемент - это имя столбца, а второй элемент - значение для проверки.

Пример использования этих функций:
import sqlite3

connection = sqlite3.connect("BeaverTG.db")
cursor = connection.cursor()

 - Создание таблицы
create_table("my_table", [("id", "INTEGER"), ("name", "TEXT"), ("age", "INTEGER")])

 - Добавление записи
add_record("my_table", {"id": 1, "name": "John", "age": 25})

 - Проверка существования записи 
exists = exists_in_table("my_table", ("id", 1))
print(exists)  # Выводит True

 - Получение значения столбца
name = get_column_value_by_name("my_table", "name", ("id", 1))
print(name)  # Выводит "John"

 - Обновление значения столбца
update_column_value("my_table", "age", 30, ("id", 1))
Пожалуйста, обратите внимание, что перед использованием этих функций необходимо установить библиотеку SQLite3.

# SQLtools
This file provides convenient functions for working with the SQLite database in Python. Below is a description of each function:

**create_table(table_name, columns)**
- Creates a table with the specified name and columns.
- Parameters: `table_name` - the name of the table, and `columns` - a list of tuples, where each tuple contains the column name and column type.

**add_record(table_name, values)**
- Adds a record to the specified table.
- Parameters: `table_name` - the name of the table, and `values` - a dictionary where the keys are column names and the values are the corresponding values.

**exists_in_table(table_name, condition)**
- Checks if a record exists in the specified table based on the given condition.
- Parameters: `table_name` - the name of the table, and `condition` - a tuple where the first element is the column name and the second element is the value to check.
- Returns True if the record exists, otherwise False.

**get_column_value_by_name(table_name, column_to_get, condition)**
- Retrieves the value of a specific column in the table based on the condition.
- Parameters: `table_name` - the name of the table, `column_to_get` - the name of the column to retrieve, and `condition` - a tuple where the first element is the column name and the second element is the value to check.
- Returns the value of the specified column or None if not found.

**update_column_value(table_name, column_to_update, new_value, condition)**
- Updates the value of a specific column in the table based on the condition.
- Parameters: `table_name` - the name of the table, `column_to_update` - the name of the column to update, `new_value` - the new value to set, and `condition` - a tuple where the first element is the column name and the second element is the value to check.

Here's an example of how to use these functions:

```python
import sqlite3

connection = sqlite3.connect("BeaverTG.db")
cursor = connection.cursor()

# Creating a table
create_table("my_table", [("id", "INTEGER"), ("name", "TEXT"), ("age", "INTEGER")])

# Adding a record
add_record("my_table", {"id": 1, "name": "John", "age": 25})

# Checking if a record exists
exists = exists_in_table("my_table", ("id", 1))
print(exists)  # Outputs True

# Getting the value of a column
name = get_column_value_by_name("my_table", "name", ("id", 1))
print(name)  # Outputs "John"

# Updating the value of a column
update_column_value("my_table", "age", 30, ("id", 1))
```

Please note that before using these functions, you need to install the SQLite3 library.
