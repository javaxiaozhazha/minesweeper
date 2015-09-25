from pyramid.view import view_config
from services import GameService, Jsonify
from models import Player

ERROR = {"404":"Game Service not found"}

@view_config(route_name='home', renderer='templates/index.pt')
def my_view(request):
    return {'project': 'minesweeper'}

@view_config(route_name='api.init', renderer='json')
def load_game_view(request):
    """If unfinished game is found in memory, then load it
     Otherwise create a new game
    """
    level = 0
    if 'level' not in request.session:
        request.session['level'] = level
    else:
        level = request.session['level']
    #If there was no game service, or  current game finished, then we can start a new  game service
    if 'service' not in request.session or request.session['service']._game._result is not 0:
        print 'Init game...'
        service = create_game(level, [Player("player1")])
        request.session['service'] = service
    else:
        print "load existing game..."
        service = request.session["service"]
    print "mines:", service._game._mines
    return [Jsonify.to_board_view(service._game._board, service._game._result),
            request.session['level']];

@view_config(route_name='api.new', renderer='json')
def new_game_view(request):
    """Create a new game from level 0 no matter what
    """
    print 'Start a new game from beginner level...'
    level = 0
    service = create_game(level, [Player("player1")])
    request.session['service'] = service
    request.session['level'] = level
    print "mines:", service._game._mines
    return [Jsonify.to_board_view(service._game._board, service._game._result),
            request.session['level']];

@view_config(route_name='api.update', renderer='json')
def update_view(request):
    """Call this view when left click to reveal a cell
    """
    if 'service' not in request.session:
        return ERROR
    service = request.session["service"]
    row = int(request.json_body['row'])
    col = int(request.json_body['col'])
    print "Update:", row, col
    service.update_board_with_reveal(row, col)
    if service._game._result==1: #Enter next level if player won
        request.session['level'] += 1
    return [Jsonify.to_board_view(service._game._board, service._game._result),
            service._game._result, request.session['level']];

@view_config(route_name='api.flag', renderer='json')
def flag_view(request):
    """Call this view when right click a cell to flag it
    """
    if 'service' not in request.session:
        return ERROR
    service = request.session["service"]
    row = int(request.json_body['row'])
    col = int(request.json_body['col'])
    service.update_board_with_flag(row, col)
    return [Jsonify.to_board_view(service._game._board, service._game._result),
            service._game._result, request.session['level']];

#helper function
def create_game(level, players):
    """Create game according to game level and players
    """
    service = None
    if level==0:
        service = GameService(10, 10, 5, players)
    elif level==1:
        service =  GameService(16, 16, 40, players)
    elif level==2:
        service = GameService(20, 20, 80, players)
    service.add_player_to_game([players[0]])
    service.set_board()
    return service