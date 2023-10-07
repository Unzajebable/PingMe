import argparse
from create_db import create_db
from psycopg2 import connect
from module import User, Message

create_db()
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_password", help="set new password")
parser.add_argument("-l", "--list", help="list users", action="store_true")
parser.add_argument("-d", "--delete", help="delete specified user")
parser.add_argument("-e", "--edit", help="edit a user")

args = parser.parse_args()

while True:
    if len(args.password) < 8:
        args.password = input("Password has to have at least 8 characters: ")
    else:
        break

connection = connect(host='localhost', user='postgres', password='2121', database='ping_me_db')
connection.autocommit = True
cursor = connection.cursor()

if args.username == True and args.password == True and args.edit == True and args.new_password == True:
    while True:
        if len(args.new_password) < 8:
            args.new_password = input("New password also has to have at least 8 characters: ")
        else:
            
            User.new_hashed_password(args.password, args.new_password)
            break
elif args.username == True and args.password == True and args.delete == True:

elif args.username == True and args.password == True:
    new_user = User(args.username, args.password)
    new_user.save_to_db(cursor)
elif args.list:
    User.load_all_users(cursor)
else:
    parser = argparse.ArgumentParser()
    parser.print_help()
