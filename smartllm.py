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
def respond_to_query(query, check_keywords=False):
    global conversation_context
    query = query.lower()  # Convert the query to lower case

    # Define a list of ERP and infrastructure-related keywords
    erp_keywords = ["erp", "microsoft business central", "business central", "enterprise resource planning"]
    infrastructure_keywords = ["vmware", "veeam", "netapp", "citrix", "infrastructure"]

    # Check if the query contains any of the ERP or infrastructure-related keywords
    if check_keywords and not any(keyword in query for keyword in erp_keywords + infrastructure_keywords):
        # If the query doesn't contain any of the ERP or infrastructure-related keywords, return a default message
        return "I'm sorry, I can only provide information on ERPs and infrastructure."

    # Check if the query is in the company_info dictionary
    if query in company_info:
        # If it is, return the corresponding value
        return company_info[query]

    # If the query doesn't match any of the predefined ones, use the Gemini model to generate a response
    instructions =  "Instructions: Respond to the query."
    message = f"Instructions:{instructions} Message description: {conversation_context} {query}"
    response = model.generate_content(message).text
    # Update the conversation context
    conversation_context += " " + response

    return response

# Streamlit code starts here
st.title("DatapositAI")

# Greet the user
st.write("Welcome to PositAI! How can I assist you today?")

# Define the options for the dropdown menu
options = ["About", "Team", "Mission", "Vision and Values", "Leadership", "Clients", "Partnerships"]

# Create the dropdown menu and get the selected option
selected_option = st.selectbox("Choose an option:", options)

# Get bot response for the selected option
bot_response = respond_to_query(selected_option)

# Display bot response
st.write(bot_response)

# Get user input
user_message = st.text_input("Do you need additional help? If yes, please type your issue below:")

# Add a button to trigger the bot's response
if st.button('Send'):
    # Display user input in conversation area
    st.markdown(f"**You:** {user_message}")

    # Get bot response
    bot_response = respond_to_query(user_message, check_keywords=True)

    # Display bot response in conversation area
    st.markdown(f"**Bot:** {bot_response}")
