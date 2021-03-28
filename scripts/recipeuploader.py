import csv
import random
import psycopg2 as psycopg2
import time
from utils.config import config


class recipe:
    def __init__(self, RecipeId, RecipeName, Description, Servings, CookTime, Difficulty, Steps, UserId, CreationDate):
        self.id = RecipeId
        self.name = RecipeName
        self.description = Description
        self.servings = Servings
        self.cooktime = CookTime
        self.diffculty = Difficulty
        self.steps = Steps
        self.userid = UserId
        self.creationdate = CreationDate

    def getList(self):
        recipe = []
        recipe.append(self.id); recipe.append(self.name); recipe.append(self.description)
        recipe.append(self.servings); recipe.append(self.cooktime); recipe.append(self.diffculty)
        recipe.append(self.steps); recipe.append(self.userid); recipe.append(self.creationdate)
        return recipe

def recipe_uploader():
    start = time.time()
    recipeList = []
    difficultiesList = ['Easy', 'Easy-Medium', 'Medium', 'Medium-Hard', 'Hard']
    servingsList = [1, 2, 3, 4, 5, 6, 7, 8]
    count = 0
    with open('data/RAW_recipes.csv', encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # skip first row
        next(csv_reader)
        for row in csv_reader:
            count += 1
            if count <= 5000: # this means start at recipe #5000
                continue
            #recipeList.append(recipe(row[1], row[0], row[9], random.choice(servingsList), row[2], random.choice(difficultiesList), row[7], row[3], row[4]))
            newrecipe = recipe(row[1], row[0], row[9][:1000], random.choice(servingsList), row[2], random.choice(difficultiesList), row[8][:1000],
                   row[3], row[4])
            recipeList.append(newrecipe.getList())
            if count == 15000: # this means end at recipe #15000
                break

    """ insert multiple vendors into the vendors table  """
    sql = """INSERT INTO "Recipes"("RecipeId", "RecipeName", "Description", "Servings", "CookTime", "Difficulty", "Steps", "UserId", "CreationDate") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = conn = psycopg2.connect(host="reddwarf.cs.rit.edu", database="p320_03f", user="p320_03f", password="KFnU9gXi7JFk")
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        for recipeinfo in recipeList:
            cur.execute(sql, (recipeinfo[0], recipeinfo[1], recipeinfo[2], recipeinfo[3], recipeinfo[4], recipeinfo[5], recipeinfo[6], recipeinfo[7], recipeinfo[8]))
        #cur.executemany(sql, (recipeList[0], recipeList[1], recipeList[2], recipeList[3], recipeList[4], recipeList[5], recipeList[6], recipeList[7], recipeList[8]))
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
    recipe_uploader()
