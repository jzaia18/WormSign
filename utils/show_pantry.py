import psycopg2 as psycopg2

from utils.config import config


def show_pantry(uid):
    """ gets a user's pantry data """
    global results
    checkdb = """SELECT I."IngredientName" FROM "UserOrders" U, "OrderIngredients" O, "Ingredients" I, 
                        WHERE U."UserId" = '%{}%' AND U."OrderId" = O."OrderId" AND 
                        O."IngredientId" = I."IngredientId";""".format(uid)
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
