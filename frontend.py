import streamlit as st
import utilities as ut
from PIL import Image
from streamlit.components.v1 import html

FLASK_SERVER_URL = "http://127.0.0.1:5000"


image_urls = ["https://media.istockphoto.com/id/1460853312/photo/abstract-connected-dots-and-lines-concept-of-ai-technology-motion-of-digital-data-flow.jpg?s=612x612&w=0&k=20&c=bR6oXBoagK2Yagty_At67Dx_wiYRuKJY3hM_ZHCuIxo=","https://media.istockphoto.com/id/1438504729/photo/shot-of-sound-recording-studio-mixer.jpg?s=612x612&w=0&k=20&c=3vBl54T4beVGGKrLoJ14HvTXKmjLYwLkQiPgdlJIos8=","https://picsum.photos/300/200","https://picsum.photos/300/200","https://picsum.photos/300/200","https://picsum.photos/300/200","https://picsum.photos/300/200","https://picsum.photos/300/200","https://picsum.photos/300/200","https://picsum.photos/id/41/367/267"]

image_data = [
    ("https://picsum.photos/300/200", ("Artist 1", "Song 1")),
    ("https://picsum.photos/300/200", ("Artist 2", "Song 2")),
    ("https://picsum.photos/300/200", ("Artist 3", "Song 3")),
]
# Page setup
st.set_page_config(page_title="Music recommender", page_icon="🎶", layout="wide")
st.title("🎶 Music recommender")

if 'new_release_button' not in st.session_state:
    st.session_state.key = False
if 'charts_button' not in st.session_state:
    st.session_state.key = False
if 'moods_and_genres_button' not in st.session_state:
    st.session_state.key = False
if 'geeks_button' not in st.session_state:
    st.session_state['geeks_button'] = False
if 'slider_seeker' not in st.session_state:
    st.session_state['slider_seeker'] = False
if 'slider_seeker_button' not in st.session_state:
    st.session_state['slider_seeker_button'] = False


if 'sad_button' not in st.session_state:
    st.session_state['sad_button'] = False
if 'romance_button' not in st.session_state:
    st.session_state['romance_button'] = False

if 'party_button' not in st.session_state:
    st.session_state['party_button'] = False

if 'sleep_button' not in st.session_state:
    st.session_state['sleep_button'] = False

def login_page():
    # Center the content on the page
    st.markdown(
        """
        <style>
        .st-centered {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
        }
        .image-container {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Create a centered header
    st.markdown("<h3 style='text-align: center;'>Log in with</h3>", unsafe_allow_html=True)

    # Spotify logo URL (replace with the actual image URL)
    spotify_logo_url = "https://developer.spotify.com/images/guidelines/design/logos.svg"

    # Wrap the image in a container div to center it
    spotify_login_button = f"""
    <div class="image-container">
        <a href="{FLASK_SERVER_URL}/login">
            <img src="{spotify_logo_url}" alt="Login with Spotify" style="width: 200px; height: auto;">
        </a>
    </div>
    """

    # Display the Spotify login button in the centered layout
    st.markdown(spotify_login_button, unsafe_allow_html=True)



def protected_content():
    row_input = st.columns((2, 1, 2, 1))
    with row_input[0]:
        # Use a text_input to get the keywords to filter the database
        text_search = st.text_input("🔍 Search music by title or musician", value="")
        # Filter the dataframe using masks
        df = ut.extract_data_into_dataframe()
        
        print(text_search)
        m1 = df['track_name'].str.contains(text_search)
        print(m1)
        m2 = df['artists'].str.contains(text_search)
        print(m2)
        
        df_search = df[m1 | m2]
        if text_search:
            print(df_search)

    # Create a horizontal container for the buttons
    button_container = st.columns(spec=[0.3, 0.3, 0.3], gap="medium") 
    # Create buttons for each subheader within the container and also set session states for them
   

    # with button_container[0]:
    #     new_release_button = st.button("🆕 New releases", use_container_width=True)
        
    with button_container[0]:
        charts_button = st.button("↗️ Charts", use_container_width=True)
        
    with button_container[1]:
        moods_and_genres_button = st.button("😊 Moods and genres", use_container_width=True)

    
    with button_container[2]:
        geeks_button = st.button("🤓 For geeks",use_container_width=True)

    if geeks_button:
        st.session_state['geeks_button'] = not st.session_state['geeks_button']
        
        
    bb = ""
    if st.session_state["geeks_button"]:

         # Explain the purpose of tempo range
        st.write("Set your preferred tempo range for music. For example, if you like slower music, set a lower minimum tempo, and if you prefer faster music, set a higher maximum tempo.")

        st.session_state['slider_seeker'] = not st.session_state['slider_seeker']
        st.session_state['slider_seeker_button'] = not st.session_state['slider_seeker_button']
        # Use st.slider for an interactive range input
        tempo_min = st.slider("Minimum Tempo (BPM)", min_value=60, max_value=180, value=80)
        tempo_max = st.slider("Maximum Tempo (BPM)", min_value=60, max_value=180, value=140)
        energy = st.slider("Energy", min_value=60, max_value=180, value=140)
        acousticness = st.slider("Acousticness", min_value=60, max_value=180, value=140)
        valance = st.slider("Valance", min_value=60, max_value=180, value=140)

        
        bb = st.button("get recommendation")

    if bb:
        st.write("")
        if st.session_state['slider_seeker_button']:
            # You can use these tempo_min and tempo_max values in your recommendation system
            st.write(f"Your preferred tempo range: {tempo_min} BPM - {tempo_max} BPM")

    # # Define sections for each subheader
    # if new_release_button:
    #         st.session_state['slider_seeker'] = False
    #         st.session_state["geeks_button"] = False
    #         st.subheader("New Tracks")
    #         # Call the function to generate the scrolling content
    #         scrolling_content = ut.generate_horizontal_scrolling_content(image_data)
    #         # Display the scrolling content
    #         st.markdown(scrolling_content, unsafe_allow_html=True)
    #         #html(scrolling_content)

        
    if charts_button:
        
        st.session_state['slider_seeker'] = False
        st.session_state["geeks_button"] = False
        #st.experimental_rerun()

        st.subheader("Most Popular Tracks")
        df = ut.extract_data_into_dataframe()
        popular_tracks_recs = ut.get_popular_tracks(df)
        print(popular_tracks_recs.iloc[0]['artists'])
        image_data_popular_tracks = [
            ("https://picsum.photos/id/45/367/267", (popular_tracks_recs.iloc[0]['artists'], popular_tracks_recs.iloc[0]['track_name'])),
        ("https://picsum.photos/id/41/367/267", (popular_tracks_recs.iloc[1]['artists'], popular_tracks_recs.iloc[1]['track_name'])),
        ("https://picsum.photos/id/42/367/267", (popular_tracks_recs.iloc[2]['artists'], popular_tracks_recs.iloc[2]['track_name'])),
        ("https://picsum.photos/id/46/367/267", (popular_tracks_recs.iloc[3]['artists'], popular_tracks_recs.iloc[3]['track_name'])),
        ("https://picsum.photos/id/47/367/267", (popular_tracks_recs.iloc[4]['artists'], popular_tracks_recs.iloc[4]['track_name'])),
        ("https://picsum.photos/id/48/367/267", (popular_tracks_recs.iloc[5]['artists'], popular_tracks_recs.iloc[5]['track_name'])),
        ("https://picsum.photos/id/49/367/267", (popular_tracks_recs.iloc[6]['artists'], popular_tracks_recs.iloc[6]['track_name'])),
        ("https://picsum.photos/id/4/367/267", (popular_tracks_recs.iloc[7]['artists'], popular_tracks_recs.iloc[7]['track_name'])),
        ("https://picsum.photos/id/2/367/267", (popular_tracks_recs.iloc[8]['artists'], popular_tracks_recs.iloc[8]['track_name'])),
        ("https://picsum.photos/id/3/367/267", (popular_tracks_recs.iloc[9]['artists'], popular_tracks_recs.iloc[9]['track_name']))]
        # Call the function to generate the scrolling content
        scrolling_content = ut.generate_horizontal_scrolling_content(image_data_popular_tracks)
        # Display the scrolling content
        st.markdown(scrolling_content, unsafe_allow_html=True)
        st.subheader("Top artists")

        df = ut.extract_data_into_dataframe()
        popular_artists_recs = ut.get_top_artists(df)
        print(popular_artists_recs.iloc[0]['artists'])
        image_data_popular_artists = [
            ("https://picsum.photos/id/45/367/267", (popular_artists_recs.iloc[0]['artists'], "")),
        ("https://picsum.photos/id/41/367/267", (popular_artists_recs.iloc[1]['artists'], "")),
        ("https://picsum.photos/id/42/367/267", (popular_artists_recs.iloc[2]['artists'], "")),
        ("https://picsum.photos/id/46/367/267", (popular_artists_recs.iloc[3]['artists'], "")),
        ("https://picsum.photos/id/47/367/267", (popular_artists_recs.iloc[4]['artists'], "")),
        ("https://picsum.photos/id/48/367/267", (popular_artists_recs.iloc[5]['artists'], "")),
        ("https://picsum.photos/id/49/367/267", (popular_artists_recs.iloc[6]['artists'], "")),
        ("https://picsum.photos/id/4/367/267", (popular_artists_recs.iloc[7]['artists'], "")),
        ("https://picsum.photos/id/2/367/267", (popular_artists_recs.iloc[8]['artists'], "")),
        ("https://picsum.photos/id/3/367/267", (popular_artists_recs.iloc[9]['artists'], ""))]

        # Call the function to generate the scrolling content
        scrolling_content = ut.generate_horizontal_scrolling_content(image_data_popular_artists)
        # Display the scrolling content
        st.markdown(scrolling_content, unsafe_allow_html=True)

    if moods_and_genres_button:
        st.session_state['slider_seeker'] = False
        st.session_state["geeks_button"] = False
        
        st.subheader(" Breakbeat")

        df = ut.extract_data_into_dataframe()
        breakbeat_recs = ut.get_song_recommendations_by_genre(df,'breakbeat',10)
        print(breakbeat_recs)
        image_data_breakbeat = [
            ("https://picsum.photos/id/45/367/267", (df['artists'][breakbeat_recs[0]], df['track_name'][breakbeat_recs[0]])),
        ("https://picsum.photos/id/41/367/267", (df['artists'][breakbeat_recs[1]], df['track_name'][breakbeat_recs[1]])),
        ("https://picsum.photos/id/42/367/267", (df['artists'][breakbeat_recs[2]], df['track_name'][breakbeat_recs[2]])),
        ("https://picsum.photos/id/46/367/267", (df['artists'][breakbeat_recs[3]], df['track_name'][breakbeat_recs[3]])),
        ("https://picsum.photos/id/47/367/267", (df['artists'][breakbeat_recs[4]], df['track_name'][breakbeat_recs[4]])),
        ("https://picsum.photos/id/48/367/267", (df['artists'][breakbeat_recs[5]], df['track_name'][breakbeat_recs[5]])),
        ("https://picsum.photos/id/49/367/267", (df['artists'][breakbeat_recs[6]], df['track_name'][breakbeat_recs[6]])),
        ("https://picsum.photos/id/4/367/267", (df['artists'][breakbeat_recs[7]], df['track_name'][breakbeat_recs[7]])),
        ("https://picsum.photos/id/2/367/267", (df['artists'][breakbeat_recs[8]], df['track_name'][breakbeat_recs[8]])),
        ("https://picsum.photos/id/3/367/267", (df['artists'][breakbeat_recs[9]], df['track_name'][breakbeat_recs[9]]))
            ]
        scrolling_content = ut.generate_horizontal_scrolling_content(image_data_breakbeat)
            # Display the scrolling content
        st.markdown(scrolling_content, unsafe_allow_html=True)

        st.subheader(" Ambient")
        ambient_recs = ut.get_song_recommendations_by_genre(df,'ambient',10)
        print(ambient_recs)

        image_data_ambient = [
            ("https://picsum.photos/id/45/367/267", (df['artists'][ambient_recs[0]], df['track_name'][ambient_recs[0]])),
        ("https://picsum.photos/id/41/367/267", (df['artists'][ambient_recs[1]], df['track_name'][ambient_recs[1]])),
        ("https://picsum.photos/id/42/367/267", (df['artists'][ambient_recs[2]], df['track_name'][ambient_recs[2]])),
        ("https://picsum.photos/id/46/367/267", (df['artists'][ambient_recs[3]], df['track_name'][ambient_recs[3]])),
        ("https://picsum.photos/id/47/367/267", (df['artists'][ambient_recs[4]], df['track_name'][ambient_recs[4]])),
        ("https://picsum.photos/id/48/367/267", (df['artists'][ambient_recs[5]], df['track_name'][ambient_recs[5]])),
        ("https://picsum.photos/id/49/367/267", (df['artists'][ambient_recs[6]], df['track_name'][ambient_recs[6]])),
        ("https://picsum.photos/id/4/367/267", (df['artists'][ambient_recs[7]], df['track_name'][ambient_recs[7]])),
        ("https://picsum.photos/id/2/367/267", (df['artists'][ambient_recs[8]], df['track_name'][ambient_recs[8]])),
        ("https://picsum.photos/id/3/367/267", (df['artists'][ambient_recs[9]], df['track_name'][ambient_recs[9]]))
            ]

        scrolling_content = ut.generate_horizontal_scrolling_content(image_data_ambient)
            # Display the scrolling content
        st.markdown(scrolling_content, unsafe_allow_html=True)

        st.subheader(' Anime')

        anime_recs = ut.get_song_recommendations_by_genre(df,'anime',10)
        print(anime_recs)

        image_data_anime = [
            ("https://picsum.photos/id/45/367/267", (df['artists'][anime_recs[0]], df['track_name'][anime_recs[0]])),
        ("https://picsum.photos/id/41/367/267", (df['artists'][anime_recs[1]], df['track_name'][anime_recs[1]])),
        ("https://picsum.photos/id/42/367/267", (df['artists'][anime_recs[2]], df['track_name'][anime_recs[2]])),
        ("https://picsum.photos/id/46/367/267", (df['artists'][anime_recs[3]], df['track_name'][anime_recs[3]])),
        ("https://picsum.photos/id/47/367/267", (df['artists'][anime_recs[4]], df['track_name'][anime_recs[4]])),
        ("https://picsum.photos/id/48/367/267", (df['artists'][anime_recs[5]], df['track_name'][anime_recs[5]])),
        ("https://picsum.photos/id/49/367/267", (df['artists'][anime_recs[6]], df['track_name'][anime_recs[6]])),
        ("https://picsum.photos/id/4/367/267", (df['artists'][anime_recs[7]], df['track_name'][anime_recs[7]])),
        ("https://picsum.photos/id/2/367/267", (df['artists'][anime_recs[8]], df['track_name'][anime_recs[8]])),
        ("https://picsum.photos/id/3/367/267", (df['artists'][anime_recs[9]], df['track_name'][anime_recs[9]]))
            ]

        scrolling_content = ut.generate_horizontal_scrolling_content(image_data_anime)
            # Display the scrolling content
        st.markdown(scrolling_content, unsafe_allow_html=True)

        st.subheader(' Bluegrass')

        bluegrass_recs = ut.get_song_recommendations_by_genre(df,'bluegrass',10)
        print(bluegrass_recs)

        image_data_bluegrass = [
            ("https://picsum.photos/id/45/367/267", (df['artists'][bluegrass_recs[0]], df['track_name'][bluegrass_recs[0]])),
        ("https://picsum.photos/id/41/367/267", (df['artists'][bluegrass_recs[1]], df['track_name'][bluegrass_recs[1]])),
        ("https://picsum.photos/id/42/367/267", (df['artists'][bluegrass_recs[2]], df['track_name'][bluegrass_recs[2]])),
        ("https://picsum.photos/id/46/367/267", (df['artists'][bluegrass_recs[3]], df['track_name'][bluegrass_recs[3]])),
        ("https://picsum.photos/id/47/367/267", (df['artists'][bluegrass_recs[4]], df['track_name'][bluegrass_recs[4]])),
        ("https://picsum.photos/id/48/367/267", (df['artists'][bluegrass_recs[5]], df['track_name'][bluegrass_recs[5]])),
        ("https://picsum.photos/id/49/367/267", (df['artists'][bluegrass_recs[6]], df['track_name'][bluegrass_recs[6]])),
        ("https://picsum.photos/id/4/367/267", (df['artists'][bluegrass_recs[7]], df['track_name'][bluegrass_recs[7]])),
        ("https://picsum.photos/id/2/367/267", (df['artists'][bluegrass_recs[8]], df['track_name'][bluegrass_recs[8]])),
        ("https://picsum.photos/id/3/367/267", (df['artists'][bluegrass_recs[9]], df['track_name'][bluegrass_recs[9]]))
            ]

        scrolling_content = ut.generate_horizontal_scrolling_content(image_data_bluegrass)
            # Display the scrolling content
        st.markdown(scrolling_content, unsafe_allow_html=True)

        st.subheader("Acoustic")
        df = ut.extract_data_into_dataframe()
        acos_recs = ut.get_song_recommendations_by_genre(df,'acoustic',10)
        print(acos_recs)

        
        image_data_acos = [
            ("https://picsum.photos/id/45/367/267", (df['artists'][acos_recs[0]], df['track_name'][acos_recs[0]])),
        ("https://picsum.photos/id/41/367/267", (df['artists'][acos_recs[1]], df['track_name'][acos_recs[1]])),
        ("https://picsum.photos/id/42/367/267", (df['artists'][acos_recs[2]], df['track_name'][acos_recs[2]])),
        ("https://picsum.photos/id/46/367/267", (df['artists'][acos_recs[3]], df['track_name'][acos_recs[3]])),
        ("https://picsum.photos/id/47/367/267", (df['artists'][acos_recs[4]], df['track_name'][acos_recs[4]])),
        ("https://picsum.photos/id/48/367/267", (df['artists'][acos_recs[5]], df['track_name'][acos_recs[5]])),
        ("https://picsum.photos/id/49/367/267", (df['artists'][acos_recs[6]], df['track_name'][acos_recs[6]])),
        ("https://picsum.photos/id/4/367/267", (df['artists'][acos_recs[7]], df['track_name'][acos_recs[7]])),
        ("https://picsum.photos/id/2/367/267", (df['artists'][acos_recs[8]], df['track_name'][acos_recs[8]])),
        ("https://picsum.photos/id/3/367/267", (df['artists'][acos_recs[9]], df['track_name'][acos_recs[9]]))
            ]
        scrolling_content = ut.generate_horizontal_scrolling_content(image_data_acos)
            # Display the scrolling content
        st.markdown(scrolling_content, unsafe_allow_html=True)

        st.subheader("Afro-beat")
        afro_recs = ut.get_song_recommendations_by_genre(df,'afrobeat',10)
        print(afro_recs)

        image_data_afro = [
            ("https://picsum.photos/id/45/367/267", (df['artists'][afro_recs[0]], df['track_name'][afro_recs[0]])),
        ("https://picsum.photos/id/41/367/267", (df['artists'][afro_recs[1]], df['track_name'][afro_recs[1]])),
        ("https://picsum.photos/id/42/367/267", (df['artists'][afro_recs[2]], df['track_name'][afro_recs[2]])),
        ("https://picsum.photos/id/46/367/267", (df['artists'][afro_recs[3]], df['track_name'][afro_recs[3]])),
        ("https://picsum.photos/id/47/367/267", (df['artists'][afro_recs[4]], df['track_name'][afro_recs[4]])),
        ("https://picsum.photos/id/48/367/267", (df['artists'][afro_recs[5]], df['track_name'][afro_recs[5]])),
        ("https://picsum.photos/id/49/367/267", (df['artists'][afro_recs[6]], df['track_name'][afro_recs[6]])),
        ("https://picsum.photos/id/4/367/267", (df['artists'][afro_recs[7]], df['track_name'][afro_recs[7]])),
        ("https://picsum.photos/id/2/367/267", (df['artists'][afro_recs[8]], df['track_name'][afro_recs[8]])),
        ("https://picsum.photos/id/3/367/267", (df['artists'][afro_recs[9]], df['track_name'][afro_recs[9]]))]
        scrolling_content = ut.generate_horizontal_scrolling_content(image_data_afro)
            # Display the scrolling content
        st.markdown(scrolling_content, unsafe_allow_html=True)

        st.subheader("Blues")
        blues_recs = ut.get_song_recommendations_by_genre(df,'blues',10)
        print(blues_recs)

        image_data_blues = [
            ("https://picsum.photos/id/45/367/267", (df['artists'][blues_recs[0]], df['track_name'][blues_recs[0]])),
        ("https://picsum.photos/id/41/367/267", (df['artists'][blues_recs[1]], df['track_name'][blues_recs[1]])),
        ("https://picsum.photos/id/42/367/267", (df['artists'][blues_recs[2]], df['track_name'][blues_recs[2]])),
        ("https://picsum.photos/id/46/367/267", (df['artists'][blues_recs[3]], df['track_name'][blues_recs[3]])),
        ("https://picsum.photos/id/37/367/267", (df['artists'][blues_recs[4]], df['track_name'][blues_recs[4]])),
        ("https://picsum.photos/id/28/367/267", (df['artists'][blues_recs[5]], df['track_name'][blues_recs[5]])),
        ("https://picsum.photos/id/49/367/267", (df['artists'][blues_recs[6]], df['track_name'][blues_recs[6]])),
        ("https://picsum.photos/id/4/367/267", (df['artists'][blues_recs[7]], df['track_name'][blues_recs[7]])),
        ("https://picsum.photos/id/2/367/267", (df['artists'][blues_recs[8]], df['track_name'][blues_recs[8]])),
        ("https://picsum.photos/id/3/367/267", (df['artists'][blues_recs[9]], df['track_name'][blues_recs[9]]))]

        scrolling_content = ut.generate_horizontal_scrolling_content(image_data_blues)
            # Display the scrolling content
        st.markdown(scrolling_content, unsafe_allow_html=True)

        st.subheader("Brazil")
        brazil_recs = ut.get_song_recommendations_by_genre(df,'brazil',10)
        print(brazil_recs)

        image_data_brazil = [
            ("https://picsum.photos/id/45/367/267", (df['artists'][brazil_recs[0]], df['track_name'][blues_recs[0]])),
        ("https://picsum.photos/id/41/367/267", (df['artists'][brazil_recs[1]], df['track_name'][brazil_recs[1]])),
        ("https://picsum.photos/id/42/367/267", (df['artists'][brazil_recs[2]], df['track_name'][brazil_recs[2]])),
        ("https://picsum.photos/id/46/367/267", (df['artists'][brazil_recs[3]], df['track_name'][brazil_recs[3]])),
        ("https://picsum.photos/id/37/367/267", (df['artists'][brazil_recs[4]], df['track_name'][brazil_recs[4]])),
        ("https://picsum.photos/id/28/367/267", (df['artists'][brazil_recs[5]], df['track_name'][brazil_recs[5]])),
        ("https://picsum.photos/id/49/367/267", (df['artists'][brazil_recs[6]], df['track_name'][brazil_recs[6]])),
        ("https://picsum.photos/id/4/367/267", (df['artists'][brazil_recs[7]], df['track_name'][brazil_recs[7]])),
        ("https://picsum.photos/id/2/367/267", (df['artists'][brazil_recs[8]], df['track_name'][brazil_recs[8]])),
        ("https://picsum.photos/id/3/367/267", (df['artists'][brazil_recs[9]], df['track_name'][brazil_recs[9]]))]


    
        scrolling_content = ut.generate_horizontal_scrolling_content(image_data_brazil)
            # Display the scrolling content
        st.markdown(scrolling_content, unsafe_allow_html=True)
    
# Main application
def main():
    
    is_not_logged = True

    if is_not_logged:
        #login_page()
        protected_content()
    else: 
        protected_content()


main()