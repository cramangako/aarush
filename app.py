from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
import json

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
DATA_FILE = "posts.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load posts if file exists
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        posts = json.load(f)
else:
    posts = []

def save_posts():
    with open(DATA_FILE, "w") as f:
        json.dump(posts, f, indent=2)

@app.route("/api/posts", methods=["GET"])
def get_posts():
    return jsonify(posts[::-1])  # newest first

@app.route("/api/posts", methods=["POST"])
def add_post():
    text = request.form.get("text", "")
    image = request.files.get("image")

    image_url = None
    if image:
        filename = f"{uuid.uuid4().hex}_{image.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image.save(filepath)
        image_url = f"/uploads/{filename}"

    post = {"id": uuid.uuid4().hex, "text": text, "image": image_url}
    posts.append(post)
    save_posts()
    return jsonify(post), 201

@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
