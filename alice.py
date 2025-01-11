from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
import time
import streamlit as st

def main():
    st.title("chat with Alice")
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
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    user_input = st.chat_input("say something...!!")
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role":"user","content":user_input})

        with st.chat_message("assistant"):
           response = chain.invoke({"text":user_input})
           st.markdown(response.content)
        st.session_state.messages.append({"role":"assistant","content":response.content})



if __name__ == "__main__":
    main()
