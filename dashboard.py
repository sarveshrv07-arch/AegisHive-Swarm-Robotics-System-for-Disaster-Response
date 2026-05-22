from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():

    return "AegisHive Dashboard Active"


@app.route('/status')
def status():

    return {

        'robots': 5,

        'system': 'Operational',

        'survivors_detected': 2

    }


if __name__ == '__main__':

    app.run(debug=True)
