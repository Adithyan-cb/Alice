from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
import time
import streamlit as st


def main():
    title = """
        <h1 style="text-align:center">Alice</h1>
    """
    st.html(title)
    st.warning("Note : Alice is curently under development",icon="⚠️")
    Alice = ChatGroq(api_key=os.getenv("GROQ_API_KEY"),model="llama3-8b-8192")
        
    file = open("personality.txt","r")

    system = file.read()
    file.close()

    human = "{text}"

    prompt = ChatPromptTemplate.from_messages([("system",system),("user",human)])
    chain = prompt | Alice

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"],avatar=message["avatar"]):
            st.markdown(message["content"])
    
    user_input = st.chat_input("say hi to alice...")

    user_img = "images/user.png"
    alice_img = "images/Alice.jpeg"
    if user_input:
        # display user message
        with st.chat_message("user",avatar=user_img):
            st.markdown(user_input)
        st.session_state.messages.append({"role":"user",
                                          "content":user_input,
                                          "avatar":user_img
                                          })
        # context
        context = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages]
        )

        combined_input = f"{context}\nUser: {user_input}"
        
        # display alice message 
        with st.chat_message("assistant",avatar="images/Alice.jpeg"):
           response = chain.invoke({"text":combined_input})
           st.markdown(response.content)
        st.session_state.messages.append({"role":"assistant",
                                          "content":response.content,
                                          "avatar":alice_img,
                                          })



if __name__ == "__main__":
    main()
