import numpy as np
import matplotlib.pyplot as plt
import psycopg2 as psycopg2


def most_cooked_recipes():
    sql = """SELECT "CookedRecipes"."UserId", COUNT(*) c
    FROM "CookedRecipes"
    GROUP BY "UserId"
    ORDER BY c
    DESC"""

    conn = None
    try:
        # connect to the PostgreSQL database
        conn = conn = psycopg2.connect(host="reddwarf.cs.rit.edu", database="p320_03f", user="p320_03f",
                                       password="KFnU9gXi7JFk")
        # create a new cursor
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(sql)
        # commit the changes to the database
        results = cur.fetchall()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    # will put this data into some kind of graphic
    # for result in results:
    #     print("RecipeId: " + str(result[0]) + "  Number of times cooked: " + str(result[1]))

    freqData = np.array([x[1] for x in results])
    largest = max(freqData) + 1 # add 1 to account for exclusive

    bins = [1,2,5,10,20,50,100,10000]
    binlabels = ["1", "2-5", "6-10", "11-20", "21-50", "51-100", "101+"]
    h = np.histogram(freqData, bins=bins)
    plt.bar(binlabels, h[0])
    # plt.xticks(bins)

    plt.title("User Productivity")
    plt.xlabel("Amount of recipes cooked")
    plt.ylabel("Number of users")
    plt.show()

if __name__ == '__main__':
    most_cooked_recipes()
