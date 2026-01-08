import psycopg2
 
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password="spark@1234"
)
 
cursor = conn.cursor()
# cursor.execute("CREATE TABLE student(id INT, name VARCHAR(50));")
# conn.commit()

cursor.execute("SELECT * FROM student;")
print(cursor.fetchall())

cursor.close()
conn.close()