class Application:

    def parse_input_data(self, data: str):
        result = {}
        if data:
            # делим параметры через &
            params = data.split('&')
            for item in params:
                # делим ключ и значение через =
                k, v = item.split('=')
                result[k] = v
        return result

    def get_wsgi_input_data(self, environ) -> bytes:
        # получаем длину тела
        content_length_data = environ.get('CONTENT_LENGTH')
        # приводим к int
        content_length = int(content_length_data) if content_length_data else 0
        # считываем данные если они есть
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            # декодируем данные
            data_str = data.decode(encoding='utf-8')
            # собираем их в словарь
            result = self.parse_input_data(data_str)
        return result

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if path[(len(path)) - 1] != '/':
            path += ('/')

        # Метод которым отправили запрос
        method = environ['REQUEST_METHOD']
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)

        # получаем параметры запроса
        query_string = environ['QUERY_STRING']
        request_params = self.parse_input_data(query_string)

        if path in self.routes:
            view = self.routes[path]
            request = {}
            request['method'] = method
            request['data'] = data
            request['request_params'] = request_params
            for front in self.fronts:
                front(request)
            code, text = view(request)
            start_response(code, [('Content-Type', 'text/html')])
            return [text.encode('utf-8')]
        else:
            start_response('404 ERROR', [('Content-Type', 'text/html')])
            return [b'404 PAGE Not Found']
