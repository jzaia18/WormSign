import pickle
import pandas


def ingredients_uploader():
    with open('data/ingr_map.pkl', 'rb') as f:
        data = pickle.load(f)
        print(data)


if __name__ == '__main__':
    ingredients_uploader()
