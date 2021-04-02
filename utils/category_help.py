import psycopg2 as psycopg2

from utils.config import config


def insert_category(recipe_id, category_id):
    """ inserts into the RecipeCategories Table """
    check_sql = """SELECT * FROM "RecipeCategories" 
                    WHERE "RecipeId" = '{}' AND "CategoryId" = '{}';""".format(recipe_id, category_id)
    insert_category_sql = """INSERT INTO "RecipeCategories"("RecipeId", "CategoryId") VALUES(%s, %s)"""
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
            # execute the INSERT statement to the RecipeCategories table
            cur.execute(insert_category_sql, (recipe_id, category_id))
            # commit the changes to the database
            conn.commit()
        else:
            return 'failed'

        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 'failed2'
    finally:
        if conn is not None:
            conn.close()
    return 'success'


def get_categories(userid):
    # get user's categories based on id
    retrieve = """SELECT X."CategoryId", X."CategoryName" FROM "Categories" X, "UserCategories"Y 
                    WHERE X."CategoryId" = Y."CategoryId" AND Y."UserId" = '{}';""".format(userid)
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # check if user exists
        cur.execute(retrieve)
        # store all results
        categories = cur.fetchall()
        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return categories