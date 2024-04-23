import streamlit as st
import google.generativeai as genai
import time
import warnings

# To ignore all warnings
warnings.filterwarnings("ignore")

# Define a dictionary to hold the information about your company
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
def respond_to_query(query):
    global conversation_context
    query = query.lower()  # Convert the query to lower case

    # Check for keywords in the query and respond accordingly
    if "company" in query or "business" in query or "organization" in query:
        response = company_info["about"]
    elif "team" in query or "staff" in query or "employees" in query:
        response = company_info["team"]
    elif "leadership" in query or "executives" in query or "management" in query:
        response = "The leadership team of DataposIT Limited consists of:\n"
        for role, leader in company_info["leadership"].items():
            response += f"- {role}: {leader}\n"
    elif "partnerships" in query or "affiliations" in query:
        response = "Our company has the following partnerships:\n"
        response += "\nBusiness Apps Partnerships:\n"
        for partner in company_info["partnerships"]["business_apps"]:
            response += f"- {partner}\n"
        response += "\nInfrastructure Partnerships:\n"
        for partner in company_info["partnerships"]["infrastructure"]:
            response += f"- {partner}\n"
    else:
        # If the query doesn't match any of the predefined ones, use the Gemini model to generate a response
        instructions =  "Instructions: Respond to the query."
        message = f"Instructions:{instructions} Message description: {conversation_context} {query}"
        response = model.generate_content(message).text
        # Update the conversation context
        conversation_context += " " + response

    return response


# Streamlit code starts here
st.title("PositAI")
# Main loop: wait for the user to input a message, respond using the chatbot
user_message = st.text_input("User")
if user_message:
    chatbot_response = respond_to_query(user_message)
    st.markdown(f"**Chatbot:** {chatbot_response}")
