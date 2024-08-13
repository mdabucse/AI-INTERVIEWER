import google.generativeai as genai
from PyPDF2 import PdfReader
from langchain.memory import ChatMessageHistory

# Function to extract text from a PDF file
def extract_pdf(path):
    reader = PdfReader(path)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()
    return extracted_text

# Initialize generative AI model
genai.configure(api_key="AIzaSyBxiikGl4VBeMuV692el6GK9adhkLNnaX0")
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize chat history
chat_history = ChatMessageHistory()

# Function to generate prompt based on chat history and resume content
def generate_prompt(chat_history, resume_content):
    prompt = f"""
        You are an Expert Interviewer to Interview a Candidate Based On their Skills Technology Stack And Project Related Questions
        Based on that First Ask Questions from the "Tell me about yourself" After That Based On their responce And Resume Content You Ask Questions
        Eg:"What are Techinicals Skills You Have?"
        Like That 
        This is The Previous Content Provided by the Candidate Response {chat_history.messages}
        This is the Content from the Resume 
        {resume_content}
        Based On this Response and Resume Content Ask Questions Alone do not provide any Additional Contents Give Only One Question After This Prompt Calling Give Another Question
    """
    return prompt

# Path to the resume PDF file
resume_path = r'Mohamed_Abubakkar_S_22AD051.pdf'
resume_content = extract_pdf(resume_path)

# Initial prompt to start the interaction
initial_prompt = generate_prompt(chat_history, resume_content)

# Add AI-generated response to chat history
response = model.generate_content(initial_prompt)
print(response.text)
chat_history.add_ai_message(response.text)

# User input loop
while True:
    user_input = input("Enter Your Prompt or 'q' to Exit: ")
    if user_input.lower() == 'q':
        break
    chat_history.add_user_message(user_input)

    # Generate response based on updated chat history
    response = model.generate_content(generate_prompt(chat_history, resume_content))
    print("The Prompt is\n", initial_prompt)
    print("This is The Response \n", response.text)
    chat_history.add_ai_message(response.text)
