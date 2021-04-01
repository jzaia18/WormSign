import psycopg2 as psycopg2
import datetime

from utils.config import config


def create_recipe(recipe_name, description, cook_time, servings, difficulty, ingredient_list, steps, user_id):
    """ creates a new recipe """
    results = None
    conn = None
    checkdb = """INSERT INTO Recipes (RecipeName, Description, Servings, CookTime, Difficulty, Steps, UserId, CreationDate)
                   VALUES ({}, {}, {}, {}, {}, {}, {}, {})""".format(recipe_name, description, servings, cook_time, difficulty, steps, user_id, datetime.datetime.utcnow())

    print(checkdb)
    return
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # check if user exists
        cur.execute(checkdb)
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
