from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

create_db_messenger = "CREATE DATABASE messenger;"

create_tbl_users = """CREATE TABLE users (
    id serial,
    username varchar(255) UNIQUE,
    hashed_password varchar(80),
    PRIMARY KEY (id)
);"""

create_tbl_messages = """CREATE TABLE messages (
    id serial,
    from_id int,
    to_id int,
    text text,
    creation_date timestamp DEFAULT now(),
    PRIMARY KEY (id),
    FOREIGN KEY (from_id) REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (to_id) REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE
);"""

user_ = "postgres"
password_ = "coderslab"
host_ = "localhost"
database_ = "messenger"
try:
    cnx = connect(user=user_, password=password_, host=host_)
    cnx.autocommit = True
    cursor = cnx.cursor()
    try:
        cursor.execute(create_db_messenger)
        print('"messenger" database has been created')
    except DuplicateDatabase as err:
        print(err)
except OperationalError as err:
    print('connection Error:', err)
else:
    cursor.close()
    cnx.close()

try:
    cnx = connect(user=user_, password=password_, host=host_, database=database_)
    cnx.autocommit = True
    cursor = cnx.cursor()

    try:
        cursor.execute(create_tbl_users)
        print('"users" table has been created')
    except DuplicateTable:
        print('table "users" already exists')

    try:
        cursor.execute(create_tbl_messages)
        print('"messages" table has been created')
    except DuplicateTable:
        print('table "messages" already exists')
except OperationalError as err:
    print('connection Error:', err)
else:
    cursor.close()
    cnx.close()
