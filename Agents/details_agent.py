import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import json
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from .utils import get_chatbot_response,get_embedding
from copy import deepcopy
load_dotenv()


class DetailsAgent:
    def __init__(self):
        api_key=os.getenv("GROQ_API_KEY")
        model_name=os.getenv("MODEL_NAME")
        self.client=ChatGroq(api_key=api_key,model=model_name)
        self.embedding_model=SentenceTransformer(os.getenv("EMBEDDING_MODEL"))
        self.pc=Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name=os.getenv("INDEX_NAME")

    def get_closest_result(self,input_embeddings,index_name,top_k=2):
        index=self.pc.Index(index_name)

        results=index.query(
            namespace="ns1",
            vector=input_embeddings,
            top_k=top_k,
            include_value=False,
            include_metadata=True
        )
        
        return results
    
    def get_response(self,messages):
        messages=deepcopy(messages)


        user_message=messages[-1]["content"]
        embedding=get_embedding(self.embedding_model,user_message)
        result=self.get_closest_result(embedding,self.index_name)
        source_knowledge='\n'.join([x['metadata']['text'].strip()+"\n" for x in result['matches']])

        prompt = f"""
        Using the contexts below, answer the query.

        Contexts:
        {source_knowledge}

        Query: {user_message}
        """

        system_prompt = """ You are a customer support agent for a coffee shop called Merry's way. You should answer every question as if you are waiter and provide the neccessary information to the user regarding their orders and be very specific with answers."""

        messages[-1]['content']=prompt

        input_messages=[{"role":"system","content":system_prompt}]+messages[-3:]
        
        chatbot_output=get_chatbot_response(self.client,input_messages)
        output=self.postprocess_output(chatbot_output)

        return output
        

    def postprocess_output(self,output):
        return {
            "role":"Assistant",
            "content":output,
            "memory":{
                "agent":"details agent"
            }
        }
         

    