# Brick-Hack
The project is a site for recipe suggestion based on the input ingredients

Using flask, HTML, CSS and bootstrap, the backend and the frontend of the website have been built.

To further extend the project to make use of microservices, the website is hosted
on docker container to handle scalability in the future.

To map the recipes to the input ingredients, a model based on TF-IDF transformer has been built and the matching recipes are ranked using cosine similarity and the top 3 results are displayed to the user.

Steps to build the project:
1. Clone the repository.
2. Download the recipe.csv file from (https://tinyurl.com/46m9bb7b)
2. Run `docker build -t recipeFinder .`
3. Run `docker run -p 5001:5000 recipeFinder`
4. The website can be accessed at `http://localhost:5001`
