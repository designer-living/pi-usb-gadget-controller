from flask import Flask, redirect
from flask_restful import Resource, Api
import os
from send_key import press_key

app = Flask(__name__)
api = Api(app)

@app.route("/")
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
      <li><a href="/play">PLAY/PAUSE</a></li>
      </ul>
      </body>
      </html>
      """


class KeyPresser(Resource):

    def __init__(self, key):
      self.key = key

    def get(self):
        press_key(self.key)
        return redirect("/")



class Play(Resource):
    def get(self):
        press_key('PLAY')
        return {'hello': 'world'}


#api.add_resource(Root, '/')
api.add_resource(KeyPresser, '/up', endpoint="up", resource_class_kwargs={'key': 'UP'})
api.add_resource(KeyPresser, '/down', endpoint="down", resource_class_kwargs={'key': 'DOWN'})
api.add_resource(KeyPresser, '/left', endpoint="left", resource_class_kwargs={'key': 'LEFT'})
api.add_resource(KeyPresser, '/right' , endpoint="right", resource_class_kwargs={'key': 'RIGHT'})
api.add_resource(KeyPresser, '/select' , endpoint="select", resource_class_kwargs={'key': 'SELECT'})
api.add_resource(KeyPresser, '/home' , endpoint="home", resource_class_kwargs={'key': 'HOME'})
api.add_resource(KeyPresser, '/back' , endpoint="back", resource_class_kwargs={'key': 'BACK'})
api.add_resource(KeyPresser, '/play' , endpoint="play", resource_class_kwargs={'key': 'PLAY'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
