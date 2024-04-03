import os
import openai
from dotenv import loaddotenv
import random
from flaskcors import CORS




app = Flask(name)
CORS(app)
loaddotenv()
openai.apikey = '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'

def get_openai_response(prompt_text):
    """
    Function to get a response from OpenAI's chat model.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Specify the chat model you're using
            messages=[
                {"role": "user", "content": prompt_text}
            ]
        )
        original_response = response.choices[0].message['content'].strip()
        personalized_response = personalized_response(original_response)
        return personalized_response
    except Exception as e:
        return f"An error occurred: {str(e)}"

def personalized_response(response_text):
    """Modify response to reflect the chatbot's snobby responsability"""
    snobby_additions = [
        "Well, of course, that's the only sensible option.",
        "I suppose you wouldn't know, but it's quite obvious.",
        "Ah, finally, a question  woth my time"
    ]

@app.route('/chat', methods=['POST', 'GET'])
def chat():
    if request.method == "POST":
        data = request.json
        prompt_text = data.get('message')
        if not prompt_text:
            return jsonify({"error": "No message provided"}), 400
        response_text = get_openai_response(prompt_text)
        return jsonify({"response": response_text})
    else:
        return jsonify({"message": "Get requests are not supported for this endpoint."})



if __name == "__main":
    app.run(debug=True)
