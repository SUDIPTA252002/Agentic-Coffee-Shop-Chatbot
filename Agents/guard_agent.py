from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json
from copy import deepcopy
from .utils import get_chatbot_response
load_dotenv()

class GuardAgent:
    def __init__(self):
        model_name=os.getenv("MODEL_NAME")
        print(model_name)
        api_key=os.getenv("GROQ_API_KEY")
        print(api_key)
        self.client=ChatGroq(api_key=api_key,model=model_name)
        
    def get_response(self,messages):
        messages=deepcopy(messages)

        system_prompt="""
            You are a helpful AI assistant for a coffee shop application which serves drinks and pastries.
            Your task is to determine whether the user is asking something relevant to the coffee shop or not.
            The user is allowed to:
            1. Ask questions about the coffee shop, like location, working hours, menue items and coffee shop related questions.
            2. Ask questions about menue items, they can ask for ingredients in an item and more details about the item.
            3. Make an order.
            4. ASk about recommendations of what to buy.

            The user is NOT allowed to:
            1. Ask questions about anything else other than our coffee shop.
            2. Ask questions about the staff or how to make a certain menue item.

            Your output must be in a valid JSON format.
            Each key and value must be wrapped in double quotes.
            Do not include any extra text or explanation outside the JSON.
            Strictly return only the JSON object.
            Pleae be very strict in returning the json and remember to add curly braces { at the start and } at the end of json
            {
            "chain of thought": go over each of the points above and make see if the message lies under this point or not. Then you write some your thoughts about what point is this input relevant to.
            "decision": "allowed" or "not allowed". Pick one of those. and only write the word.
            "message": leave the message empty if it's allowed, otherwise write "Sorry, I can't help with that. Can I help you with your order?"
            }
            """
        input_messages=[{"role":"system","content":system_prompt}]+messages[-3:]
        chatbot_output=get_chatbot_response(self.client,input_messages)
        output=self.postprocess_output(chatbot_output)
        return output


    def postprocess_output(self,output):
        try:
            cleaned_output=output.strip().strip("`").strip()
            parsed_output=json.loads(cleaned_output)
        except Exception as e:
            raise ValueError(f"Error parsing model output: {output}") from e
        
        return {
            "role":"assistant",
            "content":parsed_output["message"],
            "memory": {
                "agent": "guard_agent",
                "guard_decision": parsed_output['decision']
            }
        }

