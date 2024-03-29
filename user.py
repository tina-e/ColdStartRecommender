class User:
    # user model - stores any relevant information about him
    def __init__(self, name, budget, level):
        self.name = name
        self.level = level
        self.budget = budget
        self.category_list = []
        self.unwanted_ingredients = []
        self.has_lactose_intolerance = False
        self.has_gluten_intolerance = False
        self.pseudo_ratings = {}
        self.ratings_to_add_to_df = {}

    def get_category_indices(self):
        recipe_types = ["desserts_overlap", "main_dish_overlap", "side_dish_overlap",
                        "meat_and_poultry_overlap", "soups_stews_and_chili_overlap", "cakes_overlap",
                        "breakfast_and_brunch_overlap", "salad_overlap", "pasta_and_noodels_overlap",
                        "appetizers_and_snacks_overlap", "roasts_overlap", "casseroles_overlap",
                        "low_calorie_overlap", "healthy_overlap", "veggie_overlap", "stir_fry_overlap",
                        "asian_style_overlap", "pizza_overlap", "deep_fried_overlap", "italy_and_italian_style_overlap",
                        "candy_overlap", "seafood_overlap", "cookies_overlap", "everyday_cooking_overlap",
                        "dips_and_spreads_overlap", "drinks_overlap", "spirits_overlap"]
        return [recipe_types.index(category) for category in self.category_list]

    def get_dislikes(self):
        return [self.has_lactose_intolerance, self.has_gluten_intolerance, self.unwanted_ingredients]

    def has_chosen_categories(self):
        return len(self.category_list) != 0
