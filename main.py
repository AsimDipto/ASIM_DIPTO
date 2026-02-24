from flask import Flask, Response
import os

app = Flask(__name__)

# মেইন হোমে কেউ ঢুকলে এই মেসেজ দেখাবে
@app.route('/')
def home():
    return "Server is running. Access denied."

# আপনার পছন্দের সেই লম্বা এবং সিকিউর লিঙ্ক
@app.route('/Fuck-you-Ankita.m3u')
def get_playlist():
    # এটি আপনার স্ক্যানার দিয়ে তৈরি হওয়া আসল ফাইলটি পড়বে
    filename = "Fuck-you-Ankita.m3u"
    
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return Response(content, mimetype='text/plain')
    else:
        return "Playlist file not found yet. Please run scanner.py first.", 404

if __name__ == "__main__":
    # Render এর জন্য পোর্ট কনফিগারেশন
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
