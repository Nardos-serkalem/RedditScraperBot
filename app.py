import streamlit as st
import json

with open("ranked_saas_ideas.json", "r") as f:
    saas_ideas = json.load(f)

st.title(" Best SaaS Ideas from Reddit")
st.write("Using LLMs to rank the best startup ideas!")

for idea in saas_ideas[:10]:  
    st.subheader(idea["title"])
    st.write(f"Upvotes: {idea['upvotes']} | Comments: {idea['num_comments']}")
    st.write(f"AI Rating: {idea['llm_rating']}")
    st.write("---")
