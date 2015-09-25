from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    my_session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings, session_factory=my_session_factory)
    config.include('pyramid_chameleon')
    config.include("pyramid_beaker")
    config.add_static_view('static', 'static', cache_max_age=0)
    config.add_route('home', '/')
    #Add my route config here
    config.add_route('api.init', '/api/init')
    config.add_route('api.new', '/api/new')
    config.add_route('api.update', '/api/update')
    config.add_route('api.flag', '/api/flag')
    config.scan()
    return config.make_wsgi_app()
