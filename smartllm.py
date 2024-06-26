import os
import json
import streamlit as st
import google.generativeai as genai
import time
import warnings

# To ignore all warnings
warnings.filterwarnings("ignore")

# Define company information
company_info = {
    "about": "DataposIT Limited is a leading IT solutions integrator specializing in business applications, infrastructure, managed services, and IT consultancy services. The company is dedicated to providing state-of-the-art IT solutions to its clients and is capable of both informing and implementing complex solutions for businesses of all sizes",
    "team": "The team at DataposIT Limited is comprised of highly trained professionals whose collective IT industry knowledge makes the company one of the premier IT firms in the region",
    "mission": "DataposIT Limited aims to add substantial value by providing Information Technology solutions that address the requirements of its clients today while simultaneously being dynamic enough to cater for the needs of the future",
    "vision_and_values": "The company believes in Value Creation through providing industry-leading solutions resulting in Customer Satisfaction. They encourage Teamwork to effectively and efficiently meet their goals and objectives. Integrity is their most valued asset and they take Accountability to their clients earnestly.",
    "leadership": {
        "CEO": "Kariuki Kinyanjui",
        "CTO": "Aaron Mbowa",
        "CFO": "Nadia Sumar"
    },
    "clients": "DataposIT Limited serves a diverse range of sectors including Banking, Healthcare Services, Professional Services...",
    "partnerships": {
        "business_apps": ["Microsoft Silver Partner", "MicroStrategy implementation partner and reseller"],
        "infrastructure": ["VMware Certified Professional Cloud", "VMware Partner Enterprise Solution Provider", "VEEAM Gold Partner", "VEEam Cloud and SERVICE PROVIDER", "NetAPP Gold Partner", "Citrix Partner Silver Solution Advisor"]
    }
}

# Configure the API key for genai
API_KEY = "AIzaSyDka3NcQmGov-lxU-bKLCjg2fus_dVEe30"
genai.configure(api_key=API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel(model_name="models/gemini-pro")

# Initialize a variable to hold the context of the conversation
conversation_context = ""

# Define a function to handle user queries and generate responses
# Define a function to handle user queries and generate responses
def respond_to_query(query, check_keywords=False):
    global conversation_context
    query = query.lower()  # Convert the query to lower case
    print("Query:", query)  # Add this line to see the query being processed

    # Check if the query contains any of the company information keys
    for key, value in company_info.items():
        print("Checking key:", key)  # Add this line to see which key is being checked
        if key in query:
            # If it does, return the corresponding value
            return value
        if isinstance(value, dict):
            # If the value is a dictionary, check if the query contains any key in this dictionary
            for sub_key, sub_value in value.items():
                print("Checking sub-key:", sub_key)  # Add this line to see which sub-key is being checked
                if sub_key in query:
                    return sub_value

    # If the query doesn't match any of the predefined keys, use the Gemini model to generate a response
    instructions =  "Instructions: Respond to the query."
    message = f"Instructions:{instructions} Message description: {conversation_context} {query}"
    response = model.generate_content(message).text
    # Update the conversation context
    conversation_context += " " + response

    return response
# Define a function to load the chat history from a file
def load_chat_history():
    if os.path.exists("chat_history.json"):
        with open("chat_history.json", "r") as f:
            return json.load(f)
    else:
        return []

# Define a function to save the chat history to a file
def save_chat_history(chat_history):
    with open("chat_history.json", "w") as f:
        json.dump(chat_history, f)

# Streamlit code starts here
st.title("DatapositAI")

# Load the chat history at the start of the app
st.session_state.messages = load_chat_history()

# Display chat history
for message in st.session_state.messages:
    with st.empty():
        st.markdown(f"**{message['role'].capitalize()}:** {message['content']}")

# Get user input
user_message = st.text_input("What do you want to know about DataposIT? Type here:")

# Add a button to trigger the bot's response
if st.button('Send'):
    # Display user input in conversation area
    st.markdown(f"**You:** {user_message}")

    # Get bot response
    bot_response = respond_to_query(user_message)

    # Display bot response in conversation area
    st.markdown(f"**Bot:** {bot_response}")

    # Save messages to session state
    st.session_state.messages.append({"role": "user", "content": user_message})
    st.session_state.messages.append({"role": "bot", "content": bot_response})

    # Save the chat history
    save_chat_history(st.session_state.messages)
