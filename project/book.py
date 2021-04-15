import psycopg2
import csv

# For connecting to the database
conn = psycopg2.connect(
    "host=localhost port=5432 dbname=book user=postgres password=1998")
cur = conn.cursor()

# importing csv file
with open('books.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)

    for row in reader:
        cur.execute("INSERT INTO books VALUES (%s, %s, %s, %s)",
                    row
                    )
        conn.commit()
