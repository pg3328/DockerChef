from flask import Flask, request, render_template
import requests
import xml.etree.ElementTree as ET
from tf_idf import TF_IDF
import json

API_KEY = "rcaGhp0Af80tcX6DHEEvDbT0XNEiV3YZqi2fqO5YDfCAtOa001OS0VkJ"
IMAGE_URL = 'https://api.pexels.com/v1/search'
app = Flask(__name__)
model = TF_IDF()
model.pre_processing()

@app.route("/getdata", methods=['POST'])
def get_recipe_details():
    id = int(request.form['id'])
    print("ID:::", id)
    steps, ingredients = model.extract_detailed_info(id)
    result = {}
    print(ingredients)
    result['ingredients'] = ingredients
    result['steps'] = []
    for i in steps.values:
            i=i[1:-2]
            # i is a string
            for word in (i.strip(",").strip(", ").split("'")):
                if word == ", ":
                    continue
                print(word)
                result['steps'].append(word)

    print("---------------")
    print("WORKED")
    return render_template("recipe_detail.html", result=result)

@app.route("/recipe")
def recipe(query):
    query = query.split(",")
    
    model.get_top_3(query)
    result = {}
    titles, descriptions, ids, minutes = model.extract_description()
    for idx, title in enumerate(titles):
        result["title_"+str(idx)] = title
    idx = 0
    for description in descriptions:
        print(description)
        result["description_"+str(idx)] = description
        print("---------------")
        idx += 1
        
    for idx, time in enumerate(minutes):
        result["time_"+str(idx)] = time

    recipe_ingredients = []
    idx = 0
    for id in ids:
        print(id)
        result["id_"+str(idx)] = id
        idx += 1
        steps, ingredients = model.extract_detailed_info(id)
        
        print(ingredients)
        recipe_ingredients.append(ingredients)
        for i in steps.values:
            i=i[1:-2]
            # i is a string
            for word in (i.strip(",").strip(", ").split("'")):
                if word == ", ":
                    continue
                print(word)

        print("---------------")

    ## image generation TODO as improvement
    # idx = 0
    # for item in recipe_ingredients:
    #     params = {'query': item, 'per_page': 1}
    #     headers = {'Authorization': API_KEY}
    #     response = requests.get(IMAGE_URL, params=params, headers=headers)
    #     if response.status_code == 200:
    #         json_data = json.loads(response.text)
    #         image_url = json_data['photos'][0]['src']['large']
    #         print(image_url)

    #         result['image_'+str(idx)] = image_url
    #         idx += 1

    print(result)
    return result

@app.route("/submit", methods=["GET", "POST"])
def submit():
    """
        renders the html page that display the information about recipe.
    :return:  recipe page that displays the information.
    """
    ingredients = request.form.get("ingredients")
    res = recipe(ingredients)
    return render_template("recipe_list.html", result=res)


@app.route("/", methods=["GET", "POST"])
def home():
    """
        Starter function that calls the index html page which is then used to take the input.
    :return: renders the home html page.
    """
    
    return render_template("index.html")

if __name__ == "__main__":
    """
        Driver for the program that starts the code. Port used is set to default port 5000
    """
    app.run(debug=True)