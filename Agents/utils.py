def get_chatbot_response(client,messages,temperature=0):
    input_messages=[]
    for message in messages:
        input_messages.append({"role":message["role"],"content":message["content"]})

        response=client.invoke(input=input_messages,temperature=temperature)

    return response.content


def get_embedding(model,user_prompt):
    embedding=model.encode(user_prompt)
    return embedding.tolist()