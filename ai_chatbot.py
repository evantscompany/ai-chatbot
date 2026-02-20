import streamlit as st
from google import genai
from google.genai import types
import datetime

# API KEY
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Key not found.")
    st.stop()

client = genai.Client(api_key=api_key)

# HyperParameter
config = types.GenerateContentConfig(
    max_output_tokens=300,
    response_mime_type='text/plain',
    system_instruction="""
    You are a charming, sweet, and friendly AI girl.
    Speak in a cute and warm tone.
    Keep responses under 100 words.
    """
)

# --------------------------------------
def get_ai_response(question):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=question,
        config=config
    )
    return response.text


def get_today():
    now = datetime.datetime.now()
    return {
        'location': 'Korea, Seoul',
        'year': now.year,
        'month': now.month,
        'day': now.day
    }

# --------------------------------------

st.set_page_config(
    page_title='AI chatbot',
    page_icon='./logo/logo_chatbot.png'
)

col1, col2 = st.columns([1.2, 4.8])

with col1:
    st.image("./logo/logo_chatbot.png", width=200)

with col2:
    st.markdown(
        """
        <h1 style='margin-bottom:0'>AI Chat Bot</h1>
        <p style='margin-top:0; color:gray'>
        상냥하고 귀여운 챗봇과 즐거운 채팅을 해보세요 💕
        </p>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {'role': 'assistant', 'content': 'Hi there~ Ask me anything 💗'}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

question = st.chat_input('Ask me something...')
if question:
    st.session_state.messages.append({'role': 'user', 'content': question})
    st.chat_message('user').write(question)

    with st.spinner('She is thinking... 💭'):
        response = get_ai_response(question)
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.chat_message('assistant').write(response)