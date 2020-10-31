from framy.templator import render


class Index:

    def __call__(self, request):
        # return '200 OK', [b'Main page']
        return '200 OK', render('index.html')


class Products:

    def __call__(self, request):
        return '200 OK', 'Examples of products'


class Contacts:

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            title = data['title']
            text = data['text']
            email = data['email']
            print(f'Нам пришло сообщение от {email} с темой {title} и текстом {text}')
            return '200 OK', render('contacts.html')
        else:
            return '200 OK', render('contacts.html')


class Error_page:

    def __call__(self, request):
        return '404 ERROR', [b'404 PAGE Not Found']
