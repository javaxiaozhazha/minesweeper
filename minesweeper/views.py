from pyramid.view import view_config
from services import GameService, Jsonify
from models import Player

ERROR = {"404":"Resources not found"}

@view_config(route_name='home', renderer='templates/index.pt')
def my_view(request):
    return {'project': 'minesweeper'}

@view_config(route_name='api.init', renderer='json')
def start_game_view(request):
    service = None
    level = 0
    if 'level' not in request.session:
        request.session['level'] = level
    else:
        level = request.session['level']

    if 'service' not in request.session or request.session['service']._game._result is not 0:
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
        request.session['service'] = service
    else:
        service = request.session["service"]
    print "mines:", service._game._mines
    return Jsonify.to_board_view(service._game._board, service._game._result);

@view_config(route_name='api.update', renderer='json')
def update_view(request):
    if 'service' not in request.session:
        return ERROR
    service = request.session["service"]
    row = int(request.json_body['row'])
    col = int(request.json_body['col'])
    print "Update:", row, col
    service.update_board_with_reveal(row, col)
    if service._game._result==1:
        request.session['level'] += 1
    return [Jsonify.to_board_view(service._game._board, service._game._result), service._game._result];