import psycopg2 as psycopg2
import datetime

from utils.config import config


def create_recipe(recipe_name, description, cook_time, servings, difficulty, ingredient_list, steps, user_id):
    """ creates a new recipe """
    return
    results = None
    conn = None
    insert_recipe = """INSERT INTO "Recipes" ("RecipeName", "Description", "Servings", "CookTime", "Difficulty", "Steps", "UserId", "CreationDate")
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING "RecipeId"
    """

    ## TODO: requires amounts, not yet implemented
    insert_ingredient = """INSERT INTO "IngredientsForRecipe" ("RecipeId", "IngredientId")
    """
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # check if user exists
        results = cur.execute(insert_recipe, (recipe_name, description, servings, cook_time, difficulty, steps, user_id, datetime.datetime.utcnow()))


        # commit the results
        # conn.commit()

        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(difficulty, len(difficulty))
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return results
