import psycopg2 as psycopg2

from utils.config import config


def search_recipe(searchType, keyword):
    """ finds recipe based on search """
    if searchType == 'name':
        checkdb = """SELECT "RecipeId", "RecipeName" FROM "Recipes" 
                        WHERE "RecipeName" LIKE '%{}%' ORDER BY "RecipeName" ASC;""".format(keyword)
    elif searchType == 'ingredient':
        checkdb = """SELECT DISTINCT X."RecipeId", X."RecipeName" FROM "Recipes" X, "IngredientsForRecipe" Y, "Ingredients" Z
                        WHERE X."RecipeId" = Y."RecipeId" AND Y."IngredientId" = Z."IngredientId" AND
                        Z."IngredientName" LIKE '%{}%' ORDER BY X."RecipeName" ASC;""".format(keyword)
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


def search_recipe_rating(searchType, keyword):
    """ finds recipe based on search """
    if searchType == 'name':
        checkdb = """SELECT "RecipeId", "RecipeName", "avg" FROM 
                        (SELECT "Recipes"."RecipeId", "Recipes"."RecipeName", ROUND(AVG("CookedRecipes"."Rating") ,2) AS "avg"
                        FROM "Recipes" INNER JOIN "CookedRecipes" 
                        ON  "Recipes"."RecipeId" = "CookedRecipes"."RecipeId"
                        GROUP BY "Recipes"."RecipeId") AS "Ratings"
                        WHERE "RecipeName" LIKE '%{}%' ORDER BY "avg" DESC;""".format(keyword)

    elif searchType == 'ingredient':
        checkdb = """SELECT DISTINCT "Ratings"."RecipeId", "Ratings"."RecipeName", "avg" FROM 
                        (SELECT "Recipes"."RecipeId", "Recipes"."RecipeName", ROUND(AVG("CookedRecipes"."Rating") ,2) AS "avg"
                        FROM "Recipes" INNER JOIN "CookedRecipes" 
                        ON  "Recipes"."RecipeId" = "CookedRecipes"."RecipeId"
                        GROUP BY "Recipes"."RecipeId") AS "Ratings", "IngredientsForRecipe" Y, "Ingredients" Z
                        WHERE "Ratings"."RecipeId" = Y."RecipeId" AND Y."IngredientId" = Z."IngredientId" AND
                        Z."IngredientName" LIKE '%{}%' ORDER BY "avg" DESC;""".format(keyword)
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


def search_recipe_recent(searchType, keyword):
    """ finds recipe based on search """
    if searchType == 'name':
        checkdb = """SELECT "RecipeId", "RecipeName", "CreationDate" FROM "Recipes" 
                        WHERE "RecipeName" LIKE '%{}%' ORDER BY "CreationDate" DESC;""".format(keyword)
    elif searchType == 'ingredient':
        checkdb = """SELECT DISTINCT X."RecipeId", X."RecipeName", "CreationDate" FROM "Recipes" X, "IngredientsForRecipe" Y, "Ingredients" Z
                        WHERE X."RecipeId" = Y."RecipeId" AND Y."IngredientId" = Z."IngredientId" AND
                        Z."IngredientName" LIKE '%{}%' ORDER BY X."CreationDate" DESC;""".format(keyword)
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


def get_recipe(recipeid):
    # get recipe entity based on id
    retrieve = """SELECT * FROM "Recipes" WHERE "RecipeId" = '{}';""".format(recipeid)
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # check if user exists
        cur.execute(retrieve)
        # store all results
        recipe = cur.fetchone()
        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return recipe


def get_creator(userid):
    # get user entity based on id
    retrieve = """SELECT "Username" FROM "Users" WHERE "UserId" = '{}';""".format(userid)
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # check if user exists
        cur.execute(retrieve)
        # store all results
        user = cur.fetchone()
        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return user


def get_ingredients(recipeid):
    # gets ingredients based on recipeid
    retrieve = """SELECT X."IngredientName" FROM "Ingredients" X, "IngredientsForRecipe" Y
        WHERE X."IngredientId" = Y."IngredientId" AND Y."RecipeId" = '{}';""".format(recipeid)
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # check if user exists
        cur.execute(retrieve)
        # store all results
        ingredients = cur.fetchall()
        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return ingredients


def get_rating(recipeid):
    # gets rating based on recipeid
    avgrating = """SELECT ROUND(AVG("Rating") ,2) FROM "CookedRecipes" WHERE "RecipeId" = '{}';""".format(recipeid)
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # check if user exists
        cur.execute(avgrating)
        # store all results
        rating = cur.fetchone()
        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rating


def format_steps(steps):
    steps = steps.replace("[\'", '')
    steps = steps.replace("\']", '')
    steps = steps.split("\', \'")
    return steps
