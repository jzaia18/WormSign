import psycopg2 as psycopg2
import datetime

from utils.config import config


def create_recipe(recipe_name, description, cook_time, servings, difficulty, ingredient_list, steps, user_id):
    """ creates a new recipe """
    result = None
    conn = None
    insert_recipe = """INSERT INTO "Recipes" ("RecipeName", "Description", "Servings", "CookTime", "Difficulty", "Steps", "UserId", "CreationDate")
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING "RecipeId"
    """

    insert_ingredient = """INSERT INTO "IngredientsForRecipe" ("RecipeId", "IngredientId", "Amount")
                             VALUES (%s, %s, %s)
    """

    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()

        # check if user exists
        cur.execute(insert_recipe, (recipe_name, description, servings, cook_time, difficulty, steps, user_id, datetime.datetime.utcnow()))

        result = cur.fetchone()[0]

        for pair in ingredient_list:
            cur.execute(insert_ingredient, (result, pair[0], pair[1]))

        # commit the results
        conn.commit()

        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result


def update_recipe(recipe_id, recipe_name, description, cook_time, servings, difficulty, ingredient_list, steps):
    """ creates a new recipe """
    result = None
    conn = None
    update_recipe = """UPDATE "Recipes"
                         SET "RecipeName" = %s, "Description" = %s, "Servings" = %s, "CookTime" = %s, "Difficulty" = %s, "Steps" = %s
                         WHERE "RecipeId" = %s
                         RETURNING "RecipeId"
    """

    delete_old_ingredients = """DELETE FROM "IngredientsForRecipe"
                                  WHERE "RecipeId" = %s
    """

    insert_ingredient = """INSERT INTO "IngredientsForRecipe" ("RecipeId", "IngredientId", "Amount")
                             VALUES (%s, %s, %s)
    """

    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()

        # check if user exists
        cur.execute(update_recipe, (recipe_name, description, servings, cook_time, difficulty, steps, recipe_id))

        result = cur.fetchone()[0]

        cur.execute(delete_old_ingredients, (recipe_id,))

        for pair in ingredient_list:
            cur.execute(insert_ingredient, (result, pair[0], pair[1]))

        # commit the results
        conn.commit()

        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result


def get_my_recipes(uid):
    """ gets all a users' recipes """
    result = None
    conn = None

    get_recipes = """SELECT  "RecipeId", "RecipeName" FROM "Recipes"
                       WHERE "UserId" = %s
    """

    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()

        # check if user exists
        cur.execute(get_recipes, (uid,))

        result = cur.fetchall()

        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result
