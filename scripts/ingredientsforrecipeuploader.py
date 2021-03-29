import csv
import datetime
import random
import psycopg2 as psycopg2
import time
from random_username.generate import generate_username

from scripts.passwords import generate_passwords


class recipe_ingredients:
    def __init__(self, RecipeId, IngredientIds):
        self.recipe_id = RecipeId
        self.ingredient_ids = IngredientIds
        self.amount = 1

    def getList(self):
        recipe_ingredients = []
        recipe_ingredients.append(self.recipe_id)
        recipe_ingredients.append(self.ingredient_ids)
        recipe_ingredients.append(self.amount)
        return recipe_ingredients


def recipe_ingredients_uploader():
    start = time.time()
    recipe_ingredients_list = []

    count = 0
    with open('data/PP_recipes.csv', encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # skip first row
        next(csv_reader)
        for row in csv_reader:
            # we dont want RecipeIds greater than 25000
            if int(row[0]) > 25000:
                continue
            recipe_id = row[0]
            ingredient_ids = row[7].strip('[]').replace(" ","")
            ingredient_ids = ingredient_ids.split(',')
            for ingr_id in ingredient_ids:
                new_user = recipe_ingredients(recipe_id, ingr_id)
                recipe_ingredients_list.append(new_user.getList())
                count += 1


    recipe_id_sql = """SELECT "RecipeId" FROM "Recipes" WHERE "RecipeId" is not NULL"""
    ingredient_id_sql = """SELECT "IngredientId" FROM "Ingredients" WHERE "IngredientId" is not NULL"""
    sql = """INSERT INTO "IngredientsForRecipe"("RecipeId", "IngredientId", "Amount") VALUES(%s, %s, %s)"""
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = conn = psycopg2.connect(host="reddwarf.cs.rit.edu", database="p320_03f", user="p320_03f",
                                       password="KFnU9gXi7JFk")
        # create a new cursor
        cur = conn.cursor()
        # get our list of valid recipe_ids
        cur.execute(recipe_id_sql)
        valid_recipe_ids = [item[0] for item in cur.fetchall()]
        # get our list of valid ingredient_ids
        cur.execute(ingredient_id_sql)
        valid_ingredient_ids = [item[0] for item in cur.fetchall()]
        # execute the INSERT statement
        for recipe_info in recipe_ingredients_list:
            if int(recipe_info[0]) in valid_recipe_ids and int(recipe_info[1]) in valid_ingredient_ids:
                cur.execute(sql, (recipe_info[0], recipe_info[1], recipe_info[2]))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    end = time.time()
    print(end - start)


if __name__ == '__main__':
    recipe_ingredients_uploader()