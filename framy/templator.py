from jinja2 import Environment, FileSystemLoader


def render(template_name, folder='templates', **kwargs):
    env = Environment()
    # указываем папку для поиска шаблонов
    env.loader = FileSystemLoader(folder)
    # находим шаблон в окружении
    template = env.get_template(template_name)
    return template.render(**kwargs)

# Отладка
# if __name__ == '__main__':
#     output_test = render('index.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])
#     print(output_test)
