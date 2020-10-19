from templator import render


class Index:

    def __call__(self, request):
        return '200 OK', [b'Main page']


class Products:

    def __call__(self, request):
        return '200 OK', [b'Examples of products']


class Contacts:

    def __call__(self, request):
        return '200 OK', [b'Our contacts']


class Error_page:

    def __call__(self, request):
        return '404 ERROR', [b'404 PAGE Not Found']


routes = {
    '/': Index(),
    '/products/': Products(),
    '/contacts/': Contacts()
}


def secret_front(request):
    request['secret'] = 'some secret'


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]


class Application:

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if path[(len(path)) - 1] != '/':
            path += ('/')
        view = Error_page()
        if path in self.routes:
            view = self.routes[path]
        request = {}
        for front in self.fronts:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return body


application = Application(routes, fronts)

# Для запуска используем gunicorn
# gunicorn simple_wsgi:application
