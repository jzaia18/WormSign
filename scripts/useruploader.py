import csv
import datetime
import random
import psycopg2 as psycopg2
import time
from random_username.generate import generate_username

from scripts.passwords import generate_passwords


class user:
    def __init__(self, UserId, Username, Password, DateJoined, LastAccessDate):
        self.id = UserId
        self.username = Username
        self.password = Password
        self.datejoined = DateJoined
        self.lastaccessdate = LastAccessDate

    def getList(self):
        user = []
        user.append(self.id);
        user.append(self.username);
        user.append(self.password)
        user.append(self.datejoined);
        user.append(self.lastaccessdate)
        return user


def user_uploader():
    start = time.time()
    user_list = []
    ct = datetime.datetime.utcnow()
    usernames_list = generate_username(5000)
    new_usernames_list = [username + str(random.randint(0, 100000000)) for username in usernames_list]
    passwords_list = generate_passwords(5000)
    count = 0
    with open('data/PP_users.csv', encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # skip first row
        next(csv_reader)
        for row in csv_reader:
            # we dont want UserIds greater than 20000
            if int(row[0]) > 20000:
                continue
            new_user = user(row[0], new_usernames_list[count], passwords_list[count], ct, ct)
            user_list.append(new_user.getList())
            count += 1
            if count == 5000:  # this means end at recipe #15000
                break

    sql = """INSERT INTO "Users"("UserId", "Username", "Password", "DateJoined", "LastAccessDate") VALUES(%s, %s, %s, %s, %s)"""
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = conn = psycopg2.connect(host="reddwarf.cs.rit.edu", database="p320_03f", user="p320_03f",
                                       password="KFnU9gXi7JFk")
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        for userinfo in user_list:
            cur.execute(sql, (userinfo[0], userinfo[1], userinfo[2], userinfo[3], userinfo[4]))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    end = time.time()
    print(end - start)


if __name__ == '__main__':
    user_uploader()
