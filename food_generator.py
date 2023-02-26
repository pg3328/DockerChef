from flask import Flask, request, render_template
import requests
import xml.etree.ElementTree as ET
from tf_idf import TF_IDF

app = Flask(__name__)

@app.route("/recipe")
def recipe(query):
    query = query.split(",")
    model = TF_IDF()
    model.pre_processing()
    model.get_top_3(query)
    descriptions, ids = model.extract_description()
    for description in descriptions:
        print(description)
        print("---------------")

    for id in ids:
        print(id)
        steps, ingredients = model.extract_detailed_info(id)
        
        print(ingredients)
        for i in steps.values:
            i=i[1:-2]
            # i is a string
            for word in (i.strip(",").strip(", ").split("'")):
                if word == ", ":
                    continue
                print(word)

        print("---------------")

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