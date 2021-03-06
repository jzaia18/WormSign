import datetime
import psycopg2 as psycopg2

from utils.config import config


def insert_user(username, password):
    """ insert a new user into the users table """
    check_sql = """SELECT * FROM "Users" WHERE "Username" = '{}';""".format(username)
    sql = """INSERT INTO "Users"("Username", "Password", "DateJoined", "LastAccessDate") VALUES(%s, %s, %s, %s) RETURNING "UserId" """
    ct = datetime.datetime.utcnow()
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # check if user exists
        cur.execute(check_sql)
        user = cur.fetchone()

        if user is not None:
            return 'failed', None
        else:
            # execute the INSERT statement
            cur.execute(sql, (username, password, ct, ct))
            user_id = cur.fetchone()[0]
            # commit the changes to the database
            conn.commit()

        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 'failed', None
    finally:
        if conn is not None:
            conn.close()
    return 'success', user_id


def login_user(username, password):
    """ logs user into the recipe manager """
    check_user = """SELECT * FROM "Users" WHERE "Username" = '{}';""".format(username)
    check_user_password = """SELECT * FROM "Users" WHERE "Username" = '{}' AND "Password" = '{}';""".format(username, password)
    ct = datetime.datetime.utcnow()
    sql = """UPDATE "Users" SET "LastAccessDate" = '{}' WHERE "Username" = '{}' AND "Password" = '{}'""".format(ct, username, password)
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # check if user exists
        cur.execute(check_user)
        user = cur.fetchone()
        # if user is empty this user doesn't exist failed
        if user is None:
            return 'no-account', None

        # if the user is not empty check the password
        cur.execute(check_user_password)
        user_and_password = cur.fetchone()

        # if user is empty this login failed
        if user_and_password is None:
            return 'failed', None
        else:
            # execute the UPDATE statement
            cur.execute(sql)
            # commit the changes to the database
            conn.commit()

        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 'failed', None
    finally:
        if conn is not None:
            conn.close()
    return 'success', user[0]
