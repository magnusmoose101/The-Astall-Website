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


def probabilityPickingSystem(arrayWithProbability, message):
  overallProbability = 0
  for item in arrayWithProbability:
    overallProbability += item["probability"]

  percentages = []
  for item in arrayWithProbability:
    if item["probability"] == 0:
      percentages.append(0)
    else:
      percentages.append((item["probability"] / overallProbability) * 100)

  picked = choices(arrayWithProbability, percentages)
  print(f"{message} {picked}")

  return picked
  

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

class Movies(Resource):
  def get(self):
    with open('movieData.json', 'r') as openJsonReadable:
      movieData = json.load(openJsonReadable)
    return movieData

    
  def post(self):
    with open('movieData.json', 'r') as openJsonReadable:
      movieData = json.load(openJsonReadable)
      
    newMovie = True
    for i in movieData:
      if remove(request.json["name"].lower()) != remove(i["name"].lower()) and newMovie == True:
        newMovie = True
      elif remove(request.json["name"].lower()) == remove(i["name"].lower()):
        newMovie = False

    if newMovie == True and remove(request.json["name"].lower()) != "":
      dataLength = len(movieData)
      print(request.json)
      
      overallProbability = 0
      for item in movieData:
        overallProbability += item["probability"]

      dataLength = len(movieData)
      meanProbabilty = overallProbability / dataLength

      print(f"Probability: {meanProbabilty}")
      
      movieData.append({"ID": dataLength + 1,"name": escape(request.get_json(force=True)["name"]), "addedBy": request.get_json(force=True)["addedBy"], "probability": int(round(meanProbabilty, 0))})
      
      with open("movieData.json", "w") as openJsonWritable:
        json.dump(movieData, openJsonWritable, indent=2)
      return movieData


class RandomMovie(Resource):
  def post(self):
    with open('movieData.json', 'r') as openJsonReadable:
      movieData = json.load(openJsonReadable)

    with open('addedByData.json', 'r') as openJsonReadable:
      addedByData = json.load(openJsonReadable)

    usedNames = []
    for item in movieData:
      usedNames.append(item["addedBy"])

    usedNames = [*set(usedNames)]

    possibleNames = []
    for item in usedNames:
      possibleNames.append(findBy(item, addedByData, "name"))

    namePicked = probabilityPickingSystem(possibleNames, "Picked Name Data:")

    for item in possibleNames:
      if item["name"] != namePicked[0]["name"]:
        item["probability"] += 1
      else:
        item["probability"] = 0

      addedByData[item["ID"] - 1]["probability"] = int(item["probability"])

    with open("addedByData.json", "w") as openJsonWritable:
      json.dump(addedByData, openJsonWritable, indent=2)

    moviesAvailable = []
    for item in movieData:
      if item["addedBy"] == namePicked[0]["name"]:
        moviesAvailable.append(item)

    chosenMovie = probabilityPickingSystem(moviesAvailable, "Picked Movie Data:")

    for item in movieData:
      if item["name"] != chosenMovie[0]["name"]:
        item["probability"] += 1
      else:
        item["probability"] = 0

      movieData[item["ID"] - 1]["probability"] = int(item["probability"])

    with open("movieData.json", "w") as openJsonWritable:
      json.dump(movieData, openJsonWritable, indent=2)

    return chosenMovie[0]

api.add_resource(Movies, '/api/movies')
api.add_resource(RandomMovie, '/api/movies/random')

def run():
  app.run(host='0.0.0.0', port=7210, threaded = True)

t = Thread(target=run)
t.start()