import argparse

from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation, NoData

from clcrypto import check_password
from models import User

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="user list", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")

args = parser.parse_args()


class IncorrectPasswordError(Exception):
    def __str__(self):
        return "Incorrect Password!"


class TooShortPasswordError(Exception):
    def __str__(self):
        return "use 8 characters or more for your password"


def create_user(cur, username, password):
    try:
        if len(password) >= 8:
            new_user = User(username=username, password=password)
            new_user.safe_to_db(cur)
            print(f'"{username}" user created')
        else:
            raise TooShortPasswordError
    except UniqueViolation as e:
        print(f'"{username}" already exists. {e}')
    except TooShortPasswordError as er:
        print(er)


def edit_user(cur, username, password, edit, new_pass):
    try:
        edited_user = User.load_user_by_username(cur, username)
        if edited_user is None:
            raise NoData
        else:
            if check_password(password, edited_user.hashed_password) and edit is True:
                if len(new_pass) >= 8:
                    edited_user.hashed_password = new_pass
                    edited_user.safe_to_db(cur)
                    print('password has been changed')
                else:
                    raise TooShortPasswordError
            else:
                raise IncorrectPasswordError
    except NoData:
        print(f'no user "{username}"')
    except IncorrectPasswordError as e:
        print(e)
    except TooShortPasswordError as er:
        print(er)


def delete_user(cur, username, password, delete):
    try:
        del_user = User.load_user_by_username(cur, username)
        if del_user is None:
            raise NoData
        else:
            if check_password(password, del_user.hashed_password) and delete is True:
                del_user.delete(cur)
                print(f'"{username}" has been deleted')
            else:
                raise IncorrectPasswordError
    except NoData:
        print(f'no user "{username}"')
    except IncorrectPasswordError as e:
        print(e)


def user_list(cur, lst):
    if lst is True:
        users = User.load_all_users(cur)
        if len(users) == 0:
            print("no users")
        else:
            for usr in users:
                print(f'id: {usr.id}   username: {usr.username}')


if __name__ == '__main__':

    user_ = "postgres"
    password_ = "coderslab"
    host_ = "localhost"
    database_ = "messenger"

    try:
        cnx = connect(user=user_, password=password_, host=host_, database=database_)
        cnx.autocommit = True

        cursor = cnx.cursor()

        if args.username and args.password \
                and not args.new_pass and not args.list and not args.delete and not args.edit:
            create_user(cursor, args.username, args.password)

        elif args.username and args.password and args.edit and args.new_pass \
                and not args.list and not args.delete:
            edit_user(cursor, args.username, args.password, args.edit, args.new_pass)

        elif args.username and args.password and args.delete \
                and not args.new_pass and not args.list and not args.edit:
            delete_user(cursor, args.username, args.password, args.delete)

        elif args.list \
                and not args.username and not args.password and not args.new_pass and not args.delete and not args.edit:
            user_list(cursor, args.list)
        else:
            parser.print_help()

    except OperationalError as e:
        print("Connection Error: ", e)
    else:
        cursor.close()
        cnx.close()

test = """"
python3 users.py
python3 users.py -l
python3 users.py -p nicepass -u Joe
python3 users.py -p ni -u Joe
python3 users.py -p nicepassword -u Joe
python3 users.py -p nicepassw -u Ann
python3 users.py -p nicepassw -u Mary
python3 users.py -l
python3 users.py -u Joe -p wrongpass -n new_pass -e
python3 users.py -u WrongUser -p somepassword -n new_pass -e
python3 users.py -u Joe -p nicepass -n new#passwd -e
python3 users.py -u Mary -p wrongpass -d
python3 users.py -u Mary -p nicepassw -d
python3 users.py -l
"""