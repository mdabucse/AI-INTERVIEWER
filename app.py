import streamlit as st
from speech_recognizer import Speech_recognizer
from audio_capture import start_recording, stop_recording
from question import AskQuestions
from text_to_speech import text_to_speech
from grade import Get_Results

def rainbow_title(text):
    colors = ['#FF5733', '#FFBD33', '#DBFF33', '#75FF33', '#33FF57', '#33FFBD', '#33DBFF', '#3357FF', '#5733FF', '#BD33FF']
    rainbow_text = ''.join(f'<span style="color:{colors[i % len(colors)]};">{char}</span>' for i, char in enumerate(text))
    return rainbow_text

# Create a two-column layout
col1, col2 = st.columns([1, 5])

with col1:
    st.image("logo.png", width=100)  # Adjust the width as needed

with col2:
    st.markdown(f"<h1 style='text-align: left;'> {rainbow_title('AI Interviewer')} </h1>", unsafe_allow_html=True)

st.sidebar.title("Techiee Hackers")

logo_url = "logo.png"
st.sidebar.image(logo_url, width=150)

st.sidebar.header("Meet Our Team")
st.sidebar.write("**Mohamed Abubakkar S**")
st.sidebar.write("**Kishore E**")
st.sidebar.write("**Kamal Gant S**")
st.sidebar.write("**Aadithya S**")

st.markdown("<hr style='border-color: #FF5733; height: 5px;'>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
global file_path

if uploaded_file is not None:
    st.write(f"Uploaded file: {uploaded_file.name}")
    file_path = f"./{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.write(f"File saved at: {file_path}")

    # Initialize session state for recording control and conversation state
    if 'recording' not in st.session_state:
        st.session_state.recording = False
    if 'recording_thread' not in st.session_state:
        st.session_state.recording_thread = None
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    if 'result' not in st.session_state:
        st.session_state.result = []

    # Create two columns for Start and Stop buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Start Conversation"):
            st.write("Conversation started!")
            filename = "output.wav"
            st.session_state.recording_thread = start_recording(filename)
            st.session_state.recording = True
            st.session_state.conversation_started = True
    recognizer = ''
    with col2:
        if st.session_state.recording and st.button("Stop Recording"):
            stop_recording()
            if st.session_state.recording_thread is not None:
                st.session_state.recording_thread.join()
            st.write("Recording stopped!")
            st.session_state.recording = False

            # Initialize speech recognizer with the recorded file
            recognizer += Speech_recognizer('output.wav')
            st.session_state.result.append(recognizer)

    if st.session_state.conversation_started:
        questions = AskQuestions(recognizer, file_path)
        st.write(questions)
        text_to_speech(questions)

    if st.button("Get Score"):
        score = Get_Results(st.session_state.result)
        st.write(f"Score: {score}")
