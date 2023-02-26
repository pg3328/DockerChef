import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TF_IDF():
    __slots__ = "vectorizer", "df", "similarity_scores", "corpus", "query", "top_recipes"
    def __init__(self, file_name = 'RAW_recipes.csv') -> None:
        self.vectorizer = CountVectorizer()
        self.df = pd.read_csv(file_name)
        self.similarity_scores = None
        self.corpus = None
        self.query = None
        self.top_recipes = None

    def pre_processing(self):
        # Preprocess the text
        self.df['ingredients'] = self.df['ingredients'].apply(lambda x: x.lower())
        self.df['ingredients'] = self.df['ingredients'].str.replace('[^\w\s]','')

        self.corpus = self.vectorizer.fit_transform(self.df['ingredients'])


    def get_top_3(self, ingredient_list):
        self.query = ingredient_list
        
        query_vector = self.vectorizer.transform([' '.join(self.query)])

        self.similarity_scores = cosine_similarity(query_vector, self.corpus)
        N = 3
        top_indices = self.similarity_scores.argsort()[0][::-1][:N]
        self.top_recipes = self.df.iloc[top_indices]
        # print(self.top_recipes)


    def extract_description(self):
        top_3_descriptions = self.top_recipes['description']
        top_3_ids = self.top_recipes['id']
        return (top_3_descriptions, top_3_ids)

    def extract_detailed_info(self, id):
        frame = self.df[self.df['id'] == id]
        return frame['steps'], frame['ingredients'].values

