from flask import Flask, Response
import os

app = Flask(__name__)


@app.route('/')
def home():
    return "Server is running. Access denied."


@app.route('/Fuck-you-Ankita.m3u')
def get_playlist():
    
    filename = "Fuck-you-Ankita.m3u"
    
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return Response(content, mimetype='text/plain')
    else:
        return "Playlist file not found yet. Please run scanner.py first.", 404

if __name__ == "__main__":
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
