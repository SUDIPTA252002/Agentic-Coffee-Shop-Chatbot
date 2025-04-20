from Agents import GuardAgent
import os

def main():
    pass

if __name__=="__main__":
    guard_agent=GuardAgent()
    messages=[]
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        print("\n\nPrint Messages ...............")
        for message in messages:
             print(f"{message['role'].capitalize()}: {message['content']}")

        prompt=input("USER: ")
        messages.append({"role":"user","content":prompt})

        guard_agent_response=guard_agent.get_response(messages)
        print("GUARD AGENT OUTPUT: ",guard_agent_response)
        messages.append(guard_agent_response)
