import recipe_parse
from fractions import Fraction
from string import punctuation
import random
import pprint

pp = pprint.PrettyPrinter(indent=1)

# ingredient_frame : quantity, unit, name, type
# steps_frame : text, text_split, method, ingredients, *tools, *time
 
unhealthy_stuff = ["dairy", "sugar", "salt", "sodium", "fat", "syrup", "cake", 
                      "sweet", "caramel", "cream", "cheese", "milk", "oil", "grease",
                       "lard", "butter", "chocolate", "msg"]
healthy_stuff = ["grain", "wheat", "fish", "corn", "rice", 
                    "pea", "carrot", "lettuce", "cabbage", "beet",
                    "bean", "vegetable", "veg", "oat", "kale", "nut", 
                    "seed", "green", "broccoli", "spinach", "sprout"]

def transform_to_healthy(url):
    ingredients_frame, step_frame, primary_method = recipe_parse.parse(url)
    #pp.pprint(ingredients_frame)
    #print(step_frame)
    ratio = 1.5
    for ing in ingredients_frame:
      for item in (unhealthy_stuff + healthy_stuff):
        if item in unhealthy_stuff and item in ing["name"] and ing["quantity"]: 
            new_amount = float(ing["quantity"])/ratio
            ing["quantity"] = str(new_amount)
        elif item in healthy_stuff and item in ing["name"] and ing["quantity"]:
            new_amount = float(ing["quantity"])*ratio
            ing["quantity"] = str(new_amount)
    return (ingredients_frame, step_frame, primary_method)

def transform_to_unhealthy(url):
    ingredients_frame, step_frame, primary_method = recipe_parse.parse(url)
    ratio = 1.5
    for ing in ingredients_frame:
      for item in (unhealthy_stuff + healthy_stuff):
        if item in unhealthy_stuff and item in ing["name"] and ing["quantity"]: 
            new_amount = float(ing["quantity"])*ratio
            ing["quantity"] = str(new_amount)
        elif item in healthy_stuff and item in ing["name"] and ing["quantity"]:
            new_amount = float(ing["quantity"])/ratio
            ing["quantity"] = str(new_amount)
    return (ingredients_frame, step_frame, primary_method) 

#------

def transform_to_vegetarian(url):
    #Transforms form non vegetarian to vegetarian
    meat_options = ["ground beef","cubed beef chuck roast","can beef broth","bacon","salmon steaks","shrimp","eggs","chicken broth"]
    # veg_alternates = ["tofu", "soy", "tempeh", "seitan", "lupin", "spelt", "oat flakes", "black beans", "pea"]
    alternates = {"ground beef":"tofu","cubed beef chuck roast":"soy", "can beef broth":"tempeh", "bacon":"seitan", "salmon steaks":"lupin", "shrimp":"spelt","eggs":"black beans","chicken broth": "pea"}
    conversion_ratio = [0.25,0.3,0.2,0.1,0.4,0.35,0.5,0.3]
    ingredients_frame, steps_frame, primary_method = recipe_parse.parse(url)
    new_ingredients = []
    for ing in ingredients_frame:
        
        if ing["name"] in meat_options:
            
            new_ingredients.append({"quantity": float(ing["quantity"]) * random.choice(conversion_ratio), "unit": ing["unit"], "name": alternates[ing["name"]], "type" : "vegetarian"})
        else:
            new_ingredients.append({"quantity": ing["quantity"], "unit": ing["unit"], "name": ing["name"], "type" : ing["type"]})

    for step in steps_frame:
        for i in meat_options:
            if i in step["text"]:
                step["text"] = step["text"].replace(i,alternates[i])
        step["text_split"] = step["text"].strip(punctuation).split()

    return (new_ingredients,steps_frame,primary_method)


def transform_to_non_vegetarian(url):
    #Transforms form vegetarian to non-vegetarian
    veg_options = ["tofu", "quinoa","soybean","peas"]
    # meat_options = ["ground beef","cubed beef chuck roast","can beef broth","bacon","salmon steaks","shrimp","eggs","chicken broth"]
    # veg_alternates = ["tofu", "soy", "tempeh", "seitan", "lupin", "spelt", "oat flakes", "black beans", "pea"]
    alternates = {"tofu":"ground beef","quinoa":"shredded chicken","soybean":"bacon","peas":"salmon"}
    conversion_ratio = [0.25,0.3,0.2,0.1]
    ingredients_frame, steps_frame, primary_method = recipe_parse.parse(url)
    new_ingredients = []
    converted = 0
    for ing in ingredients_frame:
        for i in veg_options:
            if i in ing["name"]:
                # new_ingredients.append({"quantity": float(ing["quantity"]) * random.choice(conversion_ratio), "unit": ing["unit"], "name": alternates[i], "type" : "meat"})
                ing["quantity"] = float(ing["quantity"]) * random.choice(conversion_ratio)
                ing["name"] = alternates[i]
                ing["type"] = "meat"
                converted = 1


    for step in steps_frame:
        for i in veg_options:
            if i in step["text"]:
                step["text"] = step["text"].replace(i,alternates[i])
        step["text_split"] = step["text"].strip(punctuation).split()

    if converted == 0:
        ingredients_frame.append({"quantity": 0.3, "unit": "ounces", "name": "shredded chicken", "type" : "meat"})
        new_step = {"text":"     Final Step: Add 0.3 ounces of shredded chicken.","text_split":"","method":"shred","ingredients":"shredded chicken"}
        steps_frame.append(new_step)

    return (ingredients_frame, steps_frame, primary_method)

        
#------

def transform_cuisine(url):
    # Transforms to Chinese cuisine by replacing all sauces with soy sauce
    ingredients_frame, steps_frame, primary_method = recipe_parse.parse(url)

    for ingredient in ingredients_frame:
        if "sauce" in ingredient["name"]:
            ingredient["name"] = "soy sauce"

    for step in steps_frame:
        step_text = step["text"].translate(str.maketrans('', '', punctuation)).split()
        for i in range (len(step["text_split"])):
            if step_text[i] == "sauce":
                step["text_split"][i - 1] = "soy"
                step["text"] = " ".join(step["text_split"])

    return (ingredients_frame, steps_frame, primary_method)
    

#-----

def double_amount(url):
    ingredients_frame, steps_frame, primary_method = recipe_parse.parse(url)
    #print(ingredients_frame)
    
    for ingredient in ingredients_frame:
        ingredient["quantity"] = str(Fraction(float(ingredient["quantity"]) * 2))
        
    return (ingredients_frame, steps_frame, primary_method)

def half_amount(url):
    ingredients_frame, steps_frame, primary_method = recipe_parse.parse(url)
    
    for ingredient in ingredients_frame:
        ingredient["quantity"] = str(Fraction(float(ingredient["quantity"]) * 1/2))

    return (ingredients_frame, steps_frame, primary_method)

#-----

def transform_method(url, new_method):
    # Changes the primary cooking method
    ingredients_frame, steps_frame, primary_method = recipe_parse.parse(url)
    
    for step in steps_frame:
        if step["method"] == primary_method:
            step["method"] = new_method
            step["text_split"][2] = new_method.capitalize()
            step["text"] = " ".join(step["text_split"])

    return (ingredients_frame, steps_frame, new_method)


def main():
    url = input("Input the recipe URL: ")
    transformations = {"To vegetarian": transform_to_vegetarian, "To non-vegetarian": transform_to_non_vegetarian,
        "To healthy": transform_to_healthy, "To unhealthy": transform_to_unhealthy,
        "To Chinese cuisine": transform_cuisine, "Double amount": double_amount,
        "Half amount": half_amount, "Change cooking method": transform_method}
    print("TRANSFORMATION OPTIONS:")
    for transformation in transformations:
        print(transformation)
    transform = input("Input the type of transformation: ")
    if transform in transformations:
        if transformations[transform] == transform_method:
            method = input("Input the new cooking method: ")
            result_ingredients, result_steps, result_method = transform_method(url, method)
        else:
            result_ingredients, result_steps, result_method = transformations[transform](url)
    
    # Pretty print recipe
    print("\nIngredients:")
    for i in result_ingredients:
        print(i['quantity'], i['unit']+'s', "of", i['name'])
    print("\nSteps:")
    for i in result_steps:
        print("\n", i['text'])
    print("\nCooking method: ", result_method.capitalize())
   
if __name__ == '__main__':
    main()
    #transform_cuisine("https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/")
