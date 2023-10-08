import argparse
from create_db import create_db
from psycopg2 import connect, OperationalError
from module import User, Message
from clcrypto import check_password
from user_handling import login_or_new_user


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-t", "--to", help="addressee username")
parser.add_argument("-s", "--send", help="message content")
parser.add_argument("-l", "--list", help="show all messages", action="store_true")

args = parser.parse_args()


def list_messages(username, password, cursor):
    if login_or_new_user(username, password, cursor):
        curr_user = User.load_user_by_username(cursor, username)
        if curr_user:
            Message.show_all_my_messages(curr_user.id, cursor)
        else:
            print("User not found")
    else:
        print("Failed to log in, check your credentials")


def send_message(username, target, message, cursor):
    curr_user = User.load_user_by_username(cursor, username)
    target_user = User.load_user_by_username(cursor, target)
    if target_user:
        new_msg = Message(curr_user.id, target_user.id, message)
        new_msg.save_to_db(cursor)
        print("Message to:", target, "sent!")
    else:
        print("Addressee not found, message not sent - check spelling")


if __name__ == '__main__':
    try:
        connection = connect(host='localhost', user='postgres', password='2121', database='ping_me_db')
        connection.autocommit = True
        cursor = connection.cursor()

        if args.username and args.password and args.to and args.send:
            if login_or_new_user(args.username, args.password, cursor):
                send_message(args.username, args.to, args.send, cursor)
            else:
                print("Failed to log in, check your credentials")
        elif args.username and args.password and args.list:
            list_messages(args.username, args.password, cursor)
        else:
            parser.print_help()

        cursor.close()
        connection.close()
    except OperationalError as err:
        print("Connection Error: ", err)
