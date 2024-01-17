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

# Add as I write the prompt 
# Inputs from user
name_input = st.text_input("What is your name?")
role_input = st.text_input("What is your job title?")
company_input = st.text_input("What company do you work for?")
age_input = st.slider("Roughly how old is your family member", 0, 120)

# AI prompts
# Start with basic prompt and itterate
system_prompt = """
You are an expert who understands job roles and can explain them to anyone who asks. You can be informal. Your responses will be delivered via phone.
"""

# Use f_string - may need to move where this is created
# change prompt to be in "me" perspective from the family member. "describe to me what my relative, Alex, does"
prompt = f"""
I want to understand what my family member, {name_input} does for a living. They are a {job_input} at {company_input}.
Explain their job using concert examples. Also include information about what the company does. 
I am not very technical so explain it in easy to understand terms.
"""

# Button push to run AI & make Call
user_num = st.text_input("Enter your friend's phone #, please")
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
  # Try out Cloudflair's llama2 API
  story = chat_completion.choices[0].message.content

  # Show AI Response to User
  st.write("Your relative will get a call that says: ", story)

  # Make Twilio Call
  twiml = f"<Response><Say voice='Polly.Ruth-Neural' language='en-US'>{story}</Say></Response>"
  call = twilioClient.calls.create(
      twiml=twiml,
      to=os.environ['MY_PHONE'],  #user input 
      from_=os.environ['TWILIO_PHONE']  #your Twilio num
)
  print(call.sid)
