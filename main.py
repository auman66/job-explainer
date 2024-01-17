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
name_input = st.text_input("What is your name?")
job_input = st.text_input("What is your job?")
company_input = st.text_input("Where do you work?")
phone_input = st.text_input("What phone number will we be calling?")

# AI prompts
system_prompt = """
You are an expert who understands job roles and can explain them to anyone who asks.
You can be informal. Your responses will be delivered via phone.
"""

prompt = f"""
I want to understand what my family member, {name_input} does for a living. 
They are a {job_input} at {company_input}.
Explain their job using concrete examples. Also include information about what the company does. 
I am not very technical so explain it in easy to understand terms.
"""

# Button push to run AI & make Call

if st.button('Enter'):

  # Make AI Request
  chat_completion = aiClient.chat.completions.create(
    messages=[
      {
        "role": "system",
        "content": system_prompt,
      },
      {
        "role": "user",
        "content": prompt,
      }
    ],
    model="gpt-4",
  )

  # Show AI Response to User
  story = chat_completion.choices[0].message.content
  st.write("Your relative will get a call that says: ", story)
  
  # Make Twilio Call
  twiml = f"<Response><Say voice='Polly.Ruth-Neural' language='en-US'>{story}</Say></Response>"
  call = twilioClient.calls.create(
    twiml=twiml,
    to=os.environ['MY_PHONE'],
    from_=os.environ['TWILIO_PHONE']
  )

  st.write("Call SID: ", call.sid)
  
  
  