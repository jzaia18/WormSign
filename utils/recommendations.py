import psycopg2 as psycopg2

from utils.config import config


def recommend_by_rating():
    """ finds recipe based on search """
    checkdb = """SELECT "RecipeId", "RecipeName", "avg" FROM
                 (SELECT "Recipes"."RecipeId", "Recipes"."RecipeName", ROUND(AVG("CookedRecipes"."Rating") ,2) AS "avg"
                 FROM "Recipes" INNER JOIN "CookedRecipes"
                 ON  "Recipes"."RecipeId" = "CookedRecipes"."RecipeId"
                 GROUP BY "Recipes"."RecipeId") AS "Ratings"
                 ORDER BY "avg" DESC;"""

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
