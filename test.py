import streamlit as st


st.title("echo bot")

if "message" not in st.session_state:
    st.session_state.message = []


for message in st.session_state.message:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

inp = st.chat_input("say something..!!")

if inp:
    with st.chat_message("user"):
        st.markdown(inp)
    
    st.session_state.message.append({"role":"user","content":inp})

    with st.chat_message("assistant"):
        response = f"echo:{inp}"
        st.markdown(response)
    
    st.session_state.message.append({"role":"assistant","content":response})