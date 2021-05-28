import pandas
from libreco.data import DatasetPure
from libreco.algorithms import UserCF

import time
# ATTENTION: add in user_cf.py line 159: user = user_id


class UserCfRecommender:
    def __init__(self):
        self.data = self.get_ratings_from_file()
        self.user_list = self.data['user'].tolist()

    def fit_algorithm(self, num_recommendations):
        data, self.data_info = DatasetPure.build_trainset(self.data)
        # userCF is a "pure" model according to the library
        self.user_cf = UserCF(task="rating", data_info=self.data_info, k=num_recommendations, sim_type="cosine")
        self.user_cf.fit(data)

    def add_user(self, user, num_recommendations):
        if len(user.ratings_to_add_to_df) < 10:
            ratings_to_add = user.pseudo_ratings
            user_df = self.list_to_dataframe(ratings_to_add, user.name)
            print("Using " + str(int(user_df.size / 6)) + " pseudo ratings for standard recommender")
            self.data = self.get_ratings_from_file().append(user_df.sample(int(user_df.size / 6))).append(self.list_to_dataframe(user.ratings_to_add_to_df, user.name))
            self.fit_algorithm(num_recommendations)
        else:
            ratings_to_add = user.ratings_to_add_to_df
            user_df = self.list_to_dataframe(ratings_to_add, user.name)
            print("using real ratings for standard recommender")
            self.data = self.get_ratings_from_file().append(user_df) #reload 7 mio ratings - best way to remove pseudo ratings
            self.fit_algorithm(num_recommendations)

    def recommend_items(self, user, num_of_recommendations):
        if not user.has_chosen_categories() and len(user.ratings_to_add_to_df) == 0:
            recommended_items = self.user_cf.data_info.popular_items[:num_of_recommendations]
        else:
            recommended_items = self.user_cf.recommend_user(user.name, num_of_recommendations)
            recommended_items = [self.data_info.id2item.get(reco[0]) for reco in recommended_items]
        return recommended_items

    def get_ratings_from_file(self):
        return pandas.read_csv("data/reviews.csv", sep=",", names=["user", "item", "label"])

    def list_to_dataframe(self, list_of_ratings, username):
        user_data = []
        for recipe, rating in list_of_ratings.items():
            user_data.append([username, recipe, rating])
        user_df = pandas.DataFrame(user_data, columns=['user', 'item', 'label'])
        return user_df
