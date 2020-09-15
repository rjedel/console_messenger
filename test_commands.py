test_users = """"
python3 users.py&&
python3 users.py -l&&
python3 users.py -p nicepass -u Joe&&
python3 users.py -p ni -u Joe&&
python3 users.py -p nicepassword -u Joe&&
python3 users.py -p nicepassw -u Ann&&
python3 users.py -p nicepassw -u Mary&&
python3 users.py -l&&
python3 users.py -u Joe -p wrongpass -n new_pass -e&&
python3 users.py -u WrongUser -p somepassword -n new_pass -e&&
python3 users.py -u Joe -p nicepass -n new#passwd -e&&
python3 users.py -u Mary -p wrongpass -d&&
python3 users.py -u Mary -p nicepassw -d&&
python3 users.py -l&&
python3 users.py -p passwo5d -u Monica&&
python3 users.py -p wordpass -u Bob
"""

messages = """"
python3 messages.py -l -u Joe -p new#passwd&&
python3 messages.py -l -u Ann -p nicepassw&&
python3 messages.py -u Ann -p nicepassw -t Joe -s "Hello Joe"&&
python3 messages.py -u Ann -p nicepassw -t Joe -s "How Are You?"&&
python3 messages.py -u Ann -p nicepassw -t Joe -s "Are you OK?"&&
python3 messages.py -u Joe -p new#passwd -t Wronuser -s "from joe to ann"&&
python3 messages.py -u Joe -p new#passwd -t Ann -s "Hi, Ann I'm fine"&&
python3 messages.py -u Monica -p passwo5d -t Joe -s "Hi, Joe"&&
python3 messages.py -u Monica -p passwo5d -t Bob -s "Meeting tomorrow 1 P.M."&&
python3 messages.py -u Bob -p wordpass -t Monica -s "fine by me"&&
python3 messages.py -u Bob -p wordpass -t Ann -s "Where are You?"&&
python3 messages.py -u Bob -p wordpass -t wrongrecipient -s "some message"&&
python3 messages.py -u Bob -p wordpass -l&&
python3 messages.py -u Monica -p passwo5d -l&&
python3 messages.py -u Ann -p nicepassw -l&&
python3 messages.py -u Joe -p new#passwd -l&&
python3 messages.py -l -u Ann -p nicepassw&&
python3 messages.py -l -u Ann -p wrongpass
"""
