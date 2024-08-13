import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()

    engine.setProperty('rate', 150)  
    engine.setProperty('volume', 1.0)  

    # Speak the text
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    text = "Hello, welcome to text to speech conversion using Python!"
    
    # Convert text to speech
    text_to_speech(text)
