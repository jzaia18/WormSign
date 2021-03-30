import datetime
import psycopg2 as psycopg2

from utils.config import config


def create_category(user_id, category_name):
    """ create a new category """
    check_sql = """SELECT * FROM "Categories" WHERE "CategoryId" = '{}';""".format(category_name)
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
            return 'failed'
        else:
            # execute the INSERT statement
            cur.execute(sql, (username, password, ct, ct))
            # commit the changes to the database
            conn.commit()

        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 'failed'
    finally:
        if conn is not None:
            conn.close()
    return 'success'