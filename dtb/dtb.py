from psycopg2 import Error
import psycopg2.extras

try:
    connection = psycopg2.connect(user="postgres",
                                  password="g,adfgi9hm",
                                  host="localhost",
                                  port="5432",
                                  database="postgres")
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM main")
    record = cursor.fetchone()
    print("You are connected to base")

except (Exception, Error) as error:
    raise TypeError("Error while connecting to PostgreSQL", error)

