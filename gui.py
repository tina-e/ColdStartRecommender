import sys
import math


from PyQt5 import uic, QtSvg, QtGui
from PyQt5.QtCore import QRect, Qt, QStringListModel, QItemSelectionModel
from PyQt5.Qt import QButtonGroup
from PyQt5.QtWidgets import *
import PyQt5

from standard_recommender import UserCfRecommender
from user import User
import recipe


class RecommenderInterface(QMainWindow):
    def __init__(self):
        self.system = UserCfRecommender()
        QMainWindow.__init__(self)
        uic.loadUi("recsys.ui", self)
        self.rating_combobox.hide()
        self.search_field_prototype.hide()

        self.category_selected_counter = 0
        self.max_category_selected_counter = 2

        self.next_button.clicked.connect(self.switch_to_next_stack)

        self.new_user = None
        self.button = None
        for button in self.buttonGroup.buttons():
            button.clicked.connect(lambda _, b=button: self.on_type_clicked(b))

        self.rec_display_dict = {}
        self.old_model = QtGui.QStandardItemModel()
        self.new_model = QtGui.QStandardItemModel()
        self.old_view.clicked.connect(self.on_old_rated)
        self.new_view.clicked.connect(self.on_new_rated)

        self.num_recommendations = 30

    def switch_to_next_stack(self):
        name_current_stack = self.stacked_widget.currentWidget().objectName()
        num_current_stack = self.stacked_widget.currentIndex()
        # last page before switching to recommendation-page
        if name_current_stack == 'unwanted_page':
            self.new_user.has_lactose_intolerance = (self.lactose_checkbox.checkState() == 2)
            self.new_user.has_gluten_intolerance = (self.gluten_checkbox.checkState() == 2)
            self.stacked_widget.setCurrentIndex(num_current_stack + 1)
            self.rating_combobox.show()
            self.search_field_prototype.show()
            self.label_instructions.setText("Zum Bewerten: Bewertung wählen und Rezept anklicken")
            self.label_instructions.show()
            self.display_recommendations()

        # is on recommendation-page -> update recommendations
        elif name_current_stack == 'recommendations_page':
            self.display_recommendations()

        # switch any other page
        elif self.is_valid_input(name_current_stack):
            if name_current_stack == 'start_page':
                self.label_instructions.setText(f"Wähle bis zu {self.max_category_selected_counter} Kategorien, die dir zusagen.")
            elif name_current_stack == 'category_page_2':
                self.label_instructions.hide()
            self.label_error.setText("")
            self.category_selected_counter = 0
            self.stacked_widget.setCurrentIndex(num_current_stack + 1)

    def on_type_clicked(self, clicked_button):
        clicked_types = clicked_button.objectName().split('0')
        for clicked_type in clicked_types:
            if clicked_type in self.new_user.category_list:
                self.new_user.category_list.remove(clicked_type)
                clicked_button.setStyleSheet('')
                self.category_selected_counter = self.category_selected_counter - 1
            elif self.category_selected_counter < self.max_category_selected_counter:
                self.new_user.category_list.append(clicked_type)
                clicked_button.setStyleSheet('background-color: lightblue;')
                self.category_selected_counter = self.category_selected_counter + 1

    def is_valid_input(self, stack_name):
        # start page
        if stack_name == 'start_page':
            if not self.input_username.text().strip() or not self.input_budget or not self.input_level:
                self.label_error.setText("Bitte fülle alle Felder aus.")
                return False
            if self.input_username.text() in self.system.user_list:
                self.label_error.setText("Username belegt.")
                return False
            if self.input_budget.currentText() == 'kleines Budget': budget = 1
            elif self.input_budget.currentText() == 'mittleres Budget': budget = 3
            elif self.input_budget.currentText() == 'höheres Budget': budget = 5
            self.new_user = User(self.input_username.text(), self.input_level.currentText(), budget)
        return True

    def display_recommendations(self):
        print("user has selected the following categories: " + str(self.new_user.category_list))

        self.next_button.setText("Vorschläge werden geladen...")
        self.old_model.clear()
        self.new_model.clear()

        if len(self.new_user.pseudo_ratings) == 0:
            self.new_user.pseudo_ratings = recipe.get_pseudo_ratings(self.new_user)
        self.system.add_user(self.new_user, self.num_recommendations)
        recommendations = self.system.recommend_items(self.new_user.name, self.num_recommendations)
        recommendations = recipe.modify_recommendations(recommendations, self.new_user.get_dislikes())

        for recommendation in recommendations:
            model_params = (self.old_model, "o") if self.is_old(recommendation) else (self.new_model, "n")
            index = len(model_params[0].findItems("", flags=Qt.MatchContains))
            self.rec_display_dict[(model_params[1], index)] = recommendation
            rec_string = recommendation.split("/")[-1].split(".")[0].replace("-", " ")
            item = QtGui.QStandardItem(rec_string)
            item.setSelectable(True)
            model_params[0].appendRow(item)

        self.old_view.setModel(self.old_model)
        self.new_view.setModel(self.new_model)
        self.next_button.setText("Vorschläge neu laden")

    def on_old_rated(self, index):
        print(self.rec_display_dict)
        item_view = self.old_model.item(index.row())
        item_view.setBackground(QtGui.QColor('yellow'))
        rated_item = self.rec_display_dict.get(('o', index.row()))
        selected_rating = self.rating_combobox.currentText().split(" ")[0]
        self.new_user.ratings_to_add_to_df[rated_item] = int(selected_rating)
        print("added: ")
        print(self.new_user.ratings_to_add_to_df[rated_item])

    def on_new_rated(self, index):
        item_view = self.new_model.item(index.row())
        item_view.setBackground(QtGui.QColor('yellow'))
        rated_item = self.rec_display_dict.get(('n', index.row()))
        selected_rating = self.rating_combobox.currentText().split(" ")[0]
        self.new_user.ratings_to_add_to_df[rated_item] = int(selected_rating)
        print("added: ")
        print(self.new_user.ratings_to_add_to_df[rated_item])

    def is_old(self, recommendation):
        recipe_categories = recipe.get_categories_by_href(recommendation)
        user_categories = self.new_user.get_category_indices()
        return any(category in recipe_categories for category in user_categories)


if __name__ == "__main__":
    app = QApplication([])
    window = RecommenderInterface()
    window.show()
    sys.exit(app.exec_())
