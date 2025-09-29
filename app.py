import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.title("CORD-19 Data Explorer")
st.write("Interactive exploration of COVID-19 research papers")

@st.cache_data
def load_data():
    use_cols = ["title", "abstract", "publish_time", "authors", "journal", "source_x"]
    df = pd.read_csv("data/metadata.csv", usecols=use_cols, low_memory=False)
    df = df.dropna(subset=["title", "abstract", "publish_time"])
    df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
    df = df.dropna(subset=["publish_time"])
    df["year"] = df["publish_time"].dt.year
    return df

df = load_data()

# Year filter
year_range = st.slider("Select year range", int(df["year"].min()), int(df["year"].max()), (2020, 2021))
filtered = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

# Publications per Year
st.subheader("Publications per Year")
st.bar_chart(filtered["year"].value_counts().sort_index())

# Top Journals
st.subheader("Top 10 Journals")
st.bar_chart(filtered["journal"].value_counts().head(10))

# Word Cloud
st.subheader("Word Cloud of Titles")
titles_text = " ".join(filtered["title"].dropna().astype(str).tolist())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(titles_text)
st.image(wordcloud.to_array())

# Data sample
st.subheader("Sample Papers")
st.write(filtered[["title", "authors", "journal", "publish_time"]].head(20))
