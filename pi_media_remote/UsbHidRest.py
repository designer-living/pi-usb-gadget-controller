#!/usr/bin/env python3

from flask import Flask, redirect
from flask_restful import Resource, Api
import os
from pi_media_remote.send_key import press_key

app = Flask(__name__)
api = Api(app)

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
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <title>REMOTE</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

<!--  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"> -->
<!--  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script> -->
<!--  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script> -->
</head>
<body class="bg-dark">
    <br>
    <div class="container-sm bg-dark rounded text-center">
            <br>
            <div class="row">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col-10">
                    <a class="btn btn-dark btn-lg text-light btn-outline-primary" href="/up" role="button">&uarr;</a>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <div class="row">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col-10 mt-1 mb-1">
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/left" role="button">&larr;</a>
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/select" role="button"><small>ok</small></a>
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/right" role="button">&rarr;</a>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <div class="row">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col-10 mb-5">
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/down" role="button">&darr;</a>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <div class="row mb-4">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col">
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/home" role="button">&thinsp;&nbsp;&#8962;&nbsp;&thinsp;</a>
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/play" role="button">&#9658;&par;</a>
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/back" role="button">&nbsp;&crarr;&nbsp;</a>
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/" role="button">&nbsp;&#9212;&nbsp;</a>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <div class="row">
                <div class="col-2">
                    &emsp;
                </div>
                <div class="col-8" id="dropDownDiv">
                    
                </div>
                <div class="col-2">
                    &emsp;
                </div>
            </div>
            <div class="row mt-5">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col-10">
                    <p class="text-light"><small id="statusMessage">&emsp;</small></p>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <br>
        <br>
    </div>
</body>
</html>
    """












class KeyPresser(Resource):

    def __init__(self, key):
      self.key = key

    def get(self):
        press_key(self.key)
        return redirect(redirect_link)



#class Play(Resource):
#    def get(self):
#        press_key('PLAY')
#        return {'hello': 'world'}


#api.add_resource(Root, '/')
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
