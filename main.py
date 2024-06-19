import os
from helper import *
from openai import OpenAI
import json
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

user_msg = input("Tell me a research area or question you have: ")

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": SYSTEM_CONTEXT},
    {"role": "user", "content": user_msg}
  ]
)

json_response = completion.choices[0].message.content.strip()
json_obj = json.loads(json_response)
print(json_obj)
from semanticscholar import SemanticScholar
sch = SemanticScholar()
# print(completion.choices[0].message.content)
for subtopic in json_obj["subtopics"]:
    keywords_list = json_obj["subtopics"][subtopic]["keywords"]
    combined_query_string = ','.join(str(x) for x in keywords_list)
    results = sch.search_paper(combined_query_string, limit=5)
    print(f'Subtopic {subtopic} has {results.total} results.', f'First occurrence: {results[0].title}.')