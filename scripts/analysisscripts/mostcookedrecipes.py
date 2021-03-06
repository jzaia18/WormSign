import psycopg2 as psycopg2


def most_cooked_recipes():
    sql = """SELECT "CookedRecipes"."RecipeId", COUNT(*) c FROM "CookedRecipes" GROUP BY "RecipeId" ORDER BY c DESC"""

    conn = None
    try:
        # connect to the PostgreSQL database
        conn = conn = psycopg2.connect(host="reddwarf.cs.rit.edu", database="p320_03f", user="p320_03f",
                                       password="KFnU9gXi7JFk")
        # create a new cursor
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(sql)
        # commit the changes to the database
        results = cur.fetchall()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    # will put this data into some kind of graphic
    for result in results:
        print("RecipeId: " + str(result[0]) + "  Number of times cooked: " + str(result[1]))

if __name__ == '__main__':
    most_cooked_recipes()
