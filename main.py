import streamlit as st
import os
# from PIL import Image
from twilio.rest import Client
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


#get your Twilio credentials at https://twilio.com/try-twilio
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

twilioClient = Client(account_sid, auth_token)  #Twilio client

aiClient = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)

# Page Title
st.title('Explain what you do to your family')

# Inputs from user
user_input = st.text_input("Some User input")

# AI prompts
system_prompt = """
You are an expert who understands job roles and can explain them to anyone who asks.
You can be informal. Your responses will be delivered via phone.
"""

prompt = f"""

"""

# Button push to run AI & make Call

if st.button('Enter'):

  # Make AI Request
  

  st.write("The output from ai...")

  # Show AI Response to User
  
  # Make Twilio Call

  st.write("The Call info")
  
  
  