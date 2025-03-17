import streamlit as st
import pandas as pd
import requests
import pickle


with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)


def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movies_indices = [i[0] for i in sim_scores]
    return movies.loc[movies_indices, ['title', 'movie_id']]


def fetch_poster(movie_id):
    api_key = 'c7823f9077aab491088b430ff210ac5d'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception as e:
        print(f"Error fetching poster: {e}")
    return None

st.markdown(
    """
    <style>
        body {
            background-color: #e0f7fa;
            color: #000000;
            font-family: Arial, sans-serif;
        }
        .stApp {
            background-color: #e0f7fa;
            padding: 20px;
            border-radius: 12px;
        }
        .title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #01579b;
            text-align: center;
            margin-bottom: 20px;
        }
        .movie-card {
            background-color: #ffffff;
            padding: 10px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.2s;
            margin-bottom: 10px;
        }
        .movie-card:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        }
        img {
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title"> CINEMATE-MOVIE RECOMMENDATION</div>', unsafe_allow_html=True)
selected_movie = st.selectbox("Select a movie", movies['title'].values)


if st.button('Recommend', key='recommend_button'):
    recommendations = get_recommendations(selected_movie)
    st.write("### Top 10 Recommended Movies:")

    #  2x5 grid for recommendations
    for i in range(0, 10, 5):
        cols = st.columns(5)
        for col, (_, row) in zip(cols, recommendations.iloc[i:i + 5].iterrows()):
            movie_title = row['title']
            movie_id = row['movie_id']
            poster_url = fetch_poster(movie_id)
            with col:
                if poster_url:
                    st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                    st.image(poster_url, width=130)
                    st.write(f"**{movie_title}**")
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.write(f"**{movie_title}** (Poster not available)")






                 