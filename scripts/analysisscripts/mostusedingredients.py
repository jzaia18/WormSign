import pickle
import psycopg2 as psycopg2
import time


def most_used_ingredients():
    sql = """WITH X as (Select "Ingredients"."IngredientId", "Ingredients"."IngredientName", COUNT(*) CookedCount from "Ingredients"
                INNER JOIN "IngredientsForRecipe" IFR on "Ingredients"."IngredientId" = IFR."IngredientId"
                INNER JOIN "CookedRecipes" CR on IFR."RecipeId" = CR."RecipeId"
                GROUP BY "Ingredients"."IngredientId" ORDER BY CookedCount DESC)
                Select * From X"""

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

    for result in results:
        print("IngredientId: " + str(result[0]) + "  IngredientName: " + str(
            result[1]) + "  Number of uses " + str(result[2]))


if __name__ == '__main__':
    most_used_ingredients()
