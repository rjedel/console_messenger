import argparse
from models import User, Message

from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation, NoData

from clcrypto import check_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-t", "--to", help="recipient")
parser.add_argument("-s", "--send", help="message content")
parser.add_argument("-l", "--list", help="messages list", action="store_true")

args = parser.parse_args()


class IncorrectPasswordError(Exception):
    def __str__(self):
        return "Incorrect Password!"


# class TooShortPasswordError(Exception):
#     def __str__(self):
#         return "use 8 characters or more for your password"

def messages_list(cur, lst, username, password):
    if lst is True:
        try:
            user = User.load_user_by_username(cur, username)
            if user is None:
                raise NoData
            else:
                if check_password(password, user.hashed_password):
                    messages = Message.load_all_messages(cur, user.id)
                    if len(messages) == 0:
                        print("no messages")
                    else:
                        for msg in messages:
                            print(
                                f'message to: {User.load_user_by_id(cursor, msg.to_id).username}\nsent on: {msg.creation_date:%y-%m-%d %H:%M:%S}\ncontent: {msg.text}\n')
                else:
                    raise IncorrectPasswordError
        except NoData:
            print(f'no user "{username}"')
        except IncorrectPasswordError as e:
            print(e)


def send_message(cur, username, password, to, send):
    try:
        user = User.load_user_by_username(cur, username)
        if user is None:
            print(f'no user "{username}"')
        else:
            if check_password(password, user.hashed_password):
                recipient = User.load_user_by_username(cur, to)
                if recipient is None:
                    print(f'no user "{to}"')
                else:
                    msg = Message(user.id, recipient.id, send)
                    msg.safe_to_db(cur)
                    print('message was sent')
            else:
                raise IncorrectPasswordError
    except IncorrectPasswordError as e:
        print(e)


if __name__ == '__main__':

    user_ = "postgres"
    password_ = "coderslab"
    host_ = "localhost"
    database_ = "messenger"

    try:
        cnx = connect(user=user_, password=password_, host=host_, database=database_)
        cnx.autocommit = True

        cursor = cnx.cursor()

        if args.username and args.password and not args.to and not args.send and args.list:
            messages_list(cursor, args.list, args.username, args.password)

        elif args.username and args.password and args.to and args.send and not args.list:
            send_message(cursor, args.username, args.password, args.to, args.send)

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


python3 messages.py -l -u Joe -p new#passwd
python3 messages.py -l -u Ann -p nicepassw

python3 messages.py -u Ann -p nicepassw -t Joe -s "from ann to joe"
python3 messages.py -u Ann -p nicepassw -t Joe -s "Hello Joe"
python3 messages.py -u Ann -p nicepassw -t Joe -s "How are Y?"

python3 messages.py -u Joe -p new#passwd -t Wronuser -s "from joe to ann"
python3 messages.py -u Joe -p new#passwd -t Ann -s "from joe to ann"

"""
