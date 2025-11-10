import pyttsx3

# Initialize only once (globally)
engine = pyttsx3.init()
engine.setProperty('rate', 175)
engine.setProperty('volume', 1)

# Desired voice gender; you may change to "male" if preferred
desired_gender = "female"
voices = engine.getProperty('voices')
selected_voice = voices[0].id  # default

# Try to find a suitable female voice by inspecting voice properties
for v in voices:
    if desired_gender.lower() in v.name.lower() or desired_gender.lower() in v.id.lower():
        selected_voice = v.id
        break
engine.setProperty('voice', selected_voice)

def speak(text):
    # Use the globally initialized engine
    engine.say(text)
    engine.runAndWait()