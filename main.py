from flask import Flask, Response
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "IPTV Playlist is Running! Use /playlist.m3u for the link."

@app.route('/Asim-dipto-ad-channels-dipto114119201-allchannels.m3u')
def get_playlist():
    filename = "only_new_channels.m3u"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return Response(content, mimetype='text/plain')
    else:
        return "Playlist file not found yet. Please run scanner.py first.", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
