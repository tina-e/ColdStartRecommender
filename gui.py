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
        self.rating_combobox.hide()

        self.category_selected_counter = 0
        self.max_category_selected_counter = 2

        self.next_button.clicked.connect(self.switch_to_next_stack)

        self.new_user = None
        self.button = None
        for button in self.buttonGroup.buttons():
            button.clicked.connect(lambda _, b=button: self.on_type_clicked(b))

        self.old_recommendations_model = QStringListModel()
        self.new_recommendations_model = QStringListModel()
        self.old_view.itemSelectionChanged.connect(self.update_ratings)
        self.new_view.itemSelectionChanged.connect(self.update_ratings)


    def switch_to_next_stack(self):
        name_current_stack = self.stacked_widget.currentWidget().objectName()
        num_current_stack = self.stacked_widget.currentIndex()
        # last page before switching to recommendation-page
        if name_current_stack == 'unwanted_page':
            self.new_user.has_lactose_intolerance = (self.lactose_checkbox.checkState() == 2)
            self.new_user.has_gluten_intolerance = (self.gluten_checkbox.checkState() == 2)
            # TODO: unwanted ingredients
            # self.new_user.unwanted_ingredients =
            self.stacked_widget.setCurrentIndex(num_current_stack + 1)
            self.rating_combobox.show()
            self.label_instructions.setText("Zum Bewerten: Bewertung wählen und Rezept anklicken")
            self.display_recommendations()

        # is on recommendation-page -> update recommendations
        elif name_current_stack == 'recommendations_page':
            self.display_recommendations()

        # switch any other page
        elif self.is_valid_input(name_current_stack):
            if name_current_stack == 'start_page':
                self.label_instructions.setText(f"Wähle bis zu {self.max_category_selected_counter} Kategorien, die dir am meisten zusagen.")
            elif name_current_stack == 'category_page_4':
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


    def is_valid_input(self, stack_name):
        # start page
        if stack_name == 'start_page':
            if not self.input_username.text().strip() or not self.input_budget or not self.input_level:
                self.label_error.setText("Nicht alle Felder ausgefüllt.")
                return False
            if self.input_username.text() in self.system.user_list:
                self.label_error.setText("Username belegt.")
                return False
            if self.input_budget.currentText() == 'kleines Budget': budget = 1
            elif self.input_budget.currentText() == 'mittleres Budget': budget = 3
            elif self.input_budget.currentText() == 'höheres Budget': budget = 5
            self.new_user = User(self.input_username.text(), self.input_level.currentText(), budget)

        # type selection pages
        elif 'category' in stack_name:
            if not (0 < self.category_selected_counter <= self.max_category_selected_counter):
                self.label_error.setText(f"Wähle mind. 1 und max. {self.max_category_selected_counter} aus.")
                return False
            self.category_selected_counter = 0

        return True


    def display_recommendations(self):
        self.next_button.setText("Loading Recommendations...")
        self.new_user.pseudo_ratings = recipe.get_pseudo_ratings(self.new_user)

        # calc recommendations
        self.system.add_user(self.new_user)
        recommendations = self.system.recommend_items(self.new_user.name, 20)

        print(recommendations)

        # display recommendations
        olds, news = self.split_recommendations(recommendations)
        #self.old_recommendations_model.setStringList([el.split("/")[-1].split(".")[0].replace("-", " ") for el in olds])
        #self.new_recommendations_model.setStringList([el.split("/")[-1].split(".")[0].replace("-", " ") for el in news])
        self.old_recommendations_model.setStringList(olds)
        self.new_recommendations_model.setStringList(news)
        self.old_view.setModel(self.old_recommendations_model)
        self.new_view.setModel(self.new_recommendations_model)

        # TODO: prototypisch erlauben, vorgeschlagenes Rezept zu bewerten und die Recommendations updaten sich
        self.next_button.setText("Update Recommendations")

    def update_ratings(self):
        view = self.old_view.selectedItems()
        if len(self.new_view.selectedItems()) != 0: view = self.new_view.selectedItems()
        selected_item = view.selectedItems()
        selected_rating = self.rating_combobox.currentText().split(" ")[0]
        self.new_user.ratings[selected_item] = selected_rating

    def split_recommendations(self, recommendations):
        recipe_types = ["desserts_overlap", "main_dish_overlap", "side_dish_overlap",
                        "meat_and_poultry_overlap", "soups_stews_and_chili_overlap", "cakes_overlap",
                        "breakfast_and_brunch_overlap", "salad_overlap", "pasta_and_noodels_overlap",
                        "appetizers_and_snacks_overlap", "roasts_overlap", "casseroles_overlap",
                        "low_calorie_overlap", "healthy_overlap", "veggie_overlap", "stir_fry_overlap",
                        "asian_style_overlap", "pizza_overlap", "deep_fried_overlap", "italy_and_italian_style_overlap",
                        "candy_overlap", "seafood_overlap", "cookies_overlap", "everyday_cooking_overlap",
                        "dips_and_spreads_overlap", "drinks_overlap", "spirits_overlap"]
        olds = []
        news = []
        for recommendation in recommendations:
            recipe_categories = recipe.get_categories_by_href(recommendation)
            user_categories = self.new_user.get_category_indices()
            if any(category in recipe_categories for category in user_categories):
                print("adding old: ")
                for element in recipe_categories:
                    print(recipe_types[element])
                olds.append(recommendation)
            else:
                news.append(recommendation)
        return olds, news


if __name__ == "__main__":
    app = QApplication([])
    window = RecommenderInterface()
    window.show()
    sys.exit(app.exec_())
