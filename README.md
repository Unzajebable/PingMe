# PingMe
Basic python based communicator.

# How to:

`open Command prompt > input a path to folder location`

create a new user:
`python/python3 user_handling.py -u [username here] -p [password here]`

​change your password:
`python/python3 user_handling.py -u [username here] -p [password here] -e -n [new password here]`

delete a user:
​`python/python3 user_handling.py -u [username here] -p [password here] -d`

list all users:
​`python/python3 user_handling.py -l`

send a message:
​`python/python3 PingMe.py -u [username here] -p [password here] -l`

show all your messages:
​​`python/python3 PingMe.py -u [username here] -p [password here] -t [target username here] -s [message content here]`

### when entering a command do not use brackets and figure out which python/python3 command works for your OS

Windows command example: `python user_handling.py -l`

Linux command example: `python3 user_handling.py -l`
