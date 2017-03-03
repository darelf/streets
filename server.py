from sanic import Sanic
from sanic.response import html, text
from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)


app = Sanic()

app.static('/static/', './static/')
app.static('/favicon.ico', './static/favicon.ico')


@app.route("/")
async def index(request):
    return html(env.get_template('index.html').render(title="Street Scum"))


app.run("0.0.0.0", port=8888)
