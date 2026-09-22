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
    body = json.loads(request.body) if request.body else {}
    vs_ai = body.get("vs_ai", False)

    game = Game()
    state = game.to_state_dict()

    obj = ChessGame.objects.create(
        positions=state["positions"],
        moves_log=state["moves_log"],
        turn="white",
        castling_flags=state["castling_flags"],
        board_snapshots=state["board_snapshots"],

        vs_ai=vs_ai,
    )
    return JsonResponse({"id": obj.id, "board": game.translate_board(), "turn": "white"})


@csrf_exempt
def make_move(request, game_id):
    obj = ChessGame.objects.get(id=game_id)
    if obj.status in ['checkmate', 'stalemate', 'draw']:
        return JsonResponse({"error": f"{obj.status}"}, status=400)

    game = Game.from_state_dict({
        "positions": obj.positions,
        "moves_log": obj.moves_log,
        "castling_flags": obj.castling_flags,
        "board_snapshots": obj.board_snapshots,
    })

    body = json.loads(request.body)
    isturn = False
    if obj.turn == 'black' and game.is_black(body["from"]):
        isturn = True
    if obj.turn == 'white' and game.is_white(body["from"]):
        isturn = True
    if not isturn:
        return JsonResponse({"error": "Illegal move"}, status=400)

    ok = game.move_piece(body["from"], body["to"], to_promote=body.get("promotion"))
    if not ok:
        return JsonResponse({"error": "Illegal move"}, status=400)

    obj.turn = "black" if obj.turn == "white" else "white"
    obj.status = game.is_game_end(obj.turn)

    state = game.to_state_dict()
    obj.positions = state["positions"]
    obj.moves_log = state["moves_log"]
    obj.castling_flags = state["castling_flags"]
    obj.board_snapshots = state["board_snapshots"]
    obj.save()

    return JsonResponse({
        "board": game.translate_board(),
        "turn": obj.turn,
        "status": obj.status,
        "ai_to_move": obj.vs_ai and obj.turn == "black" and obj.status == "ongoing",
    })

@csrf_exempt

def ai_move(request, game_id):
    obj = ChessGame.objects.get(id=game_id)
    if obj.status in ['checkmate', 'stalemate', 'draw']:
        return JsonResponse({"error": f"{obj.status}"}, status=400)
    if not (obj.vs_ai and obj.turn == "black"):
        return JsonResponse({"error": "Not AI's turn"}, status=400)

    game = Game.from_state_dict({
        "positions": obj.positions,
        "moves_log": obj.moves_log,
        "castling_flags": obj.castling_flags,
        "board_snapshots": obj.board_snapshots,
    })

    ai_result = game.best_move("black", depth=20, time_limit=5)
    if ai_result:
        piece, (r, c), (tr, tc), _score = ai_result
        from_sq = game.unparse_move(r, c)
        to_sq = game.unparse_move(tr, tc)
        promo = 3 if (piece == 'pawns' and game.is_board_end(tr, tc)) else None
        game.move_piece(from_sq, to_sq, to_promote=promo, verified=True)

    obj.turn = "white"
    obj.status = game.is_game_end(obj.turn)

    state = game.to_state_dict()
    obj.positions = state["positions"]
    obj.moves_log = state["moves_log"]
    obj.castling_flags = state["castling_flags"]
    obj.board_snapshots = state["board_snapshots"]
    obj.save()

    return JsonResponse({
        "board": game.translate_board(),
        "turn": obj.turn,
        "status": obj.status,
    })
def get_board(request, game_id):
    obj = ChessGame.objects.get(id=game_id)
    game = Game.from_state_dict({
        "positions": obj.positions,
        "moves_log": obj.moves_log,
        "castling_flags": obj.castling_flags,
        "board_snapshots": obj.board_snapshots,
    })
    return JsonResponse({"board": game.translate_board(), "turn": obj.turn, "status": obj.status})
def get_legal_sqrs(request,game_id):
    obj = ChessGame.objects.get(id=game_id)
    turn=obj.turn
    game = Game.from_state_dict({
        "positions": obj.positions,
        "moves_log": obj.moves_log,
        "castling_flags": obj.castling_flags,
        "board_snapshots": obj.board_snapshots,
    })
    pos_r=None
    pos_c=None  
    try:
       pos_r = int(request.GET['row'])
       pos_c = int(request.GET['col'])
    except (KeyError, ValueError):
       return JsonResponse({"error": "row and col are required integers"}, status=400)
    all_legal_moves=game.generate_legal_moves(turn)
    legal_moves=[]
    for piece,(r,c),(tr,tc) in all_legal_moves:
        if(r,c)==(pos_r,pos_c):
            legal_moves.append([tr,tc])
    
    return JsonResponse({"row": pos_r, "col": pos_c, "moves": legal_moves})

