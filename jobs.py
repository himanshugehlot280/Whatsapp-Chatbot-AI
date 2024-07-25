
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Pinecone
from langchain_community.vectorstores import Pinecone as PineconeStore
from langchain.vectorstores import Pinecone
from pinecone import Pinecone 
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from pinecone import Pinecone
from langchain_community.vectorstores import Pinecone as PineconeStore
from langchain.schema import Document
import time
from langchain.chat_models import ChatOpenAI 
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2") 


# Function to pull data from Pinecone Vector Store.
def pull_from_pinecone(pinecone_apikey=PINECONE_API_KEY ,pinecone_environment="gcp-starter",pinecone_index_name=PINECONE_INDEX_NAME ,embeddings=embeddings):
    print("20secs delay...")
    time.sleep(5)
    pinecone = Pinecone(
        api_key=pinecone_apikey,environment=pinecone_environment
    )
    index_name = pinecone_index_name
    index = PineconeStore.from_existing_index(index_name, embeddings)
    return index


# Function to fetch similar content from vector database
def similar_docs(query,k=2,pinecone_apikey=PINECONE_API_KEY,pinecone_environment="gcp-starter",pinecone_index_name=PINECONE_INDEX_NAME,embeddings=embeddings):
    pinecone = Pinecone(
        api_key=pinecone_apikey,environment=pinecone_environment
    )
    index_name = pinecone_index_name
    index = pull_from_pinecone(pinecone_apikey,pinecone_environment,index_name,embeddings)
    similar_docs = index.similarity_search_with_score(query, int(k))

    return similar_docs  


# Function for generating response for user query.
def gen(prompt): 
  llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model_name='gpt-4o',
    temperature=0.3
  ) 
  ans = llm.invoke(prompt) 
  return ans


# Create a prompt for OpenAI. 
def Generate_Prompt(relevant_docs,query_text):
    prompt = f"Based on the following information:\n\n{relevant_docs}\n\nRecommend the job to the user here is user details messages:\n{query_text} \n You got data of vacancy table now you have to recommend the job to the candidate based on the user messages  \n DO NOT USE YOUR KNOWLEDGE FOR ANSWERING QUESTION" 
    return prompt


# Function which combine all the above function. 
def mainjob(user_answer): 
    query = user_answer 
    relevant = similar_docs(query) 
    # print(relevant)  
    prompt = Generate_Prompt(relevant,query)   
    print(len(prompt))
    nresponse = gen(prompt)   
    print(nresponse)
    y = nresponse
    return y.content



