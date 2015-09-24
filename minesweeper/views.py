from pyramid.view import view_config
from services import GameService, Jsonify
from models import Player

@view_config(route_name='home', renderer='templates/index.pt')
def my_view(request):
    return {'project': 'minesweeper'}

@view_config(route_name='api.init', renderer='json')
def start_game_view(request):
    print 'Init game...'
    global service
    player = Player("player1")
    service = GameService(10, 10, 5, [player])
    service.add_player_to_game([player])
    service.set_board()
    print "mines:", service._game._mines
    return Jsonify.to_board_view(service._game._board, service._game._result);
