#!/usr/bin/env python3

from flask import Flask, redirect
from flask_restful import Resource, Api
from pi_media_remote.send_key import SendGadgetDevice
from pi_media_remote.html import JS_HOMEPAGE

app = Flask(__name__)
api = Api(app)
gadget_device = SendGadgetDevice('/dev/hidg0')

redirect_link = "/"

@app.route("/index2")
def root():
#class Root(Resource):
      return """
      <html>
      <head></head>
      <body>
      <ul>
      <li><a href="/up">UP</a></li>
      <li><a href="/down">DOWN</a></li>
      <li><a href="/left">LEFT</a></li>
      <li><a href="/right">RIGHT</a></li>
      <li><a href="/select">SELECT</a></li>
      <li><a href="/home">HOME</a></li>
      <li><a href="/back">BACK</a></li>
      <li><a href="/play">PLAY/PAUSE</a></li>
      </body>
      </html>
      """

@app.route("/")
def index2():
    return JS_HOMEPAGE


class KeyPresser(Resource):

    def __init__(self, key):
      self.key = key

    def get(self):
        gadget_device.press_key(self.key)
        return redirect(redirect_link)



api.add_resource(KeyPresser, '/up', endpoint="up", resource_class_kwargs={'key': 'UP'})
api.add_resource(KeyPresser, '/down', endpoint="down", resource_class_kwargs={'key': 'DOWN'})
api.add_resource(KeyPresser, '/left', endpoint="left", resource_class_kwargs={'key': 'LEFT'})
api.add_resource(KeyPresser, '/right' , endpoint="right", resource_class_kwargs={'key': 'RIGHT'})
api.add_resource(KeyPresser, '/select' , endpoint="select", resource_class_kwargs={'key': 'SELECT'})
api.add_resource(KeyPresser, '/home' , endpoint="home", resource_class_kwargs={'key': 'HOME'})
api.add_resource(KeyPresser, '/back' , endpoint="back", resource_class_kwargs={'key': 'BACK'})
api.add_resource(KeyPresser, '/play' , endpoint="play", resource_class_kwargs={'key': 'PLAY'})

def main():
    app.run(host='0.0.0.0', port=5000, debug=True)
