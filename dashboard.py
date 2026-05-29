from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():

    import json

    try:

        with open("dashboard_data.json", "r") as file:

            robot_data = json.load(file)

    except Exception as e:

        print(e)

        return {}

    robots_html = ""

    for robot in robot_data["robots"]:

      robots_html += f"""

      <div style="
        background:white;
        padding:15px;
        border-radius:10px;
        width:220px;
      ">

        <h2>Robot {robot['id']}</h2>

        <p id="status-{robot['id']}">
           Status: {robot['status']}
        </p>

        <p id="battery-{robot['id']}">
           Battery: {robot['battery']}%
        </p>

        <p id="explored-{robot['id']}">
           Area Explored: {robot['explored']}%
        </p>

        <p id="survivors-{robot['id']}">
           Survivors Found: {robot['survivors']}
        </p>

      </div>
      """

    return f'''

      <html>

      <head>

       <title>AegisHive Dashboard</title>

       

      </head>

      <body style="
        font-family:Arial;
        background:#f4f4f4;
        padding:20px;
      ">

        <h1>AegisHive Monitoring Dashboard</h1>

        <h3>System Status: Operational</h3>

        <h3 id="mission-time">
        Mission Time: {robot_data["mission_time"]} sec
        </h3>

        <h3 id="overall-explored">Overall Explored:
         {robot_data["overall_explored"]}%
        </h3>

        <div id="robots-container"
          style="display:flex; gap:20px; flex-wrap:wrap;">

         {robots_html}

        </div>

        <br>

        <div style="
          background:white;
          padding:15px;
          border-radius:10px;
          width:300px;
       ">

          <h2>Mission Information</h2>

          <p id="robots-active">
          Robots Active:
            {len(robot_data["robots"])}
          </p>

          <p id="survivors-detected">
          Survivors Detected:
            {robot_data["survivors_detected"]}
          </p>

        </div>

      <script>

      async function updateDashboard() {{

            const response = await fetch('/status');

            const data = await response.json();

            document.getElementById("mission-time").innerHTML =
                 `Mission Time: ${{data.mission_time}} sec`;

            document.getElementById("overall-explored").innerHTML =
                 `Overall Explored: ${{data.overall_explored}}%`;

            document.getElementById("robots-active").innerHTML =
                 `Robots Active: ${{data.robots.length}}`;

            document.getElementById("survivors-detected").innerHTML =
                 `Survivors Detected: ${{data.survivors_detected}}`;

            data.robots.forEach(robot => {{

                 document.getElementById(
                     `status-${{robot.id}}`
                 ).innerHTML =
                     `Status: ${{robot.status}}`;

                 document.getElementById(
                     `battery-${{robot.id}}`
                 ).innerHTML =
                     `Battery: ${{robot.battery}}%`;

                 document.getElementById(
                     `explored-${{robot.id}}`
                 ).innerHTML =
                     `Area Explored: ${{robot.explored}}%`;

                 document.getElementById(
                     `survivors-${{robot.id}}`
                 ).innerHTML =
                     `Survivors Found: ${{robot.survivors}}`;
            }});
      }}
            
      updateDashboard();

      setInterval(updateDashboard, 300);

      </script>

      </body>

      </html>
      '''


@app.route('/status')
def status():

    import json

    try:

        with open("dashboard_data.json", "r") as file:

            robot_data = json.load(file)

    except:

        robot_data = {

            "robots": [],

            "overall_explored": 0,

            "mission_time": 0,

            "survivors_detected": 0
        }

    return robot_data


if __name__ == '__main__':

    app.run(debug=False, threaded=True)
