import argparse
from create_db import create_db
from psycopg2 import connect, OperationalError
from module import User
from clcrypto import check_password


create_db()
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_password", help="set new password")
parser.add_argument("-l", "--list", help="list users", action="store_true")
parser.add_argument("-d", "--delete", help="delete specified user")
parser.add_argument("-e", "--edit", help="edit a user")

args = parser.parse_args()


def login_or_new_user(username, password, cursor):
    while True:
        if len(password) < 8:
            password = input("Password has to have at least 8 characters: ")
        else:
            if not User.load_user_by_username(cursor, username):
                new_user = User(username, password)
                new_user.save_to_db(cursor)
                print("New user created!")
                return new_user
            else:
                print("Welcome back", username, "!")
                return User.load_user_by_username(cursor, username)


def user_edit(username, old_pass, new_password, cursor):
    while True:
        curr_user = User.load_user_by_username(cursor, username)
        if curr_user:
            if len(new_password) < 8:
                new_password = input("New password also has to have at least 8 characters: ")
            else:
                curr_user.new_hashed_password(old_pass, new_password)
                curr_user.save_to_db(cursor)
                print("Password for", username, " changed!")
                break


def delet_me(username, password, cursor):
    curr_user = User.load_user_by_username(cursor, username)
    if curr_user:
        if check_password(password, curr_user.hashed_password):
            curr_user.delete(cursor)
            curr_user.save_to_db(cursor)
            print(username, " successfully deleted!")


if __name__ == '__main__':
    try:
        connection = connect(host='localhost', user='postgres', password='2121', database='ping_me_db')
        connection.autocommit = True
        cursor = connection.cursor()

        if args.username and args.password:
            login_or_new_user(args.username, args.password, cursor)
        elif args.username and args.password and args.edit and args.new_password:
            user_edit(args.username, args.password, args.new_password, cursor)
        elif args.username and args.password and args.delete:
            delet_me(args.username, args.password, cursor)
        elif args.list:
            User.load_all_users(cursor)
        else:
            parser.print_help()

        cursor.close()
        connection.close()
    except OperationalError as err:
        print("Connection Error: ", err)
