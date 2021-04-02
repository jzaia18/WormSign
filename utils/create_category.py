import datetime
import psycopg2 as psycopg2

from utils.config import config


def create_category(user_id, category_name):
    """ create a new category """
    check_sql = """SELECT * FROM "Categories" INNER JOIN "UserCategories" On "Categories"."CategoryId" = "UserCategories"."CategoryId"
        WHERE "CategoryName" = '{}' AND "UserId" = '{}';""".format(category_name, user_id)
    insert_category_sql = """INSERT INTO "Categories"("CategoryName") VALUES(%s) RETURNING "CategoryId" """
    insert_user_category_sql = """INSERT INTO "UserCategories"("UserId", "CategoryId") VALUES(%s, %s)"""
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # check if user exists
        cur.execute(check_sql)
        category = cur.fetchone()

        if category is None:
            # execute the INSERT statement to the Categories table
            cur.execute(insert_category_sql, (category_name,))
            # retrieve the generated category id statement
            category_id = cur.fetchone()[0]
            # execute the INSERT statement to the UserCategory table
            cur.execute(insert_user_category_sql, (user_id, category_id))
            # commit the changes to the database
            conn.commit()
        else:
            return 'failed'

        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 'failed'
    finally:
        if conn is not None:
            conn.close()
    return 'success'
