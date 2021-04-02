import datetime
import time
import datetime
import random
import psycopg2 as psycopg2

from utils.show_pantry import add_to_pantry
from utils.config import config


###########################################################################
#   Fills the pantry and pantry related tables with random ingredients
#       for random users.  Takes a second per entry because OrderId is
#       generated based off of the current time, and overlap ensues if
#       orders are filled too quickly.
#
#   Tables that fill:
#       - Pantry
#       - PantryOrders
#       - UserOrders
#


# REQUIRED: Change connection line 'conn = psycopg2.connect(**params)' in show_pantry.add_to_pantry
#  to 'conn = psycopg2.connect(host="reddwarf.cs.rit.edu",
#  database="p320_03f", user="p320_03f", password="KFnU9gXi7JFk")'
def get_column(checkdb):
    """
    gets a list of ingredient names from the sql database
    """
    names = []
    conn = None
    results = "alpha"
    try:
        # read database configuration
        # params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(host="reddwarf.cs.rit.edu", database="p320_03f", user="p320_03f", password="KFnU9gXi7JFk")
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
    for result in results:
        names.append(result[0])
    return names


if __name__ == '__main__':
    checkdb = """SELECT "UserId" FROM "Users" """
    uids = get_column(checkdb)  # get list of uids

    checkdb = """SELECT "IngredientName" FROM "Ingredients" """
    ingredients = get_column(checkdb)
    for i in range(0, len(uids)):
        rand_ingredient = random.choice(ingredients)  # select random ingredient name
        rand_user = random.choice(uids)               # select a random lucky user to add ingredient to
        cur_time = datetime.datetime.now()
        time.sleep(1)
        add_to_pantry(rand_ingredient, random.randint(1, 200), cur_time, cur_time + datetime.timedelta(days=7), rand_user)
