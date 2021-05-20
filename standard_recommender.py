import pandas
from libreco.data import DatasetPure
from libreco.algorithms import UserCF

# ATTENTION: add in user_cf.py line 159: user = user_id

class UserCF_Recommender:
    def __init__(self):
        self.data = pandas.read_csv("data/reviewsV2.csv", sep=",", names=["user", "item", "label"])
        # self.data.to_pickle("dataframe.pkl")
        # self.fit_algorithm()
        self.user_list = self.data['user'].tolist()

    def fit_algorithm(self):
        # data = pandas.read_pickle("dataframe.pkl")
        data, self.data_info = DatasetPure.build_trainset(self.data)
        self.user_cf = UserCF(task="rating", data_info=self.data_info)
        self.user_cf.fit(data)

    # TODO: fix "unknown user"
    def add_user(self, user):
        print(user.pseudo_ratings)
        # user_df = pandas.DataFrame(columns=["user", "item", "label"])
        user_data = []
        for recipe, rating in user.pseudo_ratings.items():
            user_data.append([user.name, recipe, rating])
            # user_df = user_df.append([user.name, recipe, rating], columns=["user", "item", "label"])
        user_df = pandas.DataFrame(user_data, columns=['user', 'item', 'label'])
        print(user_df)
        self.data = self.data.append(user_df)
        self.fit_algorithm()

    def recommend_items(self, user, num_of_recommendations):
        recommended_items = self.user_cf.recommend_user(user, num_of_recommendations)
        recommended_items = [self.data_info.id2item.get(reco[0]) for reco in recommended_items]
        return recommended_items

    # TODO: Delete unwanted recommendations (Allergien, ...)
    # def update_recommendations(self, unwanted_features):


#k = 10
#username_to_recommend_0 = "Angi54"
#username_to_recommend_1 = "schmifi09"
#username_to_recommend_2 = "Jacky65"

#system = UserCF_Recommender()
#print(system.recommend_items(username_to_recommend_0, k))
#print(system.recommend_items(username_to_recommend_1, k))
#print(system.recommend_items(username_to_recommend_2, k))




