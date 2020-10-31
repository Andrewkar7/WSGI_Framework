import os
from jinja2 import Template


def render(template_name, **kwargs):
    path = os.path.join('templates', template_name)
    with open(path, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)

# Отладка
# if __name__ == '__main__':
#     output_test = render('index.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])
#     print(output_test)
