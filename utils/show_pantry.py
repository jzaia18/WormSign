import psycopg2 as psycopg2
import datetime

from utils.config import config


def show_pantry(uid):
    """ gets a user's pantry data """
    global results
    checkdb = """SELECT I."IngredientName", P."CurrentQuantity", P."ExpirationDate", P."OrderId"
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


def add_to_pantry(ingredient, amount, purchased, exp, uid):
    """adds a user's input to the pantry table (and other necessary tables)"""
    checkdb = """SELECT "IngredientId" FROM "Ingredients"
                        WHERE "IngredientName" LIKE '%{}%';""".format(ingredient)
    conn = None
    error = None
    if not amount or not ingredient:
        error = "Please fill in the required fields to add an item to your pantry."
        return error
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
        if bool(cur.rowcount):  # if item existed in db
            ingred_id = cur.fetchone()[0]  # should probably check if this is valid
            order_id = int(datetime.datetime.utcnow().timestamp())

            # "store this order" message for pantry
            checkdb = """INSERT INTO "Pantry"("OrderId", "PurchaseDate", "ExpirationDate", 
                                                "PurchaseQuantity", "CurrentQuantity") 
                                                    VALUES(%s, %s, %s, %s,%s)"""
            cur.execute(checkdb, (order_id, purchased, exp, amount, amount))

            # connect new order to user
            checkdb = """INSERT INTO "UserOrders"("UserId", "OrderId") VALUES(%s, %s)"""
            cur.execute(checkdb, (uid, order_id))

            # connect order to ingredient
            checkdb = """INSERT INTO "OrderIngredients"("OrderId", "IngredientId") VALUES(%s, %s)"""
            cur.execute(checkdb, (order_id, ingred_id))

            # commit the changes!
            conn.commit()
        else:
            error = "That item does not exist in the ingredient table!"
        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return error


def update_pantry(order_id, amount, uid):
    """

    """
    checkdb = """SELECT P."CurrentQuantity" FROM "Pantry" P, "UserOrders" U           
                        WHERE P."OrderId" = '{}' AND U."UserId" = '{}';""".format(order_id, uid)
    conn = None
    error = None
    if not amount or not order_id:
        error = "Please fill in the required fields to update an item in your pantry."
        return error
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()

        # grab ingredient id from db
        cur.execute(checkdb)
        if bool(cur.rowcount):  # if order exists in pantry
            if int(amount) == 0:     # drop this order from the pantry table
                # delete order from order ingredients
                checkdb = """DELETE FROM "OrderIngredients" WHERE "OrderId" = '{}'""".format(order_id)
                cur.execute(checkdb)

                # ""   ""   "" from UserOrders
                checkdb = """DELETE FROM "UserOrders" WHERE "OrderId" = '{}'""".format(order_id)
                cur.execute(checkdb)

                # ""   ""   "" from Pantry
                checkdb = """DELETE FROM "Pantry" WHERE "OrderId" = '{}'""".format(order_id)
                cur.execute(checkdb)
                pass

            else:   # update order with new amount
                checkdb = """UPDATE "Pantry" 
                                SET "CurrentQuantity" = '{}'
                                WHERE "OrderId" = '{}'""".format(amount, order_id)
                cur.execute(checkdb)

            conn.commit()  # commit the changes!  Either way we have to commit
        else:
            error = "There is no such orderId in your pantry!"
        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return error
