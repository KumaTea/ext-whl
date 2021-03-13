import os


html = ''
path = 'whl'
prefix = f'{path}'
files = os.listdir(path)

for wheel in files:
	html += f'<a href=\"{prefix}/{wheel}\">{wheel}</a><br>\n'


with open('wheels.html', 'w', encoding='utf-8') as html_file:
   html_file.write(html)

