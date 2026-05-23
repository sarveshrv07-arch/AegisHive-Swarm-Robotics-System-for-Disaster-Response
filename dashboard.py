from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():

    return '''

    <html>

    <head>

        <title>AegisHive Dashboard</title>

        <meta http-equiv="refresh" content="5">

    </head>

    <body style="font-family:Arial; background:#f4f4f4; padding:20px;">

        <h1>AegisHive Monitoring Dashboard</h1>

        <h3>System Status: Operational</h3>

        <div style="display:flex; gap:20px;">

            <div style="background:white; padding:15px; border-radius:10px; width:200px;">
                <h2>Robot 1</h2>
                <p>Status: Active</p>
                <p>Battery: 82%</p>
            </div>

            <div style="background:white; padding:15px; border-radius:10px; width:200px;">
                <h2>Robot 2</h2>
                <p>Status: Active</p>
                <p>Battery: 76%</p>
            </div>

            <div style="background:white; padding:15px; border-radius:10px; width:200px;">
                <h2>Robot 3</h2>
                <p>Status: Returning to Base</p>
                <p>Battery: 18%</p>
            </div>

        </div>

        <br>

        <div style="background:white; padding:15px; border-radius:10px; width:300px;">

            <h2>Mission Information</h2>

            <p>Robots Active: 3</p>
            <p>Survivors Detected: 2</p>

        </div>

    </body>

    </html>

    '''


@app.route('/status')
def status():

    return {

        'robots': 3,

        'system': 'Operational',

        'survivors_detected': 2

    }


if __name__ == '__main__':

    app.run(debug=True)
