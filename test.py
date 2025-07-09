import google.generativeai as genai

# Replace this with your actual Gemini API key
api_key = "AIzaSyAkcL5USwFnTfwDpt6NFwyu3Q5G7EFgIlk"

# Configure the API
genai.configure(api_key=api_key)

# Create the model
try:
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")  # Use 1.5 for chat support
    chat = model.start_chat(history=[])

    print("Gemini Chatbot is ready! Type 'exit' to end the conversation.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Gemini: Goodbye!")
            break
        
        response = chat.send_message(user_input)
        print("Gemini:", response.text)

except Exception as e:
    print("Error while connecting to Gemini API:", e)
