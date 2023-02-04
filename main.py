from flask import Flask, jsonify, request, escape, Response, render_template, make_response, abort
from threading import Thread
from flask_restful import Resource, Api
import json
import random
from random import choices
import os.path
import uuid
import resp
from datetime import datetime
import hashlib

app = Flask('')
api = Api(app)

def findBy(IDToFind, JSONObject, fieldToFind):
    for item in JSONObject:
        if item[fieldToFind].lower() == IDToFind.lower():
            return item
          
def remove(string):
  return string.replace(" ", "")
  
@app.route('/', defaults={'path': '/home.html'})
@app.route('/<path:path>')
def get_resource(path):
  mimetypes = {
      ".css": "text/css",
      ".html": "text/html",
      ".js": "application/javascript",
      ".ttf": "font/ttf",
      ".ico": "image/x-icon",
      ".jpg": "image/jpeg"
  }
  ext = os.path.splitext(path)[1]
  mimetype = mimetypes.get(ext, "text/html")
  if ext == ".ttf":
    content = open(path.replace("/", ""), mode='rb').read()
  elif ext == ".jpg":
    content = open("images/" + path.replace("/", ""), mode='rb').read()
  else:
    content = open(path.replace("/", "")).read()
  return Response(content, mimetype=mimetype)


api.add_resource(List, '/api/lists/<ID>')

def run():
  app.run(host='0.0.0.0', port=7210, threaded = True)

t = Thread(target=run)
t.start()