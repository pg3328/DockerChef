from flask import Flask, request, render_template

from tf_idf import TF_IDF

API_KEY = "rcaGhp0Af80tcX6DHEEvDbT0XNEiV3YZqi2fqO5YDfCAtOa001OS0VkJ"
IMAGE_URL = 'https://api.pexels.com/v1/search'
app = Flask(__name__)



@app.route("/getdata", methods=['POST'])
def get_recipe_details():
    id = int(request.form['id'])
    steps, ingredients = model.extract_detailed_info(id)
    result = {}
    result['ingredients'] = ingredients
    result['steps'] = []
    for i in steps.values:
        i = i[1:-2]
        # i is a string
        for word in (i.strip(",").strip(", ").split("'")):
            if word == ", " or len(word)==0:
                continue
            result['steps'].append(word)
    return render_template("recipe_detail.html", result=result)


@app.route("/recipe")
def recipe(query):
    query = query.split(",")

    model.get_top_3(query)
    result = {}
    titles, descriptions, ids, minutes = model.extract_description()
    max_length_of_titles = max(len(title) for title in titles)
    for idx, title in enumerate(titles):
        result["title_" + str(idx)] = str(title.capitalize())+(" " * (max_length_of_titles-len(title)))
    idx = 0
    for description in descriptions:
        result["description_" + str(idx)] = description
        idx += 1

    for idx, time in enumerate(minutes):
        result["time_" + str(idx)] = str(time)+" mins"

    idx = 0
    for id in ids:
        result["id_" + str(idx)] = id
        idx += 1
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
    model = TF_IDF()
    model.pre_processing()
    app.run(debug=True)
