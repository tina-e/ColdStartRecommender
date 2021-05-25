import pandas
from libreco.data import DatasetPure
from libreco.algorithms import UserCF

# ATTENTION: add in user_cf.py line 159: user = user_id

class UserCF_Recommender:
    def __init__(self):
        self.data = pandas.read_csv("data/reviewsV2.csv", sep=",", names=["user", "item", "label"])
        self.user_list = self.data['user'].tolist()

    def fit_algorithm(self):
        # data = pandas.read_pickle("dataframe.pkl")
        data, self.data_info = DatasetPure.build_trainset(self.data)
        # userCF is a "pure" model
        self.user_cf = UserCF(task="rating", data_info=self.data_info, k=20, sim_type="cosine")
        self.user_cf.fit(data)

    def add_user(self, user):
        if len(user.ratings_to_add_to_df) == 0:
            ratings_to_add = user.pseudo_ratings
        else:
            ratings_to_add = user.ratings_to_add_to_df
        user_data = []
        for recipe, rating in ratings_to_add.items():
            user_data.append([user.name, recipe, rating])
        user_df = pandas.DataFrame(user_data, columns=['user', 'item', 'label'])
        print(user_df)
        self.data = self.data.append(user_df.sample(int(user_df.size/6)))
        user.ratings_to_add_to_df.clear() # reset not-yet-added ratings
        self.fit_algorithm()

    def recommend_items(self, user, num_of_recommendations):
        recommended_items = self.user_cf.recommend_user(user, num_of_recommendations)
        recommended_items = [self.data_info.id2item.get(reco[0]) for reco in recommended_items]
        return recommended_items



