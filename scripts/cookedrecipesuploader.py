import csv
import psycopg2 as psycopg2
import time
import random


class cooked_recipe:
    def __init__(self, UserId, RecipeId, DateCooked, Scale, Rating):
        self.user_id = UserId
        self.recipe_id = RecipeId
        self.date_cooked = DateCooked
        self.scale = Scale
        self.rating = Rating

    def getList(self):
        cooked_recipes = []
        cooked_recipes.append(self.user_id)
        cooked_recipes.append(self.recipe_id)
        cooked_recipes.append(self.date_cooked)
        cooked_recipes.append(self.scale)
        cooked_recipes.append(self.rating)
        return cooked_recipes


def cooked_recipes_uploader():
    start = time.time()
    cooked_recipes_list = []
    rands = [.1, .25, .5, .75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75, 5
             , 5.25, 5.5, 5.75, 6, 6.25, 6.5, 6.75, 7, 7.25, 7.5, 7.75, 8, 8.25, 8.5, 8.75, 9, 9.25, 9.5, 9.75, 10]
    count = 0
    with open('data/RAW_interactions.csv', encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # skip first row
        next(csv_reader)
        for row in csv_reader:
            # we dont want UserId greater than 6000
            if int(row[0]) > 20000:
                continue
            # we dont want RecipeIds greater than 25000
            if int(row[1]) > 25000:
                continue
            user_id = row[0]
            recipe_id = row[1]
            date = row[2]
            rating = row[3]
            new_cooked_recipe = cooked_recipe(user_id, recipe_id, date, random.choice(rands), rating)
            cooked_recipes_list.append(new_cooked_recipe.getList())
            count += 1
            #if count >= 10:
             #   break

    recipe_id_sql = """SELECT "RecipeId" FROM "Recipes" WHERE "RecipeId" is not NULL"""
    user_id_sql = """SELECT "UserId" FROM "Users" WHERE "UserId" is not NULL"""
    sql = """INSERT INTO "CookedRecipes"("UserId", "RecipeId", "DateCooked", "Scale", "Rating") VALUES(%s, %s, %s, %s, %s)"""
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = conn = psycopg2.connect(host="reddwarf.cs.rit.edu", database="p320_03f", user="p320_03f",
                                       password="KFnU9gXi7JFk")
        # create a new cursor
        cur = conn.cursor()
        # get our list of valid user_ids
        cur.execute(user_id_sql)
        valid_user_ids = [item[0] for item in cur.fetchall()]
        # get our list of valid recipe_ids
        cur.execute(recipe_id_sql)
        valid_recipe_ids = [item[0] for item in cur.fetchall()]

        # execute the INSERT statement
        for cooked_recipe_info in cooked_recipes_list:
            if int(cooked_recipe_info[0]) in valid_user_ids and int(cooked_recipe_info[1]) in valid_recipe_ids:
                cur.execute(sql, (cooked_recipe_info[0], cooked_recipe_info[1], cooked_recipe_info[2], cooked_recipe_info[3], cooked_recipe_info[4]))
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
    cooked_recipes_uploader()
