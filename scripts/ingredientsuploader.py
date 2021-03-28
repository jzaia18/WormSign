import pickle


class ingredient:
    def __init__(self, IngredientId, IngredientName, Aisle, MeasurementUnit):
        self.id = IngredientId
        self.name = IngredientName
        self.aisle = Aisle
        self.measurementunit = MeasurementUnit

    def getList(self):
        ingredient = []
        ingredient.append(self.id);
        ingredient.append(self.username);
        ingredient.append(self.aisle)
        ingredient.append(self.measurementunit)
        return ingredient


def ingredients_uploader():
    with open('data/ingr_map.pkl', 'rb') as f:
        data = pickle.load(f)
        print(data)
        test = data.values.tolist()

        for t in test:
            print(t)


if __name__ == '__main__':
    ingredients_uploader()
