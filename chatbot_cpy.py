from flask import Flask, render_template, request, json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException

app = Flask(__name__)

app.static_folder = 'static'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')

    # API
    authenticator = IAMAuthenticator('{apikey}')
    assistant = AssistantV2(
        version='{version}',
        authenticator=authenticator
    )

    assistant.set_service_url('{url}')
    assistant.set_disable_ssl_verification(True)
    assistant.set_default_headers({'x-watson-learning-opt-out': "true"})

    session = assistant.create_session(
        assistant_id='{assistant_id}').get_result()

    response = assistant.message(
        assistant_id='{assistant_id}',
        session_id=session['session_id'],
        input={
            'message_type': 'text',
            'text':  userText
        }
    ).get_result()

    print(json.dumps(response, indent=2))
    return response["output"]["generic"][0]["text"]


if __name__ == '__main__':
    app.run(debug=True)
