import psycopg2 as psycopg2
import datetime

from utils.config import config


def show_pantry(uid):
    """ gets a user's pantry data """
    global results
    checkdb = """SELECT I."IngredientName", P."CurrentQuantity", P."ExpirationDate"
                        FROM "UserOrders" U, "OrderIngredients" O, "Ingredients" I, "Pantry" P
                        WHERE U."UserId" = '{}' AND U."OrderId" = O."OrderId" AND
                             O."IngredientId" = I."IngredientId" AND U."OrderId" = P."OrderId";""".format(uid)
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
        results = cur.fetchall()
        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return results


def update_pantry(ingredient, amount, purchased, exp, uid):
    """adds a user's input to the pantry table (and other necessary tables)"""
    checkdb = """SELECT "IngredientId" FROM "Ingredients"
                        WHERE "IngredientName" = '{}';""".format(ingredient)
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()

        # grab ingredient id from db
        cur.execute(checkdb)
        # store ingredient id
        ingred_id = cur.fetchone()[0]  # should probably check if this is valid
        order_id = int(datetime.datetime.utcnow().timestamp())

        # "store this order" message for pantry
        checkdb = """INSERT INTO "Pantry"("OrderId", "PurchaseDate", "ExpirationDate", "PurchaseQuantity", "CurrentQuantity") VALUES(%s, %s, %s, %s,%s)"""
        cur.execute(checkdb, (order_id, purchased, exp, amount, amount))

        # connect new order to user
        checkdb = """INSERT INTO "UserOrders"("UserId", "OrderId") VALUES(%s, %s)"""
        cur.execute(checkdb, (uid, order_id))

        # connect order to ingredient
        checkdb = """INSERT INTO "OrderIngredients"("OrderId", "IngredientId") VALUES(%s, %s)"""
        cur.execute(checkdb, (order_id, ingred_id))

        # commit the changes!
        conn.commit()
        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return None
