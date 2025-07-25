from flask import Flask, request, jsonify, redirect, abort
import datetime
import random
import string
import threading

app = Flask(__name__)

# In-memory store and lock for thread safety
url_store = {}
lock = threading.Lock()

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/api/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    long_url = data.get("url") if data else None
    if not long_url or not long_url.startswith(("http://", "https://")):
        return jsonify({"error": "Invalid URL"}), 400

    with lock:
        code = generate_code()
        while code in url_store:
            code = generate_code()

        url_store[code] = {
            "url": long_url,
            "clicks": 0,
            "created_at": datetime.datetime.utcnow().isoformat()
        }

    return jsonify({
        "short_code": code,
        "short_url": f"http://localhost:5000/{code}"
    }), 200

@app.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):
    with lock:
        if short_code not in url_store:
            abort(404)
        url_store[short_code]["clicks"] += 1
        target_url = url_store[short_code]["url"]
    return redirect(target_url)

@app.route("/api/stats/<short_code>", methods=["GET"])
def stats(short_code):
    with lock:
        if short_code not in url_store:
            abort(404)
        data = url_store[short_code]
    return jsonify({
        "url": data["url"],
        "clicks": data["clicks"],
        "created_at": data["created_at"]
    })
