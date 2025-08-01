from flask import Flask, request, render_template, jsonify, session
from google.cloud import dialogflow_v2 as dialogflow
import os
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Set path to your Dialogflow service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "nexora-uman-692f0694bd0c.json"
DIALOGFLOW_PROJECT_ID = "nexora-uman"
LANGUAGE_CODE = "en"

# Dialogflow response handler
def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result.fulfillment_text

@app.route('/', methods=['GET', 'POST'])
def chat():
    if 'messages' not in session:
        session['messages'] = []
    if request.method == 'POST':
        user_input = request.form['message']
        session_id = str(uuid.uuid4())
        reply = detect_intent_texts(DIALOGFLOW_PROJECT_ID, session_id, user_input, LANGUAGE_CODE)
        session['messages'].append({'sender': 'user', 'text': user_input})
        session['messages'].append({'sender': 'bot', 'text': reply})
    return render_template('index.html', messages=session.get('messages', []))

if __name__ == '__main__':
    app.run(debug=True)
