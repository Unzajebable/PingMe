import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
#parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-l", "--list", help="list users", action="store_true")

args = parser.parse_args()
print(args.username)
