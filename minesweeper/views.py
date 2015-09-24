from pyramid.view import view_config
from services import GameService, Jsonify
from models import Player

global level
level=0

@view_config(route_name='home', renderer='templates/index.pt')
def my_view(request):
    return {'project': 'minesweeper'}

@view_config(route_name='api.init', renderer='json')
def start_game_view(request):
    global level, service
    print 'Init game...'
    player = Player("player1")
    if level==0:
        service = GameService(10, 10, 5, [player])
    elif level==1:
        service = GameService(16, 16, 40, [player])
    elif level==2:
        service = GameService(20, 20, 80, [player])
    service.add_player_to_game([player])
    service.set_board()
    print "mines:", service._game._mines
    return Jsonify.to_board_view(service._game._board, service._game._result);

@view_config(route_name='api.update', renderer='json')
def update_view(request):
    row = int(request.json_body['row'])
    col = int(request.json_body['col'])
    print "Update:", row, col
    service.update_board_with_reveal(row, col)
    if service._game._result==1:
        global  level
        level += 1
    return [Jsonify.to_board_view(service._game._board, service._game._result), service._game._result];