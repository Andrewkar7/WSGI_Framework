import views
from framy.heart import Application

routes = {
    '/': views.Index(),
    '/products/': views.Products(),
    '/contacts/': views.Contacts()
}


def secret_front(request):
    request['secret'] = 'some secret'


fronts = [secret_front]

application = Application(routes, fronts)

# Для запуска используем gunicorn
# gunicorn simple_wsgi:application
