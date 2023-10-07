from psycopg2 import connect
#from psycopg2.extras import RealDictCursor


def create_db():
    connection = connect(host='localhost', user='postgres', password='2121', database='test')
    #cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor = connection.cursor()

    sql1 = 'CREATE DATABASE PingMe_db;'

    cursor.execute(sql1)

    cursor.close()
    connection.close()

