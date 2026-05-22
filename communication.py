import paho.mqtt.client as mqtt

import json


class SwarmCommunication:

    def __init__(self):

        self.client = mqtt.Client()

        self.client.connect(
            'localhost',
            1883
        )

    def send_status(self, robot):

        data = {

            'robot_id': robot.robot_id,

            'x': robot.x,

            'y': robot.y,

            'battery': robot.battery

        }

        self.client.publish(

            'aegishive/swarm',

            json.dumps(data)

        )
