import psycopg2 as psycopg2

from utils.config import config
from utils.search_recipe import get_ingredients, get_recipe, get_rating
from utils.cook_recipes import check_for_ingredient


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
    """ finds recipe based on search """
    checkdbIDs = """SELECT "RecipeId"
                 FROM "Recipes"
                 ORDER BY "RecipeId" DESC;"""

    checkdbUserPantry = """SELECT I."IngredientName", P."CurrentQuantity", P."ExpirationDate", P."OrderId"
                        FROM "UserOrders" U, "OrderIngredients" O, "Ingredients" I, "Pantry" P
                        WHERE U."UserId" = '{}' AND U."OrderId" = O."OrderId" AND
                             O."IngredientId" = I."IngredientId" AND U."OrderId" = P."OrderId";""".format(user_id)
    recipeIds = []
    goodOnes = []
    canCook = []
    userPantry = []

    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # check if user exists
        cur.execute(checkdbIDs)
        # store all results
        recipeIds = cur.fetchall()[:50]
        cur.execute(checkdbUserPantry)
        userPantry = cur.fetchall()  # get the user's pantry
        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    for recipeid in recipeIds:
        ingredients = get_ingredients(recipeid[0])
        for ingredient in ingredients:
            include = True
            pantry_item = check_for_ingredient(ingredient[0], user_id)  # maybe slowing down
            if pantry_item is None:  # if user doesn't have an ingredient, can't use this recipe
                include = False
                break
            else:
                if ingredient[2] > pantry_item[1]:
                    include = False
                    break
        if include:
            goodOnes.append(recipeid[0])  # this recipe passes!
            print(recipeid)

    for winner in goodOnes:
        recipe = get_recipe(winner)
        canCook.append([recipe[0], recipe[1], get_rating(winner)[0]])
    canCook.sort(reverse=True, key=sortFunc)
    return canCook


def sortFunc(x):
    if x[2] is None:
        return -1
    else:
        return x[2]
