from flask import Flask, request, render_template
import pandas as pd

# Load the dataset
data = pd.read_csv('netflix_titles.csv')

app = Flask(__name__)

@app.route('/')
def home():
    # Render the main page
    return render_template("index.html")

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user inputs
    genre = request.form.get('genre')
    num_recommendations = int(request.form.get('num_recommendations'))

    # Filter dataset by genre
    filtered_data = data[data['listed_in'].str.contains(genre, na=False, case=False)]
    
    # Check if the filtered data is empty, if so, provide general recommendations
    if filtered_data.empty:
        filtered_data = data.sample(num_recommendations)
    else:
        filtered_data = filtered_data.head(num_recommendations)

    # Convert filtered data to a list of dictionaries including all columns
    recommendations = filtered_data[['title', 'description', 'type', 'cast', 'director', 'release_year', 'rating', 'duration']].to_dict(orient='records')

    # Render recommendations
    return render_template(
        "index.html", recommendations=recommendations, genre=genre
    )

if __name__ == '__main__':
    app.run(debug=True)
