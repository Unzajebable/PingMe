import argparse
from psycopg2 import connect, OperationalError
from module import User, Message
from clcrypto import check_password


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-t", "--to", help="addressee username")
parser.add_argument("-s", "--send", help="message content")
parser.add_argument("-l", "--list", help="show all messages", action="store_true")

arg = parser.parse_args()


def list_messages(username, cursor):
    messages = Message.load_all_messages(cursor, username.id)
    for message in messages:
        from_ = User.load_user_by_id(cursor, message.from_id)
        print(50 * "=")
        print(f"| from: {from_.username} | date: {message.created_date} |")
        print()
        print(message.message)
        print(50 * "_")
    # curr_user = User.load_user_by_username(username, cursor)
    # messages = Message.show_all_my_messages(curr_user.id, cursor)
    # for message in messages:
    #     from_ = User.load_user_by_id(cursor, (message.from_id, ))
    #     print(30 * "=")
    #     print(f"from: {from_.username} | date: {message.created_date}")
    #     print(message.message)
    #     print(30 * "=")
    #====================================================================
    # if new_user(username, password, cursor):
    #     curr_user = User.load_user_by_username(cursor, username)
    #     if curr_user:
    #         return Message.show_all_my_messages(curr_user.id, cursor)
    #     else:
    #         print("User not found")
    # else:
    #     print("Failed to log in, check your credentials")


def send_message(username, target, message, cursor):
    curr_user = User.load_user_by_username(username, cursor)
    target_user = User.load_user_by_username(target, cursor)
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

        if arg.username and arg.password:
            curr_user = User.load_user_by_username(arg.username, cursor)
            if check_password(arg.password, curr_user.hashed_password):
                if arg.list:
                    list_messages(curr_user, cursor)
                elif arg.to and arg.send:
                    send_message(arg.username, arg.to, arg.send, cursor)
                else:
                    parser.print_help()
            else:
                print("Incorrect password or User does not exists!")
        else:
            print("username and password are required")
            parser.print_help()

        connection.close()
    except OperationalError as err:
        print("Connection Error: ", err)
