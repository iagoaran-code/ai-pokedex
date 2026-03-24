import streamlit as st
from Pokemon_Project import PokedexOrchestrator

# Page setup
st.set_page_config(page_title="AI Pokedex", page_icon="🔴")
st.title("🔴 AI Pokedex")
st.markdown("Ask anything about Pokemon")


# Cache
@st.cache_resource
def get_pokedex():
    return PokedexOrchestrator(csv_path="pokemon.csv")


pokedex = get_pokedex()

# Chats history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = pokedex.get_answer(prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
