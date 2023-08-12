#auther: Sayak Ghosh - 08/13/2023
from sentence_transformers import SentenceTransformer
import pinecone
import openai
import streamlit as st
openai.api_key = "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"
model = SentenceTransformer('all-MiniLM-L12-v2')

pinecone.init(api_key='e0af7c2a-e4a5-48de-8985-810e4967f75a', environment='asia-southeast1-gcp-free')
index = pinecone.Index('mr-einstein')

def find_match(input):
    input_em = model.encode(input).tolist()
    result = index.query(input_em, top_k=2, includeMetadata=True)
    return result['matches'][0]['metadata']['text']+"\n"+result['matches'][1]['metadata']['text']

def query_refiner(conversation, query):

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response['choices'][0]['text']

def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses'])-1):
        
        conversation_string += "Human: "+st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: "+ st.session_state['responses'][i+1] + "\n"
    return conversation_string