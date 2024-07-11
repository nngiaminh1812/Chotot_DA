import pandas as pd
import sqlite3

db_path = '/home/nngminh1812/Documents/DA/Chotot_DA/pets_database.db'
conn = sqlite3.connect(db_path)

create_table_sql = """
CREATE TABLE IF NOT EXISTS Preprocessed (
    price REAL,
    description TEXT,
    breed TEXT,
    age TEXT,
    size TEXT,
    address TEXT,
    type TEXT,
    time TEXT
);
"""
cur = conn.cursor()
cur.execute(create_table_sql)

csv_file = '/home/nngminh1812/Documents/DA/Chotot_DA/Preprocessed_Dog.csv'
df = pd.read_csv(csv_file)

df.to_sql('Preprocessed', conn, if_exists = 'replace', index = False)

conn.commit()
conn.close()