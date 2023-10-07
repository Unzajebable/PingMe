from psycopg2 import connect, OperationalError, errorcodes, errors


def create_db():
    connection = connect(host='localhost', user='postgres', password='2121', database='test')
    connection.autocommit = True
    cursor = connection.cursor()

    create_all = True
    sql1 = 'CREATE DATABASE ping_me_db;'

    try:
        cursor.execute(sql1)
    except Exception as err:
        create_all = False
        print('FYI:', err)
        #print("Exception type:", type(err))

    if create_all:
        cursor.close()
        connection.close() #connection closed so we need another autocommit = true
        connection = connect(host='localhost', user='postgres', password='2121', database='ping_me_db')
        connection.autocommit = True

        cursor = connection.cursor()
        sql2 = """CREATE TABLE users(
        id serial PRIMARY KEY,
        username varchar(32),
        hashed_password varchar(80));"""
        cursor.execute(sql2)
        cursor.close()

        cursor = connection.cursor()
        sql3 = """CREATE TABLE messages(
        id serial PRIMARY KEY,
        from_id int NOT NULL REFERENCES users(id),
        to_id int NOT NULL REFERENCES users(id),
        created_date timestamp default current_timestamp,
        message text);"""
        cursor.execute(sql3)

    cursor.close()
    connection.close()
    print("database and tables created and fully operational")

