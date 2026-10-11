import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster (movie_title):
    try:
        response = requests.get(
            'https://www.omdbapi.com/',
            params={'t': movie_title, 'apikey': 'bfdb5c3a'},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        poster = data.get('Poster')
        if isinstance(poster, str) and poster.startswith('http'):
            return poster
        return None
    except (requests.exceptions.RequestException, ValueError, AttributeError):
        return None

def show_poster(url):
    if url:
        st.image(url)
    else:
        st.text("Poster unavailable")

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similirety[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse = True,key = lambda x:x[1])[1:6]
    recommended = []
    movie_poster = []
    for i in movie_list:
           id = movies.iloc[i[0]].movie_id
           recommended.append(movies.iloc[i[0]].title)
           movie_poster.append(fetch_poster(movies.iloc[i[0]].title))
    return recommended,movie_poster

movies_list = pickle.load(open('movies.pkl','rb'))
movies =pd.DataFrame(movies_list)
similirety = pickle.load(open('similirety.pkl','rb'))

st.title("Movie Recommendation System")
selected_movies_name = st.selectbox(
    "Top 5 Movies on your Intersts",
    (movies['title'].values),
)

if st.button("Recommend"):
    names,poster = recommend(selected_movies_name)
    col1, col2, col3,col4,col5 = st.columns(5)
    
    with col1:
       st.text(names[0])
       show_poster(poster[0])

    with col2:
       st.text(names[1])
       show_poster(poster[1])

    with col3:
       st.text(names[2])
       show_poster(poster[2])

    with col4:
       st.text(names[3])
       show_poster(poster[3])

    with col5:
       st.text(names[4])
       show_poster(poster[4])



st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: chocolate;
        
    }
    
    /* Optional: Make the top header bar transparent to match */
    [data-testid="stHeader"] {
        
        background-color:black;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.text("Search Over 5000+ Movies")