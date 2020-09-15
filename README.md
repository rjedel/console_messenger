# console_messenger
A console application for messaging between users.

Requirements: 
psycopg2-binary==2.8.5

##### Example:
```plaintext
$ python3 users.py -p nicepass -u Jon  
"Jon" user created

$ python3 users.py -u Joe -p wrongpass -n new_pass -e
Incorrect Password!

$ python3 users.py -u Joe -p nicepass -n new_pass -e
password has been changed

$ python3 users.py -u WrongUser -p somepassword -n new_pass -e
no user "WrongUser"

$ python3 messages.py -u Monica -p passwo5d -t Joe -s "Meeting tomorrow 1 P.M."
Message send

$ python3 messages.py -l -u Joe -p new_pass
Joe's INBOX:

message from: Monica
sent on: 20-09-15 10:27:46
content: Meeting tomorrow 1 P.M.

message from: Ann
sent on: 20-09-15 11:09:50
content: Hello Joe
```
