import json
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def GET_FRUIT_DATA(user_preferences):
    def find_closest_fruit(word, fruit_names):
        # Use Jaccard similarity to find the closest matching fruit name
        vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 3))
        word_matrix = vectorizer.fit_transform([word] + fruit_names)
        similarity_scores = linear_kernel(word_matrix[0], word_matrix[1:]).flatten()
        closest_index = similarity_scores.argmax()
        return fruit_names[closest_index]

    def recommend_fruits(user_preferences, fruit_data, num_recommendations=12):
        # Create a list of fruit names from the data
        fruit_names = list(fruit_data.keys()) #list(fruit_data.keys())
        shuffled_fruit_names = random.sample(fruit_names, len(fruit_names))

        # Extract liked and allergic fruits from user preferences
        liked_fruits = [find_closest_fruit(word, shuffled_fruit_names) for word in user_preferences.get('likes', []).split(",")]
        allergic_fruits = [find_closest_fruit(word, shuffled_fruit_names) for word in user_preferences.get('allergies', []).split(",")]
        print(liked_fruits)
        print(allergic_fruits)
        # Remove allergic fruits from the list of recommended fruits
        recommended_fruits = [fruit for fruit in liked_fruits]
        
        # If there are not enough recommendations, add more based on vitamin C content
        remaining_recommendations = num_recommendations - len(recommended_fruits)
        additional_recommendations = [fruit for fruit in shuffled_fruit_names if fruit not in recommended_fruits and fruit not in allergic_fruits][:remaining_recommendations]
        recommended_fruits.extend(additional_recommendations)

        # Shuffle the order of the recommended fruits
        random.shuffle(recommended_fruits)

        return recommended_fruits

    # # Example usage:
    # user_preferences = {
    #     'likes': [],
    #     'allergies': [],
    # }

    def load_fruit_data(file_path):
        with open(file_path, 'r') as file:
            fruit_data = json.load(file)
        return fruit_data

    # Load fruit data from JSON file
    fruits_data = load_fruit_data('fruit_data.json')



    # Call the recommend_fruits function
    recommended_fruits = recommend_fruits(user_preferences, fruits_data)

    # Print the recommended fruits
    return recommended_fruits
