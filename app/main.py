from flask import Flask, render_template

app = Flask(__name__)

TEXT_1 = "Flroina accepted the proposals from Alfred for the 3rd time"
TEXT_2 = "Alfred proposes to Florina for an infinite number of times"

@app.route('/')
def home():
   return render_template('index.html', bride="Florina", groom="Alfred")

@app.route('/<name>')
def outside(name):
    return name

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=3000)
