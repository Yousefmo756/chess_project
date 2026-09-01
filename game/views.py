import json

from django.shortcuts import render
from django.http import JsonResponse
from game.chess import Game 
from game.models import ChessGame
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def game(request):
    return render(request,'looks.html')      

@csrf_exempt

def create_game(request):
    game = Game()  # your chess engine object

    state = game.to_state_dict()  # converts tuples → lists, extracts positions + moves_log

    obj = ChessGame.objects.create(
        positions=state["positions"],   # <-- YOU are telling the model what "positions" means here
        moves_log=state["moves_log"],
        turn="white",
    )
    obj.save()  
    return JsonResponse({"id": obj.id, "board": game.translate_board(), "turn": "white"})
@csrf_exempt
def make_move(request, game_id):
    obj = ChessGame.objects.get(id=game_id)
    game = Game.from_state_dict({"positions": obj.positions, "moves_log": obj.moves_log})
    if obj.status in ['checkmate', 'stalemate', 'draw']:
     return JsonResponse({"error": "game ended"}, status=400) 

    body = json.loads(request.body)
    isturn=False
    if(obj.turn=='black' and game.is_black(body["from"])):
        isturn=True
    if(obj.turn=='white' and game.is_white(body["from"])):
        isturn=True    
    if not isturn:
            return JsonResponse({"error": "Illegal move"}, status=400) 
       
    ok = game.move_piece(body["from"], body["to"], to_promote=body.get("promotion"))
    if not ok:
        return JsonResponse({"error": "Illegal move"}, status=400)
    
    obj.turn = "black" if obj.turn == "white" else "white"
    obj.status = game.is_game_end(obj.turn)   # <-- one call instead of four scattered checks

    state = game.to_state_dict()
    obj.positions = state["positions"]
    obj.moves_log = state["moves_log"]
    obj.save()

    return JsonResponse({"board": game.translate_board(), "turn": obj.turn, "status": obj.status})
def get_board(request, game_id):
    obj = ChessGame.objects.get(id=game_id)
    game = Game.from_state_dict({"positions": obj.positions, "moves_log": obj.moves_log})
    return JsonResponse({"board": game.translate_board(), "turn": obj.turn, "status": obj.status})

