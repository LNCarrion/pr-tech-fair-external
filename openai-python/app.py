from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import openai
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)  # This will allow CORS for all routes

# Retrieve environment variables
endpoint = os.environ.get("AZURE_ENDPOINT")
api_key = os.environ.get("AZURE_API_KEY")
deployment = os.environ.get("AZURE_DEPLOYMENT")
search_endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT")
search_api_key = os.environ.get("AZURE_SEARCH_API_KEY")
search_index_name = os.environ.get("AZURE_SEARCH_INDEX_NAME")

client = openai.AzureOpenAI(
    base_url=f"{endpoint}/openai/deployments/{deployment}/extensions",
    api_key=api_key,
    api_version="2023-08-01-preview",
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message')

    completion = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "user",
                "content": message,
            },
        ],
        extra_body={
            "dataSources": [
                {
                    "type": "AzureCognitiveSearch",
                    "parameters": {
                        "endpoint": search_endpoint,
                        "key": search_api_key,
                        "indexName": search_index_name
                    }
                }
            ]
        }
    )

    response = [choice.message.content for choice in completion.choices if choice.message.role == "assistant"]
    return jsonify({'response': response[0] if response else ''})

if __name__ == '__main__':
    app.run(debug=True)
