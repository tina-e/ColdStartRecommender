import sys
import math

from PyQt5 import uic, QtSvg, QtGui
from PyQt5.QtCore import QRect, Qt, QStringListModel
from PyQt5.Qt import QButtonGroup
from PyQt5.QtWidgets import *

from standard_recommender import UserCF_Recommender
from user import User
import recipe

# TODO: Kategorien sinnvoll aufteilen
# TODO: Länder-Page löschen
# TODO: Auswahl für ungewollte Zutaten

class RecommenderInterface(QMainWindow):
    def __init__(self):
        self.system = UserCF_Recommender()
        QMainWindow.__init__(self)
        uic.loadUi("recsys.ui", self)

        self.category_selected_counter = 0
        self.max_category_selected_counter = 2

        self.next_button.clicked.connect(self.switch_to_next_stack)

        self.new_user = None
        self.button = None
        for button in self.buttonGroup.buttons():
            print(type(button))
            button.clicked.connect(lambda _, b=button: self.on_type_clicked(b))

        self.old_recommendations_model = QStringListModel()
        self.new_recommendations_model = QStringListModel()


    def switch_to_next_stack(self):
        num_current_stack = self.stacked_widget.currentIndex()
        # last page before switching to recommendation-page
        if num_current_stack == 7:
            self.new_user.has_lactose_intolerance = (self.lactose_checkbox.checkState() == Qt.CheckState.Checked)
            self.new_user.has_gluten_intolerance = (self.gluten_checkbox.checkState() == Qt.CheckState.Checked)
            # TODO: unwanted ingredients
            # self.new_user.unwanted_ingredients =
            self.stacked_widget.setCurrentIndex(num_current_stack + 1)
            self.display_recommendations()

        # is on recommendation-page -> update recommendations
        elif num_current_stack == 8:
            self.display_recommendations()

        # switch any other page
        elif self.is_valid_input(num_current_stack):
            if num_current_stack == 0:
                self.label_instructions.setText(f"Wähle bis zu {self.max_category_selected_counter} Kategorien, die dir am meisten zusagen.")
            elif num_current_stack == 5:
                self.label_instructions.hide()
            self.label_error.setText("")
            self.stacked_widget.setCurrentIndex(num_current_stack + 1)


    def on_type_clicked(self, clicked_button):
        clicked_type = clicked_button.objectName()
        if clicked_type in self.new_user.category_list:
            self.new_user.category_list.remove(clicked_type)
            clicked_button.setStyleSheet('')
            self.category_selected_counter = self.category_selected_counter - 1
        elif self.category_selected_counter < self.max_category_selected_counter:
            self.new_user.category_list.append(clicked_type)
            clicked_button.setStyleSheet('background-color: blue;')
            self.category_selected_counter = self.category_selected_counter + 1


    def is_valid_input(self, stack_num):
        # start page
        if stack_num == 0:
            if not self.input_username.text().strip() or not self.input_budget or not self.input_level:
                self.label_error.setText("Nicht alle Felder ausgefüllt.")
                return False
            if self.input_username.text() in self.system.user_list:
                self.label_error.setText("Username belegt.")
                return False
            self.new_user = User(self.input_username.text())

        # type selection pages
        elif stack_num in range(1, 6):
            if not (0 < self.category_selected_counter <= self.max_category_selected_counter):
                self.label_error.setText(f"Wähle mind. 1 und max. {self.max_category_selected_counter} aus.")
                return False
            self.category_selected_counter = 0

        return True


    def display_recommendations(self):
        self.next_button.setText("Loading Recommendations...")

        # TODO: find similar users
        #self.new_user.get_pseudo_ratings(["candy_overlap", "seafood_overlap"])
        self.new_user.pseudo_ratings = self.get_pseudo_ratings(self.new_user.get_category_indices())

        # calc recommendations
        self.system.add_user(self.new_user)
        recommendations = self.system.recommend_items(self.new_user.name, 10)

        # display recommendations TODO: hübsch darstellen (optional)
        olds, news = self.split_recommendations(recommendations)
        self.old_recommendations_model.setStringList(olds)
        self.new_recommendations_model.setStringList(news)
        self.old_view.setModel(self.old_recommendations_model)
        self.new_view.setModel(self.new_recommendations_model)

        # TODO: prototypisch erlauben, vorgeschlagenes Rezept zu bewerten und die Recommendations updaten sich
        self.next_button.setText("Update Recommendations")


    def split_recommendations(self, recommendations):
        olds = []
        news = []
        for recommendation in recommendations:
            for category in self.new_user.category_list:
                if recipe.is_recipe_in_category(recommendation, category):
                    olds.append(recommendation)
                else:
                    news.append(recommendation)
        return olds, news

    def get_similar_users(self, list_of_categories):
        return_users = []
        user_file = open("./data/users.csv", encoding="utf-8")
        for x in range(16187):  # 16187
            line = user_file.readline()[0:-1].split(",")
            if int(line[1]) in list_of_categories:
                return_users.append(line[0])
        return return_users

    def get_recipes_from_users(self, similar_pref_users):
        recipes = {}
        user_file = open("./data/reviewsV2.csv", encoding="utf-8")
        for x in range(7796004):  # 7796004
            line = user_file.readline()[0:-1].split(",")
            if line[0] in similar_pref_users:
                recipes[line[1]] = 5
        return recipes

    #TODO
    def modify_pseudo_ratings(self, recipe_list):
        print("?")
        return recipe_list

    def get_pseudo_ratings(self, overlap_categories):
        similar_users = self.get_similar_users(overlap_categories)
        print("number of similar users: " + str(len(similar_users)))
        pseudo_ratings = self.get_recipes_from_users(similar_users)
        print(pseudo_ratings)
        pseudo_ratings = self.modify_pseudo_ratings(pseudo_ratings)
        # print("ratings after modification: " + pseudo_ratings)
        return pseudo_ratings


if __name__ == "__main__":
    app = QApplication([])
    window = RecommenderInterface()
    window.show()
    sys.exit(app.exec_())


