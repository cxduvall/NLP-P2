from bs4 import BeautifulSoup
import requests

common_cooking_methods = ["bake", "fry", "sauté", "broil", "boil", "poach", "grill", "steam"]
common_other_methods = ["chop", "grate", "stir", "shake", "mince", "crush", "squeeze"]

page = requests.get("https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/")
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())

ingredients = soup.find_all("span", class_="ingredients-item-name")
ingredients = [ingredient.get_text() for ingredient in ingredients]
#for i, ingredient in enumerate(ingredients):

# Parse ingredient info using the data directly from website
# (using no NLP here; this isn't viewable by the user)
ingredients_data = soup.find_all("input", class_="checkbox-list-input")
ingredient_frame_lst = []
for datum in ingredients_data:
    print(datum)
    if datum.attrs.get("value") == "":
        continue
    quantity = datum.attrs.get("data-init-quantity", None)
    unit = datum.attrs.get("data-unit", None)
    ingredient = datum.attrs.get("data-ingredient", None)
    ingredient_frame_lst.append({"quantity": quantity, "unit": unit, "name": ingredient})

print(ingredients)
print(type(ingredients[0]))
print("\n", ingredient_frame_lst)

steps_data = soup.find_all("li", class_="subcontainer instructions-section-item")
steps_frame_lst = [{"text": step.text} for step in steps_data]
# extract info for each step
for i, step in enumerate(steps_frame_lst):
    step["text_split"] = step["text"].strip().split(" ")
    step["method"]= step["text_split"][4]
print("\n", steps_frame_lst)