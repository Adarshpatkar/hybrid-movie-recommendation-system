import streamlit as st
import pickle
import pandas as pd

movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movies['title_lower'] = movies['title'].str.casefold()

def recommend(movie, top_n=5):

    matched_movies = movies[
        movies['title_lower'] == movie.casefold()
    ]

    if matched_movies.empty:
        return []

    movie_index = matched_movies.index[0]

    distances = sorted(
        enumerate(similarity[movie_index]),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movies = []

    for index, similarity_score in distances[1:top_n+1]:
        recommended_movies.append(
            movies.iloc[index]['title']
        )

    return recommended_movies

st.title("🎬 Hybrid Movie Recommendation System")

selected_movie = st.selectbox(
    "Select a movie",
    movies["title"].values
)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)

    st.success(f"Top {len(recommendations)} Recommendations")

    st.subheader("Recommended Movies")

    for i, movie in enumerate(recommendations, start=1):
        st.write(f"{i}. {movie}")