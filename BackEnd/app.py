from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

WORDS_FILE = "words.json"


def load_words():
    if os.path.exists(WORDS_FILE):
        with open(WORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_words(words):
    with open(WORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)

@app.route("/api/words", methods=["GET"])
def get_words():
    return jsonify(load_words())

@app.route("/api/add", methods=["POST"])
def add_word():
    data = request.json
    word = data.get("word")
    translation = data.get("translation")
    words = load_words()
    words.append({"word": word, "translation": translation})
    save_words(words)
    return jsonify({"message": "Word added!"})

@app.route("/api/translate/<word>", methods=["GET"])
def translate(word):
    words = load_words()
    for w in words:
        if w["word"].lower() == word.lower():
            return jsonify({"translation": w["translation"]})
    return jsonify({"translation": "Немає в словнику"}), 404

if __name__ == "__main__":
    app.run(debug=True)
