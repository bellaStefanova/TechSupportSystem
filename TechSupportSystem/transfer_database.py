import sqlite3
import mysql.connector

# SQLite connection parameters
sqlite_db_path = 'db.sqlite3'  # Replace with your SQLite database file path
sqlite_conn = sqlite3.connect(sqlite_db_path)
sqlite_cursor = sqlite_conn.cursor()

# MySQL connection parameters
mysql_conn_params = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Test',
    'database': 'techsupportsystem_db'
}

# Connect to MySQL
mysql_conn = mysql.connector.connect(**mysql_conn_params)
mysql_cursor = mysql_conn.cursor()

# Retrieve SQLite table names
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = sqlite_cursor.fetchall()

# Loop through each table and migrate data to MySQL
for table in tables:
    table_name = table[0]

    # Fetch data from SQLite
    sqlite_cursor.execute(f"SELECT * FROM {table_name};")
    rows = sqlite_cursor.fetchall()

    # Create MySQL table with the same schema
    sqlite_cursor.execute(f"PRAGMA table_info({table_name});")
    columns_info = sqlite_cursor.fetchall()

    create_table_query = f"CREATE TABLE {table_name} ("
    for column_info in columns_info:
        column_name = column_info[1]
        column_type = column_info[2]
        create_table_query += f"{column_name} {column_type}, "
    create_table_query = create_table_query.rstrip(', ')
    create_table_query += ");"

    mysql_cursor.execute(create_table_query)

    # Insert data into MySQL
    for row in rows:
        insert_query = f"INSERT INTO {table_name} VALUES {row};"
        mysql_cursor.execute(insert_query)

# Commit changes and close connections
mysql_conn.commit()
mysql_cursor.close()
mysql_conn.close()
sqlite_cursor.close()
sqlite_conn.close()