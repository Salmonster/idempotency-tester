from flask import Flask

app = Flask(__name__)

@app.route("/")
def main_view():
    return "<h1>Site under construction</h1>"
