from flask import Flask, json
import os, importlib

app = Flask(__name__)

players = {}

@app.route("/")
def showFrontend():
  return app.send_static_file('frontend.html')

@app.route("/get-ai-players")
def getAiPlayers():
  return json.jsonify(os.listdir("player"))

@app.route("/init-ai-player/<ai_name>")
def initAiPlayer(ai_name):
  players.pop(ai_name, None)
  try:
    mod = importlib.import_module("player.{}.player".format(ai_name))
    players[ai_name] = getattr(mod, 'Player')()    
  except:
    return json.jsonify({
      "error": True,
      "error_msg": "{} is not available"
    })
  else:
    return json.jsonify([ai_name])

@app.route("/call-ai-player/<ai_name>/<board_state>/<player_n>")
def callAiPlayer(ai_name, board_state, player_n):
  board_state = [int(x) for x in board_state.split(',')]
  if ai_name in list(players.keys()):
    return json.jsonify({
      "error": False,
      "board_state": board_state,
      "move": players[ai_name].play(board_state, int(player_n))
    })
  else:
    return json.jsonify({
      "error": True,
      "error_msg": "{} is not initiated"
    })

@app.route("/get-init-ai-players")
def getInitAiPlayers():
  return json.jsonify(list(players.keys()))