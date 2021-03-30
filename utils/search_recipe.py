import psycopg2 as psycopg2

from utils.config import config


def search_recipe(searchType, keyword):
    """ finds recipe based on search """
    if searchType == 'name':
        checkdb = """SELECT "RecipeId", "RecipeName" FROM "Recipes" 
                        WHERE "RecipeName" LIKE '%{}%';""".format(keyword)
    elif searchType == 'ingredient':
        checkdb = """SELECT X."RecipeId", X."RecipeName" FROM "Recipes" X, "IngredientsForRecipe" Y, "Ingredients" Z
                        WHERE X."RecipeId" = Y."RecipeId" AND Y."IngredientId" = Z."IngredientId" AND
                        Z."IngredientName" LIKE '%{}%';""".format(keyword)
    # elif searchType == 'category':

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
