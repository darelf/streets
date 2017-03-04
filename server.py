from sanic import Sanic
from sanic.response import html, text
from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)

jade = {
    'title_name': 'Jade',
    'name': 'Jane Worth',
    'species': 'Human',
    'alterations': 'Skilljack',
    'comments': ['Curabitur varius pharetra neque id porta. Duis hendrerit et massa eget consequat. In mollis diam quis lectus tempus porttitor']
}

app = Sanic()

app.static('/static/', './static/')
app.static('/favicon.ico', './static/favicon.ico')


@app.get('/')
async def index(request):
    return html(env.get_template('index.html').render(title="Street Scum"))

@app.get('/contact/<name>')
async def contact(request, name):
    return html(env.get_template('contact.html').render(title="Street Scum", contact=jade))


app.run("0.0.0.0", port=8888)
