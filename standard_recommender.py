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
        # data = pandas.read_pickle("dataframe.pkl")
        data, self.data_info = DatasetPure.build_trainset(self.data)
        # userCF is a "pure" model
        self.user_cf = UserCF(task="rating", data_info=self.data_info, k=num_recommendations, sim_type="cosine")
        self.user_cf.fit(data)

    def add_user(self, user, num_recommendations):
        if len(user.ratings_to_add_to_df) < 10:
            ratings_to_add = user.pseudo_ratings
            user_df = self.list_to_dataframe(ratings_to_add, user.name)
            print("Using " + str(int(user_df.size / 6)) + " pseudo ratings for standard recommender")
            self.data = self.data.append(user_df.sample(int(user_df.size / 6)))
            self.fit_algorithm(num_recommendations)
        else:
            ratings_to_add = user.ratings_to_add_to_df
            user_df = self.list_to_dataframe(ratings_to_add, user.name)
            print("using real ratings for standard recommender")
            self.data = self.get_ratings_from_file().append(user_df) #reload 7 mio ratings (means removal of pseudo ratings
            self.fit_algorithm(num_recommendations)

        #print("es wird die folgende Anzahl ratings an die 7 mio ratings angehangen")
        #print(len(ratings_to_add))

        #user_data = []
        #for recipe, rating in ratings_to_add.items():
        #    user_data.append([user.name, recipe, rating])
        #user_df = pandas.DataFrame(user_data, columns=['user', 'item', 'label'])
        #print(user_df)

        #user_df = self.list_to_dataframe(ratings_to_add, user.name)
        #if (len(user.ratings_to_add_to_df) < 10):
        #    print("Using " + str(int(user_df.size / 6)) + " pseudo ratings for standard recommender")
        #    user.ratings_to_add_to_df.clear()  # reset not-yet-added ratings
        #self.data = self.data.append(user_df.sample(int(user_df.size / 6)))
        #self.fit_algorithm(num_recommendations)

    def recommend_items(self, user, num_of_recommendations):
        recommended_items = self.user_cf.recommend_user(user, num_of_recommendations)
        recommended_items = [self.data_info.id2item.get(reco[0]) for reco in recommended_items]
        return recommended_items

    def get_ratings_from_file(self):
        start_time = time.time()
        ret = pandas.read_csv("data/reviewsV2.csv", sep=",", names=["user", "item", "label"])
        print("--- %s seconds ---" % (time.time() - start_time))
        return ret
        #return pandas.read_csv("data/reviewsV2.csv", sep=",", names=["user", "item", "label"])

    def list_to_dataframe(self, list_of_ratings, username):
        user_data = []
        for recipe, rating in list_of_ratings.items():
            user_data.append([username, recipe, rating])
        user_df = pandas.DataFrame(user_data, columns=['user', 'item', 'label'])
        return user_df
