import streamlit as st
import pandas as pd
import os
import random

# --- Ensure CSV files exist ---
if not os.path.exists("movies.csv"):
    st.error("movies.csv not found! Please add it before running.")
if not os.path.exists("ratings.csv"):
    pd.DataFrame(columns=["userId", "userName", "movieId", "rating"]).to_csv("ratings.csv", index=False)

movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

# --- Define recommendation logic ---
def recommend_movie(genre, mood):
    filtered = movies[movies["genres"].str.contains(genre, case=False, na=False)]
    if filtered.empty:
        return None
    return filtered.sample(1).iloc[0]

# --- User Input ---
st.title("🎬 AI-Based Movie Recommendation System")

user_name = st.text_input("👤 Enter your name:")
user_mood = st.selectbox("😊 How are you feeling today?", ["Happy", "Sad", "Excited", "Romantic", "Tense"])
user_genre = st.selectbox("🎭 Choose your preferred genre:", ["Action", "Comedy", "Drama", "Thriller", "Romance", "Sci-Fi"])

# --- Recommendation Button ---
if st.button("🎥 Get Movie Recommendation"):
    recommended = recommend_movie(user_genre, user_mood)
    if recommended is not None:
        # Save movie info in session
        st.session_state.recommended = recommended
        st.session_state.user_name = user_name

        st.success(f"🍿 Hey {user_name}! Here's your movie recommendation 👇")
        st.subheader(f"🎬 {recommended['title']}")
        st.write(f"🎭 Genre: {recommended['genres']}")
        st.write(f"🌐 Language: {recommended.get('language', 'Unknown')}")

        if "image_url" in recommended and pd.notna(recommended["image_url"]):
            st.image(recommended["image_url"], width=300, caption=recommended["title"])
        else:
            st.info("Poster not available.")
    else:
        st.warning("No suitable movie found. Try another mood or genre!")

# --- Rating Section ---
if "recommended" in st.session_state:
    st.divider()
    st.subheader("⭐ Rate the Recommended Movie")
    rating = st.slider("How much did you like it?", 1, 5, 3)
    if st.button("💾 Save Rating"):
        recommended = st.session_state.recommended
        user_name = st.session_state.user_name

        new_entry = pd.DataFrame({
            "userId": [len(ratings) + 1],
            "userName": [user_name],
            "movieId": [recommended["movieId"]],
            "rating": [rating]
        })
        ratings = pd.concat([ratings, new_entry], ignore_index=True)
        ratings.to_csv("ratings.csv", index=False)

        st.success("✅ Your rating has been saved successfully!")
