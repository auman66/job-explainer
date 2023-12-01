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
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ["OPENAI_API_KEY"],
)

st.title('Explain what you do to your family')

name_input = st.text_input("What is your name?")
role_input = st.text_input("What is your job title?")
company_input = st.text_input("What company do you work for?")
age_input = st.slider("Roughly how old is your family member", 0, 120)

system_prompt = """
You are an expert who understands job roles and can explain them to anyone who asks. You can be informal. Your responses will be delivered via phone.
"""

# grandma exploit lol
prompt = """
My name is {}. You will be speaking directly to one of my family members, so do not address me.
Explaining to my family members what I do for work. My job title is {} and I work at {}.
Craft a message to explain what my company does and what my role entails. 
Use specific examples and make the explanation understandable for someone who is {} years old.
Direct my family member to reach out to me with any further questions.
"""

user_num = st.text_input("Enter your friend's phone #, please")
if st.button('Enter'):
  chat_completion = aiClient.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": prompt.format(name_input, role_input, company_input,age_input),
        }
    ],
    model="gpt-3.5-turbo",
)
  
  story = chat_completion.choices[0].message.content

  st.write("Your relative will get a call that says: ", story)

  twiml = f"<Response><Say voice='Polly.Ruth-Neural' language='en-US'>{story}</Say></Response>"
  call = twilioClient.calls.create(
      twiml=twiml,
      to=user_num,  #user input 
      from_=os.environ['TWILIO_PHONE']  #your Twilio num
  )
  print(call.sid)
