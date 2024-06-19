import streamlit as st
import os
from helper import *
from openai import OpenAI
import json

from semanticscholar import SemanticScholar
sch = SemanticScholar()

user_msg = st.text_input("Mileva", value="", placeholder="Prompt something", max_chars=None)

def build_knowledge_space(name, description, paper):
    # st.divider()
    st.text(name)
    st.text(description)
    st.text(f"Suggested paper: {paper}")

def talk_to_gpt():
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_CONTEXT},
            {"role": "user", "content": user_msg}
        ]
    )

    json_response = completion.choices[0].message.content.strip()
    print(json_response)
    json_obj = json.loads(json_response)
    # print(completion.choices[0].message.content)
    for subtopic in json_obj["subtopics"]:
        keywords_list = json_obj["subtopics"][subtopic]["keywords"]
        description = json_obj["subtopics"][subtopic]["description"]
        combined_query_string = ','.join(str(x) for x in keywords_list)
        results = sch.search_paper(combined_query_string, limit=5)
        build_knowledge_space(subtopic, description, results[0].title)
        # print(f'Subtopic {subtopic} has {results.total} results.', f'First occurrence: {results[0].title}.')
        
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# user_msg = st.text_input("Mileva", value="", placeholder="Prompt something", max_chars=None)
st.button("Enter", on_click=talk_to_gpt)
