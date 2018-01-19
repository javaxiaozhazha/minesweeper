import sys
import itertools

from pyramid.interfaces import IRoutesMapper, ISettings, IRouteRequest
from pyramid.interfaces import IViewMapperFactory, IViewMapper
from pyramid.interfaces import IRequest, IViewClassifier
from pyramid.static import static_view
from pyramid.view import _find_views
from zope.interface import providedBy
from zope.interface import Interface

def pyramid_test(request):
    route = request.matched_route
    q = request.registry.queryUtility
    routes_mapper = q(IRoutesMapper)
    view_mapper_fact = q(IViewMapperFactory)
    view_mapper = q(IViewMapper)
    settings = q(ISettings)
    routes_request = q(IRouteRequest, name=route.name)

    rm_info = routes_mapper(request)
    info = routes_request
    print dir(info)
    print info.getName()
    print get_views(request)
    get_view_by_introspector(request, route)

def get_views(request):
    views = []
    q = request.registry.queryUtility
    request_iface = q(IRouteRequest, name=request.matched_route.name)
    view_callables = _find_views(request.registry, request_iface, Interface, '')
    view_callable = view_callables[0]
    dir(view_callable)
    # view_module = _get_view_module(view_callables[0])
    return ".".join([view_callable.__module__, view_callable.__name__])

def get_view_by_introspector(request, route):
    """
    Introspector can be turned off though, See __init__.py
    """
    introspector = request.registry.introspector
    route_intr = introspector.get('routes', route.name)

    related_intr = introspector.related(route_intr)
    if related_intr is None:
        return None

    for related in related_intr:
        print "related", related
        if related.category_name == 'views':
            view_func = related['callable']
            if isinstance(view_func, static_view):
                # Lets skip over static views
                continue
            if related['attr']:
                view_action = ".".join([view_func.__module__, view_func.__name__, related['attr']])
            else:
                view_action = ".".join([view_func.__module__, view_func.__name__])
            return view_action

def _get_view_module(view_callable):
    if view_callable is None:
        return UNKNOWN_KEY

    if hasattr(view_callable, '__name__'):
        if hasattr(view_callable, '__original_view__'):
            original_view = view_callable.__original_view__
        else:
            original_view = None

        if isinstance(original_view, static_view):
            if original_view.package_name is not None:
                return '%s:%s' % (
                    original_view.package_name,
                    original_view.docroot
                )
            else:
                return original_view.docroot
        else:
            view_name = view_callable.__name__
    else:
        # Currently only MultiView hits this,
        # we could just not run _get_view_module
        # for them and remove this logic
        view_name = str(view_callable)

    view_module = '%s.%s' % (
        view_callable.__module__,
        view_name,
    )

    # If pyramid wraps something in wsgiapp or wsgiapp2 decorators
    # that is currently returned as pyramid.router.decorator, lets
    # hack a nice name in:
    if view_module == 'pyramid.router.decorator':
        view_module = '<wsgiapp>'

    return view_module
