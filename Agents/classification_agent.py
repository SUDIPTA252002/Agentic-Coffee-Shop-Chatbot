import os
from langchain_groq import ChatGroq
import json
from dotenv import load_dotenv
from .utils import get_chatbot_response
from copy import deepcopy
load_dotenv()

class ClassificationAgent:
    def __init__(self):
        api_key=os.getenv("GROQ_API_KEY")
        model_name=os.getenv("MODEL_NAME")
        self.client=ChatGroq(api_key=api_key,model=model_name) 

    def get_respnse(self,messages):
        deepcopy(messages)
        input_messages=[]
        system_prompt="""You are a helpful AI assistant for a coffee shop application.
            Your task is to determine what agent should handle the user input. You have 3 agents to choose from:
            1. details_agent: This agent is responsible for answering questions about the coffee shop, like location, delivery places, working hours, details about menue items. Or listing items in the menu items. Or by asking what we have.
            2. order_taking_agent: This agent is responsible for taking orders from the user. It's responsible to have a conversation with the user about the order untill it's complete.
            3. recommendation_agent: This agent is responsible for giving recommendations to the user about what to buy. If the user asks for a recommendation, this agent should be used.
            
            Your output should be in a structured json format like so. each key is a string and each value is a string. Make sure to follow the format exactly:
            Each key and value must be wrapped in double quotes.
            Do not include any extra text or explanation outside the JSON.
            Strictly return only the JSON object.
            Pleae be very strict in returning the json and remember to add curly braces { at the start and } at the end of json            
            {
            "chain of thought": go over each of the agents above and write some your thoughts about what agent is this input relevant to.
            "decision": "details_agent" or "order_taking_agent" or "recommendation_agent". Pick one of those. and only write the word.
            "message": leave the message empty.
            }
        """
        input_messages=[{"role":"system","content":system_prompt}]
        input_messages+=messages[-3:]

        chatbot_output=get_chatbot_response(self.client,input_messages)
        output=self.postprocess_output(chatbot_output)

        return output



    def postprocess_output(self,output):
        try:
            cleaned_output=output.strip().strip('`').strip()
            parsed_output=json.loads(cleaned_output)
        except Exception as e:
            raise ValueError(f"Error Parsing output:{output}") from e


        return {
            "role":"Assistant",
            "content":parsed_output["message"],
            "memory":{
                "agent":"classification agent",
                "classification_decision":parsed_output["decision"]
            }
        }