import psycopg2 as psycopg2

def top_10_chefs():
    sql = """WITH X as (SELECT "CookedRecipes"."UserId", avg("CookedRecipes"."Rating") AverageRating, COUNT(*) RecipesCooked FROM "CookedRecipes" GROUP BY "UserId" ORDER BY AverageRating DESC)
            Select * From X where RecipesCooked > 10 limit 10"""

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

    # might want to grab the user name too before using this data, can easily change the number of recipes needed
    # to be considered a "chef" above
    for result in results:
        print("UserId: " + str(result[0]) + "  Average Rating of Recipes: " + str(result[1]) + "  Number of Recipes cooked: " + str(result[2]))


if __name__ == '__main__':
    top_10_chefs()
