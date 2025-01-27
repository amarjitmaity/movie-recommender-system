import streamlit as st

# Importing the final_df dataframe in binary mode with the name of "movies_list" to form our website
import pickle
final_df=pickle.load(open('movies.pkl','rb'))

# Importing the similarity array in binary mode with the name of "similarity" to form our website
import pickle
similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

# Creating the input box of selecting any movie containing all the movies options
selected_movie_name=st.selectbox('Select your movie',final_df['title'])

# Defining the main "fetch_poster" function, which will recommend the similar output movies poster for a single input movie
import requests
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Defining the main "recommend" function, which will recommend the similar output movies for a single input movie
def recommend(selected_movie_name):
    movie_index=final_df[final_df['title']==selected_movie_name].index[0]
    distances=similarity[movie_index]   
    movies_list=sorted(enumerate(distances),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movie_names=[]
    recommended_movie_posters = []
    for i in movies_list:
       recommended_movie_names.append(final_df.iloc[i[0]].title)
       movie_id = final_df.iloc[i[0]].movie_id
       recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# Creating a button by pressing which, the website will show us the same movie as selected above
if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
