from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Alfred proposes to Florina for the 3rd time"

app.run(host='0.0.0.0',port=3000)
