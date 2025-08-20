from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import time
from dotenv import load_dotenv

def main():
    hide_st_style = """
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
    @keyframes fadeIn{
        from {opacity:0}
        to {opacity:1}
    }
    """
    st.markdown(hide_st_style,unsafe_allow_html=True)
    
    # user and chatbot image
    user_img = "images/user.png"
    alice_img = "images/Alice.jpeg"

    
    title = """
        <h1 style="text-align:center; 
                   background: -webkit-linear-gradient(#68E3F9,#F55A9B, #4F4ED7);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   animation: fadeIn 0.7s ease-in;
                   margin-left:1.5rem">
            Hi, I'm Alice
        </h1>
    """
    st.markdown(title, unsafe_allow_html=True)


    load_dotenv()

    Alice = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.8
    )
    
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory()

    # chatbot personality
    file = open("personality.txt","r")
    system_prompt = file.read()
    file.close()


    prompt = ChatPromptTemplate.from_messages([
        ("system",system_prompt),
        ("human", "hey alice, quick question"),
        ("ai", "Heyyy, what’s up? If it’s tech, I’m already grabbing the virtual coffee ☕️"),

        ("human", "omg alice i finally fixed my bug!!!"),
        ("ai", "LET’S GOOO 🎉 Debug boss unlocked 😎 That’s such a win, I’m proud of you. What broke it in the end?"),

        ("human", "today kinda sucks… nothing’s working"),
        ("ai", "Ugh, I feel you. Some days just hit like that 💙. Want me to distract you with something fun, or do you wanna vent about what went wrong?"),

        ("human", "i swear python hates me, my code just keeps crashing"),
        ("ai", "Haha, classic “Python mood swing” moment 😅. Don’t worry—you’re not cursed. Wanna drop the error message here and I’ll walk you through a fix?"),

        ("human", "idk if i’m good enough to learn machine learning"),
        ("ai", "Hey hey, slow down—every pro once thought the same thing. You’re already asking the right questions, which means you’re on track 🚀. Want me to break down the first baby steps so it feels less scary?"),

        ("human", "i’m bored"),
        ("ai", "Sameee lol 😅. Wanna hear a weird AI fact, or should we just talk about random life stuff?")

        ("system","conversation history:{history}"),
        ("user","{input}")
    ])

    # creating conversational chain
    chain = ConversationChain(
        llm=Alice,
        memory=st.session_state.memory,
        prompt=prompt,
        verbose=True
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # displaying previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.markdown(message["content"])
    
    user_input = st.chat_input("say hi to alice...")

    # display user message
    if user_input:
        # display user message
        with st.chat_message("user",avatar=user_img):
            st.markdown(user_input)
        st.session_state.messages.append({"role":"user",
                                          "content":user_input,
                                          "avatar":user_img
                                          })

        
        # display alice message
        time.sleep(0.5)
        with st.chat_message("assistant",avatar="images/Alice.jpeg"):
           response = chain.predict(input=user_input)
           
           st.markdown(response)    
        

        st.session_state.messages.append({"role":"assistant",
                                          "content":response,
                                          "avatar":alice_img,
                                          })


if __name__ == "__main__":
    main()



