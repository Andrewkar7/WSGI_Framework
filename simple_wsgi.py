# Для запуска используем gunicorn
# gunicorn simple_wsgi:application

from framy.heart import Application, DebugApplication, FakeApplication
from framy.templator import render
from models import OurSite
from logging_our import Logger, debug

site = OurSite()
logger = Logger('wsgi')


def main_view(request):
    logger.log('Список курсов')
    return '200 OK', render('course_list.html', objects_list=site.courses)


@debug
def create_course(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        category_id = data.get['category_id']
        print(category_id)
        if category_id:
            category = site.find_category_by_id(int(category_id))

            course = site.create_course('record', name, category)
            site.courses.append(course)
        return '200 OK', render('create_course.html')
    else:
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)


def create_category(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        category_id = data.get['category_id']
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_course(name, category)
        site.categories.append(new_category)
        return '200 OK', render('create_category.html')
    else:
        categories = site.categories
        return '200 OK', render('create_category.html', categories=categories)


routes = {
    '/': main_view,
    '/create-course/': create_course,
    '/create-category/': create_category,
}


def secret_front(request):
    request['secret'] = 'some secret'


fronts = [secret_front]

application = Application(routes, fronts)
# application = DebugApplication(routes, fronts)
# application = FakeApplication(routes, fronts)

@application.add_route('/copy-course/')
def copy_course(request):
    request_params = request['request_params']
    name = request_params['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return '200 OK', render('course_list.html', objects_list=site.courses)


@application.add_route('/category-list/')
def category_list(request):
    logger.log('Список категорий')
    return '200 OK', render('category_list.html', objects_list=site.categories)
