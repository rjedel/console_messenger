import argparse
from psycopg2.errors import UniqueViolation, NoData
from models import User, Message
from clcrypto import check_password, hash_password
from psycopg2 import connect, OperationalError


class WrongPasswordError(Exception):
    def __str__(self):
        return "Incorrect Password!"


user_ = "postgres"
password_ = "coderslab"
host_ = "localhost"
database_ = "messenger"


def connect_to_db():
    try:
        connection = connect(user=user_, password=password_, host=host_, database=database_)
        connection.autocommit = True
        return connection
    except OperationalError as err:
        print(err)
    else:
        connection.close()


cnx = connect_to_db()

if cnx is None:
    print('Cannot connect to database')
    # exit(-1)

cursor = cnx.cursor()

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="list users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")

args = parser.parse_args()


def create_user(username, password, salt=None):
    try:
        if len(password) >= 8:
            new_user = User(username=username, password=password, salt=salt)
            new_user.safe_to_db(cursor)
            print(f'"{username}" user created')
        else:
            raise ValueError
    except UniqueViolation:
        print(f'"{username}" already exists')
    except ValueError:
        print('password must be at least 8 characters long')


def edit_user(username, password, edit, new_pass):
    try:
        edited_user = User.load_user_by_username(cursor, username)
        if edited_user is None:
            raise NoData
        else:
            if check_password(password, edited_user.hashed_password) and edit is True:
                if len(new_pass) >= 8:
                    edited_user.hashed_password = new_pass
                    edited_user.safe_to_db(cursor)
                    print('password has been changed')
                else:
                    raise ValueError
            else:
                raise WrongPasswordError
    except NoData:
        print(f'no user "{username}"')
    except WrongPasswordError as err:
        print(err)
    except ValueError:
        print('password must be at least 8 characters long')


def delete_user(username, password, delete):
    try:
        del_user = User.load_user_by_username(cursor, username)
        if del_user is None:
            raise NoData
        else:
            if check_password(password, del_user.hashed_password) and delete is True:
                del_user.delete(cursor)
                print(f'"{username}" has been deleted')
            else:
                raise WrongPasswordError

    except NoData:
        print(f'no user "{username}"')
    except WrongPasswordError as err:
        print(err)


def user_list(lst):
    if lst is True:
        for usr in User.load_all_users(cursor):
            print(f'id: {usr.id}   username: {usr.username}')


if args.username and args.password and not args.new_pass and not args.list and not args.delete and not args.edit:
    create_user(args.username, args.password)

elif args.username and args.password and args.edit and args.new_pass and not args.list and not args.delete:
    edit_user(args.username, args.password, args.edit, args.new_pass)

elif args.username and args.password and args.delete and not args.new_pass and not args.list and not args.edit:
    delete_user(args.username, args.password, args.delete)

elif args.list and not args.username and not args.password and not args.new_pass and not args.delete and not args.edit:
    user_list(args.list)

else:
    parser.print_help()

# us1 = create_user('user5', 'alamakota', 'salt')
# python3 users.py -u tt -p alamakota
# python3 users.py -u tt -p alamakota -n halohalo -e

cursor.close()
cnx.close()

# print(int(args.username) * 3)
