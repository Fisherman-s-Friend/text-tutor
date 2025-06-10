from flask import Flask, request, jsonify
from flask_cors import CORS
from translation_utils import translate
from dictionary_utils import define_word, get_synonyms, get_dependency_and_pos
from LLM_utils import rephrase
from mapping_dicts import iso_dict, features_dict
from flask_sqlalchemy import SQLAlchemy
from DB import db, Users, Requests
import sys


# --------------------------------------------------------------------------#
# TODO: CHANGE THE PASSWORD TO THE PASSWORD YOU SET FOR THE POSTGRES DATABASE
# TODO: CHANGE THE DATABASE NAME TO THE NAME OF THE DATABASE YOU CREATED
DB_name = ""
pw = ""
# --------------------------------------------------------------------------#


app = Flask(__name__)
CORS(app, origins="http://localhost:3000")

# Configure SQLAlchemy


app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://postgres:{pw}@localhost/{DB_name}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
    False  # Disable modification tracking to suppress a warning
)

db.init_app(app)
with app.app_context():
    db.create_all()


RQ_data = []


@app.route("/requests/<username>", methods=["GET"])
def get_user_requests(username):
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    user_requests = Requests.query.filter_by(username=username).all()
    if not user_requests:
        return jsonify({"message": "No requests found for this user"}), 200

    requests_data = [
        {"id": request.id, "data": request.request_data} for request in user_requests
    ]
    return jsonify({"requests": requests_data}), 200


@app.route("/signin", methods=["POST"])
def signin():
    # Get data from request
    print(request.json)
    print(type(request.json))
    data = request.json
    username = data.get("username")
    email = data.get("email")

    # Find user in the database
    user = Users.query.filter_by(username=username).first()

    # Check if the user exists and the email matches
    if user and user.email == email:
        return jsonify({"message": "Sign in successful"}), 200
    # if the user exists but the email does not match
    elif user and user.email != email:
        return jsonify({"error": "Invalid username or email"}), 401
    # if the user does not exist
    else:
        signup(username, email)


from flask import jsonify


@app.route("/request/<selected_value>", methods=["GET"])
def get_request(selected_value):
    global RQ_data

    # Query the database to get the language and extra data for the selected request
    request_info = Requests.query.filter_by(request_data=selected_value).first()

    if request_info:
        # Get the language and extra data
        language = request_info.request_language
        extra_data = request_info.get_request_data_extra_as_json()
        RQ_data = extra_data

        return jsonify({"language": language, "extra_data": extra_data})
    else:
        return jsonify({"error": "Request not found"}), 404


@app.route("/tokens", methods=["POST"])
def write_to_db():
    data = request.json
    print("Data: ", data)
    username = data.get("username", "")
    request_data = data.get("text", "")
    request_data_extra = data.get("tokens", "")
    request_language = data.get("inputLanguage", "")

    print("-" * 50)
    print(f"Username: {username}")
    print(f"Request data: {request_data}")
    print(f"Request language: {request_language}")
    print(f"Request data extra: {request_data_extra}")

    # Create a new Request object
    new_request = Requests(
        username=username,
        request_data=request_data,
        request_language=request_language,
        request_data_extra=request_data_extra,
    )
    print(new_request)
    print(type(new_request))
    print("-" * 50)

    # Add the new request to the database session only if the request_data is not yet in the database
    if not Requests.query.filter_by(request_data=request_data).first():
        db.session.add(new_request)

    try:
        # Commit the session to the database
        db.session.commit()
        return jsonify({"message": "Request saved successfully"}), 200
    except Exception as e:
        # If an error occurs, rollback the session
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


def signup(username, email):

    # Create a new user
    new_user = Users(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User signed up successfully"}), 200


submitted_text = ""
analysed_text = []
selection_start = 0
selection_end = 0
definitions = ""
synonyms = ""
POS = ""
DEP = ""


@app.route("/api", methods=["POST"])
def lang_data():
    global submitted_text
    global analysed_text
    global selection_start
    global selection_end
    global definitions
    global synonyms
    global POS
    global DEP

    data = request.get_json()
    input_text = data.get("text", "")
    input_lang = data.get("inputLanguage", "")
    input_lang_non_iso = iso_dict[input_lang]
    selected_language = data.get(
        "language", "en"
    )  # Default to English if no language specified
    selected_text = data.get("selectedText", "")
    selection_start = data.get("selectionStart", "")
    selection_end = data.get("selectionEnd", "")
    print(selection_start)
    print(selection_end)
    action = data.get("action", "")
    translated_text = translate(input_text, source=input_lang, dest=selected_language)
    lemma = translated_text

    if submitted_text != "":
        found_word = (
            False  # Set a flag to False to indicate that the word has not been found
        )
        for sentence in analysed_text.sentences:
            for word in sentence.words:
                if word.start_char == selection_start:
                    POS = word.pos
                    found_word = True  # Set the flag to True if the word is found
                    break  # Break out of the inner loop
            if found_word:
                break  # Break out of the outer loop if the word is found
    else:
        POS = "Text has not been submitted yet."

    if action == "translate":
        if selected_text:
            translated_text = translate(
                selected_text, source=input_lang, dest=selected_language
            )
        return jsonify({"translation": translated_text})

    elif action == "submit":
        submitted_text = data.get("text", "")
        analysed_text = get_dependency_and_pos(submitted_text, input_lang)
        print("done")
        return jsonify({"message": "Text submitted."})

    if action in ["define", "synonyms"]:
        if type(analysed_text) == list:
            print("REQUEST DATA", RQ_data)
            temp = analysed_text
            analysed_text = RQ_data
            print("SELECTED TEXT", input_text, len(input_text))
            for s in RQ_data:
                print(s), len(s["text"])
                if s["text"] == input_text.strip():
                    print("FOUND")
                    lemma = s["lemma"]
                    POS = s["POS"]
                    print(lemma)
                    break

        else:
            for s in analysed_text.sentences:
                for word in s.words:
                    if word.start_char == selection_start:
                        lemma = word.lemma
                        print(lemma)
                        break

    if action == "define":
        definitions = ", ".join(
            [
                f"{syn.name()}: {syn.definition()}"
                for syn in define_word(lemma, lang=input_lang_non_iso)
                if syn.name().split(".")[1].upper() == POS[0]
            ]
        )
        return jsonify({"definitions": definitions})

    elif action == "synonyms":
        synonyms = ", ".join(
            syn for syn in get_synonyms(lemma, POS, lang=input_lang_non_iso)
        )
        return jsonify({"synonyms": synonyms})

    elif action == "Rephrase":
        rephrased_text = rephrase(input_text)
        return jsonify({"Rephrase": rephrased_text})

    analysed_text = temp
    return


@app.route("/submit", methods=["POST"])
def process():
    # (1) Get the JSON data from the request
    data = request.get_json()
    # split the data into the text, input language, and selected language
    submitted_text = data.get("text", "")
    input_lang = data.get("inputLanguage", "")
    input_lang_non_iso = iso_dict[input_lang]
    output_lang = data.get(
        "language", "en"
    )  # Default to English if no language specified
    # _______________________________________________

    # (2) Analyse the submitted text using the Stanza library
    analysed_text = get_dependency_and_pos(submitted_text, input_lang)
    # _______________________________________________

    # (3) Create a helper function to find the head word text by its ID
    def find_head_word_text(sentence, head_id):
        for word in sentence.words:
            if (
                word.id == head_id
            ):  # Ensure this comparison works with your data structure; may need to convert types
                return word.text
        return "- (this is the root)"  # Fallback in case the head word is not found

    # (4) Return a list of dictionaries containing the POS, DEP, etc., for each word
    response_data = []
    for sentence in analysed_text.sentences:  # Loop over sentences first
        for word in sentence.words:  # Then loop over words in each sentence

            head_word_text = find_head_word_text(sentence, word.head)

            def modify_features(features):
                features = str(features)
                if features != "":
                    features = features.split("|")
                    features = [
                        feature.split("=")[1] for feature in features if "=" in feature
                    ]
                    return_val = ", ".join(
                        features_dict.get(feature, feature) for feature in features
                    )
                    print(return_val)
                    return return_val
                return "-"

            try:
                definitions = ", ".join(
                    [
                        f"{syn.name()}"
                        for syn in define_word(word.lemma, lang=input_lang_non_iso)
                        if syn.name().split(".")[1].upper() == word.pos[0]
                    ]
                )
            except AttributeError:
                definitions = "n/a"

            word_data = {
                "lemma": word.lemma,
                "morphology": modify_features(word.feats),
                "POS": word.pos,
                "DEP": word.deprel,
                "text": word.text,
                "head": head_word_text,  # Replace head ID with head word text
                "definitions": definitions,
            }
            print(word_data)
            response_data.append(word_data)

    return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
