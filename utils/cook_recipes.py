import psycopg2 as psycopg2
import datetime

from utils.config import config


def check_for_ingredient(ingredient_id, user_id):
    """ gets a user's pantry data """
    checkdb = """SELECT P."OrderId", P."CurrentQuantity" FROM "Pantry" P, "OrderIngredients" O, "UserOrders" U
                    WHERE O."IngredientId" = '{}' AND U."UserId" = '{}' AND P."OrderId" = O."OrderId" AND
                    P."OrderId" = U."OrderId" AND O."OrderId" = U."OrderId";""".format(ingredient_id, user_id)
    conn = None
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
        result = cur.fetchone()
        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result


def remove_ingredients(order):
    """ gets a user's pantry data """
    updatedb = """UPDATE "Pantry" SET "CurrentQuantity" = '{}' WHERE "OrderId" = '{}';""".format(order[0], order[1])
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # check if user exists
        cur.execute(updatedb)
        # store all results
        conn.commit()
        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return 'success'


def cook(scale, rating, userid, recipeid):
    """ gets a user's pantry data """
    checkdb = """INSERT INTO "CookedRecipes"("DateCooked", "Scale", "Rating", "UserId", "RecipeId") 
                    VALUES(%s, %s, %s, %s, %s)"""
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
        cur.execute(checkdb, (ct, scale, rating, userid, recipeid))
        # store all results
        conn.commit()
        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return 'success'
