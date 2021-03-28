import pickle
import psycopg2 as psycopg2
import time

class ingredient:
    def __init__(self, IngredientId, IngredientName, Aisle, MeasurementUnit):
        self.id = IngredientId
        self.name = IngredientName
        self.aisle = Aisle
        self.measurementunit = MeasurementUnit

    def get_list(self):
        ingredient = []
        ingredient.append(self.id)
        ingredient.append(self.name)
        ingredient.append(self.aisle)
        ingredient.append(self.measurementunit)
        return ingredient


def ingredients_uploader():
    start = time.time()
    with open('data/ingr_map.pkl', 'rb') as f:
        data = pickle.load(f)
        ingredients_data = data.values.tolist()
        ingredients_list = []

        for ingredient_info in ingredients_data:
            name = str(ingredient_info[4])
            id = str(ingredient_info[6])
            #print("NAME: " + str(ingredient_info[4]) + " ID:" + str(ingredient_info[6]))
            new_ingredient = ingredient(id, name, None, None)

            have_ingr = False
            for item in ingredients_list:
                if id == item[0]:
                    have_ingr = True
                    break # if our name is equal to an ingredient we already have don't add this
                if name == item[1]:
                    have_ingr = True
                    break # if our id is equal to an ingredient we already have don't add this

            if have_ingr is False:
                ingredients_list.append(new_ingredient.get_list())


    sql = """INSERT INTO "Ingredients"("IngredientId", "IngredientName", "Aisle", "MeasurementUnit") VALUES(%s, %s, %s, %s)"""
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = conn = psycopg2.connect(host="reddwarf.cs.rit.edu", database="p320_03f", user="p320_03f",
                                       password="KFnU9gXi7JFk")
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        for ingredient_info in ingredients_list:
            cur.execute(sql, (ingredient_info[0], ingredient_info[1], ingredient_info[2], ingredient_info[3]))
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
    ingredients_uploader()
