from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Flroina accepted the proposals from Alfred for the 3rd time"

app.run(host='0.0.0.0',port=3000)
