import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=f52ba198cfc2e2928d65f3da009d97d4&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])

    recommendation_list = []
    recommendation_poster = []
    for i in movies_list[1:11]:
        movie_id = movies.iloc[i[0]].movie_id
        recommendation_poster.append(fetch_poster(movie_id))
        recommendation_list.append(movies.iloc[i[0]].title)

    return recommendation_list,recommendation_poster

st.title('Movie Recommender System')

selected_movie = st.selectbox(
    'Name a movie for recommendation',
    movies['title'].values
)

if st.button('recommend'):
    st.write('the recommended movies are :')
    recommended_movie_names , recommended_movie_posters= recommend(selected_movie)
    # cols = st.columns(5)
    # for i, col in enumerate(cols):
    #     with col:
    #         st.text(recommended_movie_names[i])
    #         st.image(recommended_movie_posters[i])

    rows = [st.columns(5), st.columns(5)]
    
    for i in range(10):
        col = rows[i // 5][i % 5]
        with col:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])