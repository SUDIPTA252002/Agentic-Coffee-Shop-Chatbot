from Agents import GuardAgent,ClassificationAgent
import os

def main():
    pass

if __name__=="__main__":
    guard_agent=GuardAgent()
    classification_agent=ClassificationAgent()

    messages=[]
    while True:
        # os.system('cls' if os.name=='nt' else 'clear')
        print("\n\nPrint Messages ...............")
        for message in messages:
             print(f"{message['role'].capitalize()}: {message['content']}")

        prompt=input("USER: ")
        messages.append({"role":"user","content":prompt})

        guard_agent_response=guard_agent.get_response(messages)
        print("GUARD AGENT OUTPUT: ",guard_agent_response)
        input("\nPress Enter to continue...")
        
        # Clear screen AFTER user has seen output and pressed Enter
        # os.system('cls' if os.name=='nt' else 'clear')

        if(guard_agent_response["memory"]["guard_decision"]=="not allowed"):
            messages.append(guard_agent_response)    
            continue
        classification_agent_response=classification_agent.get_respnse(messages)
        chosen_agent=classification_agent_response["memory"]["classification_decision"]
        print("Chosen Agent:",chosen_agent)
        input("\nPress Enter to continue...")
        
        # Clear screen AFTER user has seen output and pressed Enter
        # os.system('cls' if os.name=='nt' else 'clear')



