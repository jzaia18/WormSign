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


def recommend_by_user(userid):
    """ finds recipe based on search """
    checkdb = """SELECT DISTINCT "Ratings"."RecipeId", "RecipeName", "avg" FROM
                     (SELECT "Recipes"."RecipeId", "Recipes"."RecipeName", ROUND(AVG("CookedRecipes"."Rating") ,2) AS "avg"
                        FROM "Recipes" INNER JOIN "CookedRecipes"
                        ON  "Recipes"."RecipeId" = "CookedRecipes"."RecipeId"
                        GROUP BY "Recipes"."RecipeId") AS "Ratings", 
                     (SELECT DISTINCT "CookedRecipes"."UserId" FROM
                        (SELECT DISTINCT "RecipeId", "UserId" FROM "CookedRecipes" 
                            WHERE "UserId" = '{}') AS "WasMade", "CookedRecipes"
                        WHERE "WasMade"."RecipeId" = "CookedRecipes"."RecipeId" 
                        AND "WasMade"."UserId" != "CookedRecipes"."UserId") AS "OtherUsers", "CookedRecipes"
                    WHERE "OtherUsers"."UserId" = "CookedRecipes"."UserId" AND 
                    "CookedRecipes"."RecipeId" NOT IN 
                        (SELECT DISTINCT "RecipeId" FROM "CookedRecipes" WHERE "UserId" = '{}') 
                    AND "Ratings"."RecipeId" = "CookedRecipes"."RecipeId" ORDER BY "avg" DESC;""".format(userid, userid)

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


def recommend_by_recent():
    """ finds recipe based on search """
    checkdb = """SELECT "RecipeId", "RecipeName", "CreationDate"
                 FROM "Recipes"
                 ORDER BY "CreationDate" DESC;"""
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


def recommend_by_pantry(user_id):

    checkdb = """SELECT DISTINCT "Ratings"."RecipeId", "RecipeName", "avg" FROM
                    (SELECT "Available"."RecipeId", COUNT("Available"."RecipeId") AS "NumYouHave" FROM
                        (SELECT "IngredientsForRecipe"."RecipeId" FROM
                            (SELECT I."IngredientId", P."CurrentQuantity", P."OrderId" FROM "UserOrders" U, 
                            "OrderIngredients" O, "Ingredients" I, "Pantry" P WHERE U."UserId" = '{}' AND 
                            U."OrderId" = O."OrderId" AND O."IngredientId" = I."IngredientId" AND 
                            U."OrderId" = P."OrderId") AS "UserPantry", "IngredientsForRecipe"
                        WHERE "UserPantry"."IngredientId" = "IngredientsForRecipe"."IngredientId" AND
                        "UserPantry"."CurrentQuantity" >= "IngredientsForRecipe"."Amount") AS "Available"
                        GROUP BY "Available"."RecipeId") AS "IngYouHave",
                    (SELECT "RecipeId", COUNT("IngredientId") AS "NumYouNeed" FROM "IngredientsForRecipe"
                        GROUP BY "RecipeId") AS "IngYouNeed",
                    (SELECT "Recipes"."RecipeId", "Recipes"."RecipeName", 
                        ROUND(AVG("CookedRecipes"."Rating") ,2) AS "avg" FROM "Recipes" INNER JOIN "CookedRecipes" 
                        ON  "Recipes"."RecipeId" = "CookedRecipes"."RecipeId" 
                        GROUP BY "Recipes"."RecipeId") AS "Ratings" 
                WHERE "IngYouNeed"."RecipeId" = "IngYouHave"."RecipeId" AND 
                "IngYouNeed"."NumYouNeed" = "IngYouHave"."NumYouHave" AND 
                "IngYouHave"."RecipeId" = "Ratings"."RecipeId" ORDER BY "avg" DESC;""".format(user_id)

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