from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello Florina"

app.run(host='0.0.0.0',port=3000)
