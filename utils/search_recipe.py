import psycopg2 as psycopg2

from utils.config import config


def search_recipe(keyword):
    """ finds recipe based on search """
    global results
    checkname = """SELECT "RecipeId", "RecipeName" FROM "Recipes" WHERE "RecipeName" LIKE '%{}%';""".format(keyword)

    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # check if user exists
        cur.execute(checkname)
        # store all results
        results = cur.fetchall()
        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return results
