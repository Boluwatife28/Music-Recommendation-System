from PIL import Image
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize

#def populate_image_data(data):

def extract_data_into_dataframe():
    #input the dataset path
    df = pd.read_csv()  
    return df[:12000]
def get_song_recommendations_by_genre(data, genre, num_recommendations=5):
    # Get the index of the chosen genre
    try:
        genre_idx = data[data['track_genre'] == genre].index[0]
    except IndexError:
        print(f"Genre '{genre}' not found in the dataset.")
        return []
    # Drop non-numeric and non-genre columns
    numeric_data = data.drop(['track_name', 'track_genre', 'artists','album_name','track_id'], axis=1)

    # Encode the 'artist' column to numerical labels
    le = LabelEncoder()
    data['artist_label'] = le.fit_transform(data['artists'])
    # Define the batch size (adjust as needed)
    batch_size = 1000
    # Initialize the StandardScaler
    scaler = StandardScaler()
# Iterate through the dataset in batches
    for start in range(0, len(numeric_data), batch_size):
        end = start + batch_size
        batch_data = numeric_data[start:end]
    # Fit the scaler on the batch
    scaler.partial_fit(batch_data)
    # Now that the scaler is trained on the entire dataset, you can apply it to scale the entire dataset
    scaled_data = scaler.transform(numeric_data)
    # Calculate cosine similarity
    cosine_sim = cosine_similarity(scaled_data, scaled_data)
    # Get song recommendations based on the chosen genre
    recommendations = []
    try:
        similar_songs = cosine_sim[genre_idx].argsort()[-num_recommendations-1:-1][::-1]
        recommendations.extend(similar_songs)
    except IndexError:
        print("An IndexError occurred while getting song recommendations.")
    return recommendations

def get_top_artists(data):
    top_artists = data.groupby('artists')['popularity'].sum().reset_index()
    top_artists = top_artists.sort_values(by='popularity', ascending=False).head(10)
    return top_artists[["artists"]]
    

def get_popular_tracks(data):
    # Assuming 'data' is your DataFrame
    top_tracks = data[['artists', 'track_name', 'popularity']]
    top_tracks = top_tracks.sort_values(by='popularity', ascending=False).head(10)        
    return top_tracks[["artists","track_name"]]
   

def recommend_music(user_preferences, df):
    # Extract user preferences
    user_vector = [user_preferences['tempo'], user_preferences['energy'], user_preferences['acousticness'], user_preferences['valence']]

    # Normalize user vector
    user_vector = normalize([user_vector], norm='l2')

    # Extract music attributes for similarity calculation
    music_attributes = df[['tempo', 'energy', 'acousticness', 'valence']]

    # Normalize music attribute vectors
    music_attributes = normalize(music_attributes, norm='l2')

    # Calculate cosine similarity between user preferences and music items
    similarity_scores = cosine_similarity(user_vector, music_attributes)

    # Create a DataFrame with track_name and similarity score
    recommended_music = df[['track_name']]
    recommended_music['similarity_score'] = similarity_scores[0]

    # Sort music items by similarity score in descending order
    recommended_music = recommended_music.sort_values(by='similarity_score', ascending=False)

    return recommended_music[['track_name']]

def generate_horizontal_scrolling_content(image_data):
    content = """
    <style>
        .scroll-container {
            display: flex;
            align-items: center;
            overflow: hidden;
        }
        
        .scroll-content {
            overflow: auto;
            white-space: nowrap;
            flex: 1;
        }

        .scroll-button {
            background: none;
            border: none;
            cursor: pointer;
        }

        .image-container {
            display: inline-block;
            width: 300px;
            height: auto;
            margin: 10px;
            text-align: center;
        }
    </style>

    <div class="scroll-container">
        <div class="scroll-content">
            <div style="display: inline-block; width: 2000px;">
                <!-- Add your horizontally-scrollable content here -->
    """

    for image_url, (artist_name, song_name) in image_data:
        content += f'<div class="image-container">'
        content += f'<img src="{image_url}" style="max-width: 100%; max-height: 200px;" alt="Image">'
        content += f'<p><strong>Artist(s): {artist_name}</strong></p>'
        content += f'<p>Track: {song_name}</p>'
        content += f'</div>'
    
    content += """
            </div>
        </div>
    </div>
    """

    return content
# Example usage
image_urls = [""]


                                
