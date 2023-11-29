import streamlit as st
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import urllib.parse

nltk.download('punkt')
nltk.download('stopwords')

def goodreads_wrapped(df, year):
    st.subheader(f'📚 Goodreads Wrapped for {year} 🎁')

    df['Date Read'] = pd.to_datetime(df['Date Read'])
    df = df[df['Date Read'].dt.year == year]

    books_read = df['Title'].count()
    st.write(f'📖 Number of Books Read: {books_read}')

    top_authors = df['Author'].value_counts().head(5)
    st.write('🖋️ Top Authors:')
    st.write(top_authors)

    highest_rated_books = df[df['My Rating'] == df['My Rating'].max()]['Title']
    st.write('⭐ Highest Rated Books:')
    st.write(highest_rated_books)

    average_rating = df['My Rating'].mean()
    st.write(f'🌟 Average Rating: {average_rating:.2f}')

    total_pages_read = df['Number of Pages'].sum()
    total_pages_read = int(total_pages_read)
    st.write(f'📚 Total Pages Read: {total_pages_read}')

    all_reviews = df['My Review'].str.cat(sep=' ').lower()
    tokens = word_tokenize(all_reviews)
    stop_words = set(stopwords.words('english'))
    words = [word for word in tokens if word.isalpha() and word not in stop_words]
    freq_dist = nltk.FreqDist(words)
    st.write('🔠 Top 5 Most Common Words in Reviews:')
    top_words =[]
    for word, count in freq_dist.most_common(5):
        st.write(f'{word}: {count}')
        top_words.append(f'{word}: {count}')

    
    if not top_words:
        tweet_text = f"🎁 My Goodreads Wrapped for {year}: I read {books_read} books 📚, totaling {total_pages_read} pages. 🌟 My average rating was {average_rating:.2f}. Highest rated books: {', '.join(highest_rated_books[:2])}. #GoodreadsWrapped"
    else:
        tweet_text = f"🎁 My Goodreads Wrapped for {year}: I read {books_read} books 📚, totaling {total_pages_read} pages. 🌟 My average rating was {average_rating:.2f}. Highest rated books: {', '.join(highest_rated_books[:2])}. 🔠 Top words in reviews: {', '.join(top_words)}. #GoodreadsWrapped"

    
    tweet_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(tweet_text)}&via=demirbasayyuce"
    st.markdown(f'<a href="{tweet_url}" target="_blank">Share these stats on X (Twitter)</a>', unsafe_allow_html=True)

st.title('📚 Goodreads Wrapped 🎁')
st.write('Upload your Goodreads data and get your reading statistics for the year!')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    years = sorted(df['Date Read'].dropna().apply(lambda x: pd.to_datetime(x).year).unique())
    year = st.selectbox('Select a Year', options=years)
    goodreads_wrapped(df, year)